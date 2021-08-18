import sys
sys.path.insert(0, r'F:\Ensembled-AI-Trading-System')

import pandas as pd
from Utilities.config import *
from Utilities.Database_funcs import *
from Utilities.util_funcs import dataset_length
from autogluon.tabular import TabularDataset, TabularPredictor

# https://github.com/awslabs/autogluon/blob/master/docs/tutorials/tabular_prediction/tabular-quickstart.md


# Configured for regression task, can do classification as well.

class AutoML(object):
    
    def __init__(self):
        
        print("|---------------------------------|")
        print("|AutoML model has been initialized|")
        print("|---------------------------------|")

        pass

    def AML_model(self, data):

        self.data = data

        # Total time in seconds that the models will be training
        # Naturally, increase for performance
        time_limit = 6

        # Provide the eval_metric if you know what metric will be used to evaluate predictions in your application. Some other non-default metrics you might use include things like: 'f1' (for binary classification), 'roc_auc' (for binary classification), 'log_loss' (for classification), 'mean_absolute_error' (for regression), 'median_absolute_error' (for regression). 
        # You can also define your own custom metric function, see examples in the folder: autogluon/core/metrics/

        metric = 'root_mean_squared_error'  # specify your evaluation metric here
        loss_function='Logloss:border=1.5'

        date = self.data['date']
        symbol = self.data['crypto_id'][1]

        self.data.drop(['date', 'crypto_id'], axis=1, inplace=True)

        # TODO // 1 where 2 consecutive return columns for close are on top 30% of normal distribution.

        # Creating binary label column
        self.data['TARGET']  = np.where(self.data['close'].shift(-1) > self.data['close'], 1, -1) 
        X = self.data.loc[:, self.data.columns != 'close']

        label = 'TARGET'

        split = dataset_length(self.data)
        remain = len(self.data) - split

        date = date[:remain]
        print(date)

        # Splitiing the X and y into train and test datasets
        X_train, X_test = X[-split:], X[:remain]
        y_train, y_test = label[:split], label[split:]

        # Print the size of the train and test dataset
        print("|-------------------------------------------------------|")
        print("X_train shape is:", X_train.shape,"X_test shape is:", X_test.shape)
        print("|-------------------------------------------------------|")

        train_data = TabularDataset(X_train)
        test_data = TabularDataset(X_test)
      
        subsample_size = 7500  # subsample subset of data for faster demo, try setting this to much larger values
        train_data = train_data.sample(n=subsample_size, random_state=0)

        save_path = r'F:\Ensembled-AI-Trading-System\data\models'  # specifies folder to store trained models

        # If 'binary' is not the correct problem_type, please manually specify the problem_type argument in fit() 
        # (You may specify problem_type as one of: ['binary', 'multiclass', 'regression'])

        predictor = TabularPredictor(label, eval_metric=metric, verbosity=2).fit(train_data, time_limit=time_limit, presets='best_quality')        
        performance = predictor.evaluate(test_data)

        print("|-------------------------------------------------------|")
        print("AutoGluon Performance:", performance)
        print("|-------------------------------------------------------|")

        model_performance = predictor.leaderboard(test_data, silent=True)

        print("|-------------------------------------------------------|")
        print("AutoGluon Models Performance:", model_performance)
        print("|-------------------------------------------------------|")

        y_pred = predictor.predict(test_data)

        print(y_pred.dtype)

        # TODO // Configure for more than 2 outputs (-1, 1), achieved through loss function

        # perf = predictor.evaluate_predictions(y_true=label, y_pred=y_pred, auxiliary_metrics=True)

        # print("|-------------------------------------------------------|")
        # print("Prediction evaluation:", perf)
        # print("|-------------------------------------------------------|")

        predictions  = pd.DataFrame()
        predictions['AutoGluon Preds'] = y_pred
        predictions['Date'] = date

        return predictions
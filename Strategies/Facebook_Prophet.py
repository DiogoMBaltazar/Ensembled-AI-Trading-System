import sys
import fbprophet
sys.path.insert(0, r'F:\Ensembled-AI-Trading-System')

# Import Libraries
from fbprophet import Prophet
import matplotlib.pyplot as plt
# from pandas.core import datetools

from Utilities.config import *
from Utilities.Database_funcs import *

import warnings
warnings.filterwarnings("ignore")

# plt.style.available
plt.style.use("seaborn-blackgrid")

print('Prophet %s' % fbprophet.__version__)



class FBProphet(object):

    def __init__(self):
            
        print("|-------------------------------------------|")
        print("|Facebook Prophet model has been initialized|")
        print("|-------------------------------------------|")

    pass


    def Prophet_model(self, data):
    
        self.data = data

        self.data = self.data.drop(['open', 'high', 'low','volume', 'id', 'crypto_id'], axis=1)
        self.data.rename(columns={'close': 'y', 'date': 'ds'}, inplace=True)
        
        
        m = Prophet()

        m.fit(self.data)

        # Create Future dates
        future_prices = m.make_future_dataframe(periods=20,freq='min', include_history=True) # freq : 'day', 'week', 'month', 'quarter', 'year', 1(1 sec), 60(1 minute) or 3600(1 hour)

        # Predict Prices
        forecast = m.predict(future_prices)
        forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()


        # TODO // Include hyperparameter tuning

        # param_grid = {  'growth': ["linear"], 
        #         'changepoints': [None], 
        #         'n_changepoints': [25, 50, 75], 
        #         'changepoint_range': [0.25, 0.5, 0.75],
        #         'yearly_seasonality': ["auto"],
        #         'weekly_seasonality': ["auto"],
        #         'daily_seasonality': [False],
        #         'seasonality_mode': ["additive"],
        #         'seasonality_prior_scale': [10, 50, 100],
        #         'holidays_prior_scale': [10, 50, 100],
        #         'changepoint_prior_scale': [0.1, 0.33, 0.66],
        #         'mcmc_samples': [0],
        #         'interval_width': [0.25, 0.5, 0.75],
        #         'uncertainty_samples': [0]
        #       }

        return forecast

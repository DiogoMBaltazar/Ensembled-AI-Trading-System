import sys

sys.path.insert(0, r'F:\Ensembled-AI-Trading-System')

import numpy as np
import pandas as pd 
from Utilities.config import *
from sklearn.preprocessing import *
from sklearn.decomposition import *
from sklearn.model_selection import *
from Utilities.Database_funcs import *


class PCA_class(object):

    def __init__(self):
    
        print("|-------------------------------|")
        print("|PCA Engine has been initialized|")
        print("|-------------------------------|")

        pass

    def pca(self, data):

        self.data = data

        self.close = data['close'] 
        self.date = data['date'] 
        self.crypto_id = data['date'] 

        self.data.drop(columns=['id', 'crypto_id', 'date'], inplace=True)

        # This dropna might be dangerous.
        self.data = self.data.dropna()
        print(self.data.head(4))

        self.scaler = MinMaxScaler(feature_range=(0, 1))
        
        self.scaler = self.scaler.fit(self.data)
        self.normalized = self.scaler.transform(self.data)

        self.pca = PCA(0.9).fit(self.normalized)

        self.new_normalized = pd.DataFrame(self.pca.transform(self.normalized))

        n_pcs= self.pca.n_components_ # get number of component
        
        # get the most important feature names
        
        # https://stackoverflow.com/questions/22984335/recovering-features-names-of-explained-variance-ratio-in-pca-with-sklearn
        initial_feature_names = self.data.columns
        most_important = [np.abs(self.pca.components_[i]).argmax() for i in range(n_pcs)]
        most_important_names = [initial_feature_names[most_important[i]] for i in range(n_pcs)]
        
        dic = {'PC{}'.format(i+1): most_important_names[i] for i in range(n_pcs)}
        df = pd.DataFrame(sorted(dic.items()))

        print("The important features are the ones that influence more the components and thus, \nHave a large absolute value/coefficient/loading on the component.:", df)
        print("|------------------------------------------------------------------------|")
        print("|------------------------------------------------------------------------|")

        #column names for new reduced dataframe
        self.new_normalized.columns = most_important_names

        self.new_normalized['date'] = self.date
        self.new_normalized['close'] = self.close
        self.new_normalized['crypto_id'] = self.crypto_id

        self.new_normalized = self.new_normalized.loc[:,~self.new_normalized.columns.duplicated()]
        print(f"Initial dataframe shape {self.data.shape} --> After PCA: {self.new_normalized.shape}")
        print("|-----------------------------------------------------------|")

        return self.new_normalized
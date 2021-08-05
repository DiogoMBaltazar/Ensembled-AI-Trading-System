import sys
sys.path.insert(0, r'F:\Tese')

import time
import warnings
import datetime
import numpy as np
import pandas as pd
from datetime import date
from ta.utils import *
from ta import add_all_ta_features
from Utilities.Database_funcs import *
warnings.filterwarnings("ignore")
# import datatable as dt # super faster alternative to pandas 


class FeatureEngineering(object):

    def __init__(self):

        print("|-----------------------------------------------|")
        print("|Technical Indicator Engine has been initialized|")
        print("|-----------------------------------------------|")

        pass

    def log_returns(self, data):

        data['log_returns'] = (np.log(data.close / data.close.shift(-1)) )

        return data

    def handling_ohlcv_and_TA_indicators(self, data):
        """Computes over 90 technical indicators"""


        output = data.drop_duplicates()
        output = dropna(output)


        # converting column types
        for col in ['open', 'high', 'low', 'close', 'volume']:
            output[col] = output[col].astype("float")

        # Adds over 83 technical indicators
        output = add_all_ta_features(df=output, open='open', high='high', low='low', close='close', volume='volume', fillna=True)

        return output



    def calculate_volatility(self, output):

        # output['vol'] = np.std(output['log_returns'])
        # other implementaion way using pandas rolling std function to ease computation, 
        # 5 mins for now
        output['vol'] = output['log_returns'].rolling(window=5).std() * np.sqrt(5)


        # annualized daily vol (252 trading days)
        # vol = output['vol'] * 252 ** 0.5

        return output


    def more_features(self, output):


        # Needs adjustment acording data granularity
        output['Cumulative_return_100'] = ((output['close'] / output['close'].iloc[0]) - 1) * 100
        output['Daily_return_100'] = ((output['close'] / output['close'].shift(1)) - 1) * 100
        output['High-low'] = output['high'] - output['low']
        output['Close-open'] = output['close'] - output['open']

        output['avg_vol_5_bar'] = output['volume'].rolling(window=5).mean()
        output['avg_vol_10_bar'] = output['volume'].rolling(window=10).mean()
        output['avg_vol_50_bar'] = output['volume'].rolling(window=50).mean()
        output['avg_vol_100_bar'] = output['volume'].rolling(window=100).mean()

        return output

import sys
sys.path.insert(0, r'F:\Ensembled-AI-Trading-System')

import warnings
import numpy as np
import pandas as pd
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

        # Needs adjustment according data granularity
        output['Cumulative_return_100'] = ((output['close'] / output['close'].iloc[0]) - 1) * 100
        output['Daily_return_100'] = ((output['close'] / output['close'].shift(1)) - 1) * 100
        output['High-low'] = output['high'] - output['low']
        output['Close-open'] = output['close'] - output['open']

        output['avg_vol_5_bar'] = output['volume'].rolling(window=5).mean()
        output['avg_vol_10_bar'] = output['volume'].rolling(window=10).mean()
        output['avg_vol_50_bar'] = output['volume'].rolling(window=50).mean()
        output['avg_vol_100_bar'] = output['volume'].rolling(window=100).mean()

        return output


    def volume(self, output):


        # for 1 min tick data
        output['15 min volume'] = output['volume'].rolling(window=15).sum()
        output['30 min volume'] = output['volume'].rolling(window=30).sum()
        output['60 min volume'] = output['volume'].rolling(window=60).sum()
        output['6 hr volume'] = output['volume'].rolling(window=360).sum()
        output['12 hr volume'] = output['volume'].rolling(window=720).sum()
        output['24 hr volume'] = output['volume'].rolling(window=1440).sum()


    def NLP_Features(self, data):

        df = pd.read_csv(r'F:\Ensembled-AI-Trading-System\data\Sentiment_Analysis_date.csv')

        # sentiments = df[['date, symbol, sentiment']]

        

        print(df.columns)


    def fourier_transformation(self, data):

        # https://github.com/manganganath/stock_price_trend_fft

        close_fft = np.fft.fft(np.asarray(data['Close'].tolist()))
        fft_df = pd.DataFrame({'fft':close_fft})
        fft_df['absolute'] = fft_df['fft'].apply(lambda x: np.abs(x))
        fft_df['angle'] = fft_df['fft'].apply(lambda x: np.angle(x))


        # Low pass filtering 
        # take only 200 components

        fft_list = np.asarray(fft_df['fft'].tolist())
        fft_list[100:-100] = 0

        return fft_list

# # calculate the volume in coin from QUANTITY in USDT (default)
# volume = float(quantity / float(last_price))


# average buying price from bithumb.com – you can call fetch_my_trades, 
# filter the trades by the side (buy/sell) 
# and then aggregate 
# and divide them by the sum of their volumes.



# log_ret_dif = crypto_data['log_returns'] > crypto_data['log_returns'].shift(1)

# if log_ret_dif > 10% std of normal distribution of all log_returns:
#     df['target'] = 'buy'
# elif 10% < log_ret_dif < 25%:
#     df['target'] = 'hold'
# else:
#     df['target'] = 'sell'


# https://github.com/ThirstyScholar/trading-bitcoin-with-reinforcement-learning/blob/master/frl/data.py
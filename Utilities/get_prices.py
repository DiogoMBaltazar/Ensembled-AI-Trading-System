import sys
sys.path.insert(0, r'F:\Ensembled-AI-Trading-System')

import sys, os
import datetime
import numpy as np
from ib_insync import IB, Stock, util
from tqdm import trange
from Utilities.config import *
from Utilities.Database_funcs import *
from autogluon.core.decorator import obj

begin_time = datetime.datetime.now()

# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__

LOCAL_TZ = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo

Crypto_DB = Crypto_Database()
Stocks_DB = Stocks_Database()

class get_crypto_prices(object):

    def __init__(self):
    
        print("|------------------------------------------|")
        print("| Crypto Prices engine has been initialized|")
        print("|------------------------------------------|")

        pass
        
    def get_prices(self):

        self.crypto_pairs = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'DOGE/USDT', 'TRX/USDT', 
                             'XRP/USDT', 'ADA/USDT', 'FTT/USDT', 'SRM/USDT',  'BNB/USDT']
        
        self.crypto_data = Crypto_DB.insert_ohlcv(self.crypto_pairs)
        
        end_time = datetime.datetime.now() - begin_time

        print('\033[94m' + f'This query took %s', end_time, "seconds to run")



# Remember, that you need TWS running to be able to run the system. 
class get_stocks_data(object):

    def __init__(self):

        print("|-----------------------------------------|")
        print("| Stock Prices engine has been initialized|")
        print("|-----------------------------------------|")

        pass


    def _fetch_to_df(ib, symbol, exchange, end_datetime, duration, bar_size):
        
        print(f'Downloading historical data of {symbol} for {duration} '
                f'with {bar_size} resolution')


        symbols = Stocks_DB.get_symbols()

        exchange = 'SMART' # or ISK

        bar_size = "1m"

        end_datetime = datetime.time(datetime.now())

        # duration

        for symbol in symbols:

            contract = Stock(symbol, exchange=exchange, currency='USD')
        
            # takes contract, end_datetime, duration, bar_size
            Stocks_DB.insert_ohlcv(contract)

            end_time = datetime.datetime.now() - begin_time

        print('\033[94m' + f'This query took %s', end_time, "seconds to run")


# A = get_crypto_prices()        

# A.get_prices()
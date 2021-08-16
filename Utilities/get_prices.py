import sys
sys.path.insert(0, r'F:\Ensembled-AI-Trading-System')

import sqlite3
import sys, os
import datetime
import numpy as np
from ib_insync import *
from tqdm import trange
from Utilities.config import *
from Utilities.Database_funcs import *

begin_time = datetime.datetime.now()

# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__


Crypto_DB = Crypto_Database()

class get_crypto_prices(object):

    def __init__(self):

        self.connection = sqlite3.connect(MAIN_CRYPTOS_DB_FILE)
        self.connection.row_factory = sqlite3.Row

        self.cursorCryptos = self.connection.cursor()
        
    def get_prices(self):

        self.crypto_pairs = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'DOGE/USDT', 'TRX/USDT', 
                             'XRP/USDT', 'ADA/USDT', 'FTT/USDT', 'SRM/USDT',  'BNB/USDT']
        
        self.crypto_data = Crypto_DB.insert_ohlcv(self.crypto_pairs)
        
        end_time = datetime.datetime.now() - begin_time

        print('\033[94m' + f'This query took %s', end_time, "seconds to run")

A = get_crypto_prices()        

A.get_prices()
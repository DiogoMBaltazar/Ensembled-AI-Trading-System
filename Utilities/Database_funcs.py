import sys
sys.path.insert(0, r'F:\Ensembled-AI-Trading-System')

import sqlite3
import datetime
import numpy as np 
from tqdm import tqdm
from tqdm import trange
from pandas import DataFrame
from Utilities.config import *

class Crypto_Database(object):

    """sqlite3 database class that holds common helpful functions"""
    DB_LOCATION = MAIN_CRYPTOS_DB_FILE # TODO // set this to be dynamic

    # MAIN CRYPTOS IS SET AS STANDARD
    def __init__(self):
        """Initialize db class variables"""
        
        self.DB_LOCATION = MAIN_CRYPTOS_DB_FILE # TODO // set this to be dynamic
        self.connection = sqlite3.connect(self.DB_LOCATION)
        self.connection.row_factory = sqlite3.Row
        self.cursorCryptos = self.connection.cursor()
        print(self.connection)

        print(self.cursorCryptos)

    def close(self):
        """close sqlite3 connection"""
        self.connection.close()

    def execute(self, new_data):
        """execute a row of data to current cursor"""
        self.cursorCryptos.execute(new_data)

    def commit(self):
        """commit changes to database"""
        self.connection.commit()

    def get_crypto_tickers(self):
        self.cursorCryptos.execute("""SELECT DISTINCT symbol FROM Cryptos""")
        return [item[0] for item in self.cursorCryptos.fetchall()]

    def add_price_data(self, crypto_id, date, open, high, low, close, volume):
        
        self.crypto_id = crypto_id
        self.date = date
        self.Open = open
        self.High = high
        self.Low = low
        self.Close = close
        self.Volume = volume
        
        self.cursorCryptos.execute("""
            INSERT INTO Crypto_Prices (crypto_id, date, open, high, low, close, volume)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (crypto_id, date, open, high, low, close, volume))

    def insert_ohlcv(self,crypto_pairs):

        self.crypto_pairs = crypto_pairs 

        self.binance = binance

        limit = 5 # # tick bars


        # TODO // Fix this 2 for loops
        for pair in tqdm(self.crypto_pairs):
            
            self.pair = pair
            
            self.crypto_data = self.binance.fetch_ohlcv(self.pair, "1m", limit = limit)
            
            print("Retrieving data for:",  self.pair)

            for i in range(0, len(self.crypto_data)):
        
                self.dates = datetime.datetime.fromtimestamp(self.crypto_data[i][0] / 1000.0).strftime('%Y-%m-%d %H:%M:%S.%f')
                
                self.open_data, 
                self.high_data, 
                self.low_data, 
                self.close_data, 
                self.volume_data = self.crypto_data[i][1], self.crypto_data[i][2], self.crypto_data[i][3], self.crypto_data[i][4], self.crypto_data[i][5]
                
                self.cursorCryptos.execute("""
                    INSERT INTO Crypto_Prices (crypto_id, date, open, high, low, close, volume)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (self.pair, self.dates, self.open_data, self.high_data, self.low_data, self.close_data, self.volume_data))
            
                
                self.connection.commit()
                    
        print('\033[94m' + f"Retrieving {len(self.crypto_data)} bars from Binance")


    def delete_datapoint(self, date):
        return self.execute("""
            DELETE FROM Crypto_Prices WHERE date = ?
        """, (date))

    def get_symbol_ohlcv(self, symbol):
        
        self.symbol = symbol
        
        self.cursorCryptos.execute("""
            SELECT * FROM Crypto_Prices 
            WHERE crypto_id = ?
            ORDER BY date DESC
        """, (self.symbol,))
            # LIMIT 1200

        self.data = DataFrame(self.cursorCryptos.fetchall()) 
        self.data.columns = list(map(lambda x: x[0], self.cursorCryptos.description))

        if self.data is not None: 
            print("Retrieving a DF",self.data.shape, "from SQL DB with OHLCV:")
            print("---------------------------------------------------------")
            print(self.data.head())
            return self.data
        else:
            print("There is no available data at this moment for" , {symbol})
   
   
    def symbols_ohlcv(self, symbols):
       
        # takes a list of tickers
        self.symbols = symbols

        print(self.symbols)

        self.data = DataFrame(self.cursorCryptos) 
        
        for symbol in self.symbols:
            print(symbol)
            self.cursorCryptos.execute("""
                SELECT * FROM Crypto_Prices 
                WHERE crypto_id = ? 
                ORDER BY date DESC
            """, (symbol,))

            # LIMIT 1200
            self.data = self.data.append(DataFrame(self.cursorCryptos.fetchall()))
            
            print(self.data) 
        
        self.data.columns = list(map(lambda x: x[0], self.cursorCryptos.description))

        if self.data is not None: 
            print("Retrieving a DF",self.data.shape, "from SQL DB with OHLCV:")
            print("---------------------------------------------------------")
            print(self.data.head())
            return self.data
        else:
            print("There is no available data at this moment for" , {self.symbol})


# =============================================================================================
# =============================================================================================



class Stocks_Database(object):

    def __init__(self):
        """Initialize db class variables"""
        
        DB_LOCATION = MAIN_STOCKS_DB_FILE # TODO // set this to be dynamic
        self.connection = sqlite3.connect(DB_LOCATION)
        self.connection.row_factory = sqlite3.Row
        self.cursorCryptos = self.connection.cursor()
        print(self.connection)

        print(self.cursorCryptos)

    def close(self):
        """close sqlite3 connection"""
        self.connection.close()

    def execute(self, new_data):
        """execute a row of data to current cursor"""
        self.cursorCryptos.execute(new_data)

    def commit(self):
        """commit changes to database"""
        self.connection.commit()

    def get_symbols(self):
        self.cursorCryptos.execute("""SELECT DISTINCT ticker FROM Stocks""")
        return [item[0] for item in self.cursorCryptos.fetchall()]


    def insert_ohlcv(self,stocks, end_datetime, duration, bar_size):

        self.stocks = stocks 
        self.end_datetime = end_datetime 
        self.duration = duration 
        self.bar_size = bar_size 

        # self.ib = ib

        limit = 5 # # tick bars


        # TODO // Fix this 2 for loops
        for stock in tqdm(self.stocks):
            
            self.stock = stock
  
            self.stock_data = self.ib.reqHistoricalData(
                self.stock, endDateTime=self.end_datetime, durationStr=self.duration,
                barSizeSetting=self.bar_size, whatToShow='TRADES', useRTH=True)


            print("Retrieving data for:",  self.pair)

            for i in range(0, len(self.stock_data)):
        
                self.dates = datetime.datetime.fromtimestamp(self.stock_data[i][0] / 1000.0).strftime('%Y-%m-%d %H:%M:%S.%f')
                
                self.open_data, 
                self.high_data, 
                self.low_data, 
                self.close_data, 
                self.volume_data = self.stock_data[i][1], self.stock_data[i][2], self.stock_data[i][3], self.stock_data[i][4], self.stock_data[i][5]
                
                self.cursorCryptos.execute("""
                    INSERT INTO Stock_Prices (crypto_id, date, open, high, low, close, volume)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (self.pair, self.dates, self.open_data, self.high_data, self.low_data, self.close_data, self.volume_data))
            
                
                self.connection.commit()
                    
        print('\033[94m' + f"Retrieving {len(self.stock_data)} bars from Binance")

    # def __exit__(self, ext_type, exc_value, traceback):
    #     self.cursor.close()
    #     if isinstance(exc_value, Exception):
    #         self.connection.rollback()
    #     else:
    #         self.connection.commit()
    #     self.connection.close()

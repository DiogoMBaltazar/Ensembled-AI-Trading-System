import sys
sys.path.insert(0, r'F:\Tese')

import sqlite3
import numpy as np 
from pandas import DataFrame
from Utilities.config import *

class Crypto_Database(object):

    """sqlite3 database class that holds common helpful functions"""

    # MAIN CRYPTOS IS SET AS STANDARD
    def __init__(self):
        """Initialize db class variables"""
        
        DB_LOCATION = MAIN_CRYPTOS_DB_FILE # TODO // set this to be dynamic
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

    def delete_datapoint(self, date):
        return self.execute("""
            DELETE FROM Crypto_Prices WHERE date = ?
        """, (date))

    def get_symbol_ohlcv(self, symbol):
        
        self.symbol = symbol
        # Example with dynamic symbol
        # symbol = 'RHAT'
        # cur.execute("SELECT * FROM stocks WHERE symbol = '%s'" % symbol)

        self.cursorCryptos.execute("""
            SELECT * FROM Crypto_Prices 
            WHERE crypto_id = ?
            ORDER BY date DESC
        """, (self.symbol,))

        self.data = DataFrame(self.cursorCryptos.fetchall()) 
        self.data.columns = list(map(lambda x: x[0], self.cursorCryptos.description))

        if self.data is not None: 
            print("Retrieving a DF",self.data.shape, "from SQL DB with OHLCV:")
            print("---------------------------------------------------------")
            print(self.data.head())
            return self.data
        else:
            print("There is no available data at this moment for" , {symbol})




class Equities_Database(object):

    def __init__(self):
        """Initialize db class variables"""
        
        DB_LOCATION = MAIN_EQUITIES_DB_FILE # TODO // set this to be dynamic
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

    def get_stock_tickers(self):
        self.cursorCryptos.execute("""SELECT DISTINCT ticker FROM Stocks""")
        return [item[0] for item in self.cursorCryptos.fetchall()]





import config
import sqlite3
import pandas
import csv
# import alpaca_trade_api as tradeapi
from datetime import datetime, timedelta



####################### STOCKS DBs ################################

connectionStocks = sqlite3.connect(config.MAIN_STOCKS_DB_FILE)
connectionStocks.row_factory = sqlite3.Row


cursorStocks = connectionStocks.cursor()

cursorStocks.execute("""
    CREATE TABLE IF NOT EXISTS Stocks (
        id INTEGER PRIMARY KEY, 
        symbol TEXT NOT NULL UNIQUE, 
        name TEXT NOT NULL,
        exchange TEXT,
        shortable BOOLEAN
    )
""")


cursorStocks.execute(""" 
    CREATE TABLE IF NOT EXISTS Stock_Prices (
        id INTEGER PRIMARY KEY, 
        stock_id INTEGER,
        date NOT NULL,
        open NOT NULL, 
        high NOT NULL,
        low NOT NULL, 
        close NOT NULL, 
        volume NOT NULL,
        Model1_LSTM NOT NULL,
        Model2_CNN NOT NULL,
        Model3_MLEnsemble NOT NULL,
        Model4_TA1 NOT NULL,
        Model5_TA2 NOT NULL,
        Ensemble NOT NULL,
        FOREIGN KEY (stock_id) REFERENCES Stocks (id)
    ) 
""")



####################### CRYPTOS DBs ################################

connectionCryptos = sqlite3.connect(config.MAIN_CRYPTOS_DB_FILE)
connectionCryptos.row_factory = sqlite3.Row


cursorCryptos = connectionCryptos.cursor()


cursorCryptos.execute("""
    CREATE TABLE IF NOT EXISTS Cryptos (
        id INTEGER PRIMARY KEY, 
        symbol TEXT NOT NULL UNIQUE, 
        name TEXT,
        exchange TEXT,
        shortable BOOLEAN
    )
""")

cursorCryptos.execute(""" 
    CREATE TABLE IF NOT EXISTS Crypto_Prices (
        id INTEGER PRIMARY KEY, 
        crypto_id INTEGER,
        date TEXT,
        open NOT NULL, 
        high NOT NULL,
        low NOT NULL, 
        close NOT NULL, 
        volume NOT NULL,
        FOREIGN KEY (crypto_id) REFERENCES Cryptos (id)
    )
""")

####################### FUTURES DBs ################################


connectionFutures = sqlite3.connect(config.MAIN_FUTURES_DB_FILE)

connectionFutures.row_factory = sqlite3.Row

cursorFutures = connectionFutures.cursor()

cursorFutures.execute("""
    CREATE TABLE IF NOT EXISTS Futures (
        id INTEGER PRIMARY KEY, 
        symbol TEXT NOT NULL UNIQUE, 
        name TEXT NOT NULL,
        exchange TEXT NOT NULL,
        shortable BOOLEAN NOT NULL
    )
""")


cursorFutures.execute(""" 
    CREATE TABLE IF NOT EXISTS Future_Prices (
        id INTEGER PRIMARY KEY, 
        future_id INTEGER,
        date NOT NULL,
        open NOT NULL, 
        high NOT NULL,
        low NOT NULL, 
        close NOT NULL, 
        volume NOT NULL,
        FOREIGN KEY (future_id) REFERENCES Futures (id)
    )
""")






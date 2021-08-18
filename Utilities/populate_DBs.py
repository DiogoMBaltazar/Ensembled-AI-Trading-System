import sqlite3

import csv

from ib_insync import *
import config
from config import *

from numpy import array

# from webScrapingIBSite import output

connection = sqlite3.connect(config.MAIN_STOCKS_DB_FILE)
connection.row_factory = sqlite3.Row

cursorStocks = connection.cursor()

cursorStocks.execute('''
    SELECT symbol, name FROM Stocks
''')

Stocksrows = cursorStocks.fetchall()
symbols = [row['symbol'] for row in Stocksrows]

############################ CRYPTO  #####################################


connection = sqlite3.connect(config.MAIN_CRYPTOS_DB_FILE)
connection.row_factory = sqlite3.Row

cursorCryptos = connection.cursor()

cursorCryptos.execute('''
    SELECT symbol, name FROM Cryptos
''')

rows = cursorCryptos.fetchall()
existing_symbols = [row['symbol'] for row in rows]

crypto_symbols = binance.fetch_tickers()


trading_crypto_pairs = array(list(crypto_symbols.keys()))

# print(crypto_symbols)

# CONDITION TO ONLY INSERT NEW TICKERS THAT DON'T EXIST ALREADY IN THE DB.

for key in trading_crypto_pairs:
    if key not in existing_symbols:
        print (f"Inserting new pair {key}")
        print ("-------------------------------")
        cursorCryptos.execute("INSERT INTO Cryptos (symbol) VALUES (?)", (key,))

connection.commit()

# IBPY LIST ALL US Equities ib_insync

# assets = csv.reader(open("./Utilities/ib_stocks_listings.csv", "rt"), delimiter=",")
# ticker_column, name_column = [], []

# for asset in assets:
    
#     ticker_column.append(asset[0])
#     symbols.append(asset[0])
#     name_column.append(asset[1])
    
#     ticker_column = list(set(ticker_column))
#     name_column =  list(set(name_column))
    
#     for ticker_stock, name_stock in zip(ticker_column, name_column):
        
#         if ticker_stock not in symbols:
        
#             print(f"Inserting new symbol: {ticker_stock}", f" Company name: {name_stock}")
#             cursorStocks.execute("INSERT INTO Stocks (symbol, name) VALUES (?, ?)", (ticker_stock, name_stock))
        
#         else:
#             next

# connection.commit()

# symbols = ['AAPL', 'TSLA'] # add your 3k symbols
# contracts = [Stock(symbol, 'SMART', 'USD') for symbol in symbols]
# tickers = ib.reqTickers(*contracts)
# for ticker in tickers:
#   print(ticker.contract.symbol, ticker.bid, ticker,ask)

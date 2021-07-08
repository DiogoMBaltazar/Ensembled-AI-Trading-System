import os
import ccxt
from ib_insync import *

API_URL = 'https://paper-api.alpaca.markets'
API_KEY = 'PKW78ICK22FQRW32K2UZ'
SECRET_KEY = '6LWnqjH154PS9VoTrImaAF0dFjjQBcRCurcaLwzC'

MAIN_STOCKS_DB_FILE = r"C:\Users\User\Desktop\Tese_Desktop\Databases\Stocks.db"
MAIN_CRYPTOS_DB_FILE = r"C:\Users\User\Desktop\Tese_Desktop\Databases\Cryptos.db"
MAIN_FUTURES_DB_FILE = r"C:\Users\User\Desktop\Tese_Desktop\Databases\Futures.db"
# CRYPTOS_PRICES_FILE = r"C:\Users\User\Desktop\Tese_Desktop\Databases\Cryptos_Prices.db"
# TECH_DB_FILE = r"C:\Users\User\Desktop\Tese\Databases\Main.db"


# To receive trade notifications by e-mail
EMAIL_ADDRESS = ''
EMAIL_PASSWORD = ''
EMAIL_HOST = ''
EMAIL_PORT = 465



# IB config, TWS OR IB GATEWAYS NEEDS TO BE OPEN

# ib = IB()
# ib.connect('127.0.0.1', 7497, clientId=1)


# Configure at least 3 exchanges: Binance, Kraken & Bitmex

bitmex   = ccxt.bitmex({  
    'apiKey': 'YOUR_PUBLIC_API_KEY',
    'secret': 'YOUR_SECRET_PRIVATE_KEY'
})

kraken = ccxt.kraken({
    'apiKey': 'YOUR_PUBLIC_API_KEY',
    'secret': 'YOUR_SECRET_PRIVATE_KEY',
})

binance = ccxt.binance({
    'apiKey': '',
    'secret': '',
})

# symbols = binance.fetch_tickers()

# markets = binance.load_markets()
# print(markets)
# tickers = binance.fetch_tickers()
# print(tickers[1])
# result = {}
# for i in range(0, len(tickers)):
#     ticker = tickers[i]
#     id = ticker['symbol']
#     if id in binance.markets_by_id:
#         market = binance.markets_by_id[id]
#         symbol = market['symbol']
#         result[symbol] = binance.parse_ticker(ticker, market)
# print (result)
import os
import ccxt
from ib_insync import *

API_URL = 'https://paper-api.alpaca.markets'
API_KEY = ''
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
    'apiKey': '',
    'secret': ''
})

kraken = ccxt.kraken({
    'apiKey': '',
    'secret': '',
})

binance = ccxt.binance({
    'apiKey': '',
    'secret': '',
})


# Reddit Auth

reddit_api = praw.Reddit(
  client_id = "",
  client_secret = "",
  user_agent = ""
)


# Twitter Auth

CONSUMER_KEY = ""
CONSUMER_SECRET = ""
ACCESS_TOKEN = ""
ACCESS_TOKEN_SECRET = ""

# Authenticate to Twitter
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# Create API object
twitter_api = tweepy.API(auth)

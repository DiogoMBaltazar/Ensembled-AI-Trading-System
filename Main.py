import sys
sys.path.insert(0, r'F:\Ensembled-AI-Trading-System')

from Strategies.PCA import *
from Utilities.config import *
from Utilities.Database_funcs import *
from Strategies.FeatureEngineering import *

def system_start():

    Crypto_DB = Crypto_Database()

    Features = FeatureEngineering()

    pca_model = PCA_class()

    crypto_data = Crypto_DB.get_symbol_ohlcv("ETH/USDT")
    crypto_data = Features.handling_ohlcv_and_TA_indicators(crypto_data)
    crypto_data = Features.log_returns(crypto_data)
    crypto_data = Features.calculate_volatility(crypto_data)
    crypto_data = Features.more_features(crypto_data)

    crypto_data = pca_model.pca(crypto_data)

    print(crypto_data)

system_start()
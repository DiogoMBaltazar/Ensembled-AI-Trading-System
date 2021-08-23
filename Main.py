import sys
sys.path.insert(0, r'F:\Ensembled-AI-Trading-System')

from Strategies.PCA import *
from Utilities.config import *
from Utilities.util_funcs import *
from Strategies.AutoGluon import *
from Strategies.RandomForest import *
from Utilities.Database_funcs import *
from Strategies.FeatureEngineering import *
from Strategies.Facebook_Prophet import FBProphet

begin_time = datetime.datetime.now()

def system_start():

    Crypto_DB = Crypto_Database()

    Features = FeatureEngineering()

    pca_model = PCA_class()

<<<<<<< HEAD
    RF = RandomForest()

    AML = AutoML()

    FBP = FBProphet()

||||||| 0c276a3e9
=======
    AML = AutoML()
    
>>>>>>> 9e66ca23134fc58efd4da5dc0878fdb42ecb10e7
    crypto_data = Crypto_DB.get_symbol_ohlcv("ETH/USDT")
    data_01 = Features.handling_ohlcv_and_TA_indicators(crypto_data)
    data_02 = Features.log_returns(data_01)
    data_03 = Features.calculate_volatility(data_02)
    data_04 = Features.more_features(data_03)
    # crypto_data = Features.nlp_features(crypto_data)


    #ensemble the below models eventually
    data_05 = pca_model.pca(data_04)
    print(data_05.columns)
    time.sleep(15)
    data_06 = AML.AML_model(data_05)

    prophet_pred = FBP.Prophet_model(crypto_data)

    # rf = RF.rf_model(crypto_data)

    end_time = datetime.datetime.now() - begin_time
    print('\033[94m' + f'This script took %s', end_time, "seconds to run")

<<<<<<< HEAD
    return data_06, prophet_pred
||||||| 0c276a3e9
    print(crypto_data)
=======
    crypto_data = AML.AML_model(crypto_data)
    
    print(crypto_data)
>>>>>>> 9e66ca23134fc58efd4da5dc0878fdb42ecb10e7

system_start()

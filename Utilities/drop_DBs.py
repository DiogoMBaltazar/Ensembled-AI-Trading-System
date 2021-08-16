import sqlite3
import config

connection = sqlite3.connect(config.MAIN_STOCKS_DB_FILE)
    
cursor = connection.cursor()
cursor.execute("""
    DROP TABLE Stocks
""")


# cursor.execute("""
#     DROP TABLE Crypto_Prices
# """)

connection.commit()
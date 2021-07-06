import sqlite3
from config import *
import numpy as np 


class Database(object):

    """sqlite3 database class that holds common helpful functions"""
    DB_LOCATION = MAIN_CRYPTOS_DB_FILE # TODO // set this to be dynamic

    # MAIN CRYPTOS IS SET AS STANDARD
    def __init__(self, db_selected=None):
        """Initialize db class variables"""
        
        if db_selected is not None:
            self.connection = sqlite3.connect(db_selected)
        else:
            self.connection = sqlite3.connect(DB_LOCATION)
        self.cur = self.connection.cursor()

    def close(self):
        """close sqlite3 connection"""
        self.connection.close()

    def execute(self, new_data):
        """execute a row of data to current cursor"""
        self.cur.execute(new_data)

    def commit(self):
        """commit changes to database"""
        self.connection.commit()

    def get_stock_tickers(self):
        self.cur.execute("""SELECT DISTINCT ticker FROM Stocks""")
        return [item[0] for item in self.cur.fetchall()]
   
    def get_crypto_tickers(self):
        self.cur.execute("""SELECT DISTINCT crypto_id FROM Cryptos""")
        return [item[0] for item in self.cur.fetchall()]

    def add_price_data(self, crypto_id, date, open, high, low, close, volume):
        return self.execute("""
            INSERT INTO Crypto_Prices (crypto_id, date, open, high, low, close, volume)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (crypto_id, dates, open_data, high_data, low_data, close_data, volume_data))

    def delete_datapoint(self, date):
        return self.execute("DELETE FROM Crypto_Prices WHERE date=?", (date,))









    # def retrieve(self, key):
    #     cursor = self._db.execute('select * from {} where t1 = ?'.format(self._table), (key,))
    #     return dict(cursor.fetchone())

    # def executemany(self, many_new_data):
    #     """add many new data to database in one go"""
    #     self.create_table()
    #     self.cur.executemany('INSERT INTO Crypto_Prices VALUES(?, ?, ?, ?, ?)', many_new_data) # {table_name} {figures to be inserted}

    # def create_table(self):
    #     """create a database table if it does not exist already"""
    #     self.cur.execute('''CREATE TABLE IF NOT EXISTS jobs(title text, \
    #                                                         job_id integer PRIMARY KEY, 
    #                                                         company text,
    #                                                         age integer)''')
    # def __enter__(self):
    #     return self

    # def __exit__(self, ext_type, exc_value, traceback):
    #     self.cursor.close()
    #     if isinstance(exc_value, Exception):
    #         self.connection.rollback()
    #     else:
    #         self.connection.commit()
    #     self.connection.close()



# example on how to use this class:

# with Database() as db:
#     db.create_table()
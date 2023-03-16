import logging
import sys
from enum import Enum

import mariadb
import pandas as pd


class Frequency(Enum):
    FiveMinute = 1
    Hourly = 2


class MariaDB:
    MARKET_DB_NAME = 'market_data'
    TABLE_NAMES = {Frequency.FiveMinute: 'market_data_5m',
                   Frequency.Hourly: 'market_data_1h'}

    def __init__(self, host: str, port: int, user: str, pwd: str):
        self.__host = host
        self.__port = port
        self.__user = user
        self.__pwd = pwd
        logging.info(f'Connecting to {self.__host} on {self.__port}, with username {self.__user}.')
        try:
            self.__conn = mariadb.connect(
                user=self.__user,
                password=self.__pwd,
                host=self.__host,
                port=self.__port,
                database=self.MARKET_DB_NAME
            )
            self.__cursor = self.__conn.cursor()
            logging.info(f'Connection successful')
        except mariadb.Error as e:
            logging.error(f'Connection failed with error message {e}')
            sys.exit(1)

    def insert_market_data(self, market_data_df: pd.DataFrame, frequency: Frequency):
        symbols = market_data_df['symbol'].unique()
        # Insert data into the str_id table
        query = 'INSERT INTO str_id (str) VALUES (%s) ON DUPLICATE KEY UPDATE id = LAST_INSERT_ID(id);'
        self.__cursor.executemany(query, [(x,) for x in symbols])
        self.__conn.commit()
        str_read_query = 'SELECT * from str_id;'
        self.__cursor.execute(str_read_query)
        response = self.__cursor.fetchall()
        symbol_dict = {x[1]: x[0] for x in response}
        market_data_df['symbol_id'] = market_data_df['symbol'].map(symbol_dict)
        market_data = market_data_df.values
        query = 'INSERT INTO market_data (symbol_id, time, open, close, low, high, volume) VALUES (%s,%s,%s,%s,%s,%s,%s);'
        params = [(x[7], str(x[6]), x[0], x[1], x[2], x[3], x[4]) for x in market_data]
        self.__cursor.executemany(query, params)
        self.__conn.commit()

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
            self.__cur = self.__conn.cursor()
            logging.info(f'Connection successful')
        except mariadb.Error as e:
            logging.error(f'Connection failed with error message {e}')
            sys.exit(1)

    def insert_market_data(self, market_data_df: pd.DataFrame, frequency: Frequency):
        pass

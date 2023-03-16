import logging
import sys
from typing import  List, Any, Tuple

import mariadb
import pandas as pd

from database.table_register import MARIADB_MANAGER
from database.table_register import TableNames


class MariaDB:

    def __init__(self, host: str, port: int, user: str, pwd: str, database: str):
        self.__host = host
        self.__port = port
        self.__user = user
        self.__pwd = pwd
        self.__db = database
        logging.info(f'Connecting to {self.__host} on {self.__port}, with user {self.__user} to database {self.__db}')
        try:
            self.__conn = mariadb.connect(
                user=self.__user,
                password=self.__pwd,
                host=self.__host,
                port=self.__port,
                database=self.__db
            )
            self.__cursor = self.__conn.cursor()
            logging.info(f'Connection successful')
        except mariadb.Error as e:
            logging.error(f'Connection failed with error message {e}')
            sys.exit(1)

    def insert_df_into_table(self, df: pd.DataFrame, table_name: TableNames):
        if not MARIADB_MANAGER.is_valid_table(table_name):
            raise Exception(f'Table {table_name} does not exist in database')
        normalizing_details = MARIADB_MANAGER.normalizing_details(table_name)
        if normalizing_details:
            for (from_col, dest_table, dest_col) in normalizing_details:
                self.insert_new_norm_keys(df, from_col, dest_table, dest_col)
                df = self.normalize_df(df, from_col, dest_table)
        column_names = MARIADB_MANAGER.table_column_names(table_name)
        placeholders = '%s,' * len(column_names)
        query = f'INSERT INTO {table_name.name} ({",".join(column_names)}) VALUES ({placeholders[:-1]});'
        data_list = self.build_data_list(df, list(df.columns), column_names)
        self.__cursor.executemany(query, data_list)
        self.__conn.commit()

    @staticmethod
    def build_data_list(df: pd.DataFrame, df_columns: List[str], table_columns: List[str]) -> List[Tuple[Any]]:
        ret_val = list()
        df_list = df.values
        columns_map = {col: df_columns.index(col) for col in table_columns}
        for row in df_list:
            ret_val.append(tuple([row[columns_map[col]] for col in table_columns]))
        return ret_val

    def normalize_df(self, df: pd.DataFrame, from_col: str, dest_table: TableNames) -> pd.DataFrame:
        logging.info(f'About to normalize df for column {from_col} before inserting to {dest_table}')
        query = f'Select * from {dest_table.name}'
        logging.info(f'Read query is {query}')
        self.__cursor.execute(query)
        response = self.__cursor.fetchall()
        key_map = {x[1]: x[0] for x in response}
        df[from_col] = df[from_col].map(key_map)
        return df

    def insert_new_norm_keys(self, df: pd.DataFrame, from_col: str, dest_table: TableNames, dest_col: str) -> int:
        if from_col not in df.columns:
            raise Exception(f'Expecting {from_col=} in dataframe as this column should be normalized')
        unique_keys = df[from_col].unique()
        query = f'INSERT IGNORE INTO {dest_table.name} ({dest_col}) VALUES (%s)'
        logging.info(f'About to run following query {query} from insert_new_norm_keys function')
        self.__cursor.executemany(query, [(x,) for x in unique_keys])
        self.__conn.commit()
        row_count = self.__cursor.affected_rows
        logging.info(f'{row_count} rows have been affected')
        return row_count

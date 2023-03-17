import pandas as pd

from database.mariadb_connector import MariaDBConnector


class RefDB:
    def __init__(self, connector: MariaDBConnector):
        self.__connector = connector

    def save_currency_reference_data(self, exchange: str, currency_reference_data: pd.DataFrame):
        currency_reference_data['source'] = exchange

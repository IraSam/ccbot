from database.mariadb_connector import MariaDBConnector


class MktDB:
    def __init__(self, connector: MariaDBConnector):
        self.__connector = connector

    def save_market_data(self):
        pass



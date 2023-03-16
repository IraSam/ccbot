from database.table_names import TableNames
from database.tables import MariaDBTable, MariaDBTablesManager

MARIADB_MANAGER = MariaDBTablesManager()


class MarketData5mTable(MariaDBTable):
    name = TableNames.market_data_5m
    columns = ['symbol_id', 'time', 'open', 'high', 'low', 'close', 'volume']


class MarketData1hTable(MariaDBTable):
    name = TableNames.market_data_1h
    columns = ['symbol_id', 'time', 'open', 'high', 'low', 'close', 'volume']


class StrCache(MariaDBTable):
    name = TableNames.str_cache
    columns = ['id', 'str']


MARIADB_MANAGER.register_table(StrCache())
MARIADB_MANAGER.register_table(MarketData5mTable())
MARIADB_MANAGER.register_table(MarketData1hTable())

MARIADB_MANAGER.register_links(TableNames.market_data_5m, 'symbol_id', TableNames.str_cache, 'str')
MARIADB_MANAGER.register_links(TableNames.market_data_1h, 'symbol_id', TableNames.str_cache, 'str')

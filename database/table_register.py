from database.table_names import TableNames
from database.tables import MariaDBTable, MariaDBTablesManager

MARIADB_MANAGER = MariaDBTablesManager()


class MarketDataTable(MariaDBTable):
    columns = ['base_id', 'quote_id', 'time', 'open', 'high', 'low', 'close', 'volume', 'exchange_id']
    name = TableNames.na


class MarketData5mTable(MarketDataTable):
    name = TableNames.market_data_5m


class MarketData1hTable(MarketDataTable):
    name = TableNames.market_data_1h


class CurrencyTable(MariaDBTable):
    name = TableNames.ref_currency
    columns = ['id', 'symbol', 'precision', 'is_stable_coin', 'is_fiat', 'black_listed']


class ExchangeTable(MariaDBTable):
    name = TableNames.ref_exchange
    columns = ['id', 'exchange']


class ActiveTradedPairs(MariaDBTable):
    name = TableNames.ref_active_traded_pairs
    columns = ['id', 'base_id', 'quote_id', 'exchange_id', 'live']


MARIADB_MANAGER.register_table(MarketData5mTable())
MARIADB_MANAGER.register_table(MarketData1hTable())
MARIADB_MANAGER.register_table(ExchangeTable())
MARIADB_MANAGER.register_table(CurrencyTable())
MARIADB_MANAGER.register_table(ActiveTradedPairs())


MARIADB_MANAGER.register_links(TableNames.market_data_5m, 'base_id', TableNames.ref_currency, 'symbol')
MARIADB_MANAGER.register_links(TableNames.market_data_5m, 'quote_id', TableNames.ref_currency, 'symbol')
MARIADB_MANAGER.register_links(TableNames.market_data_5m, 'exchange_id', TableNames.ref_exchange, 'exchange')
MARIADB_MANAGER.register_links(TableNames.market_data_1h, 'base_id', TableNames.ref_currency, 'symbol')
MARIADB_MANAGER.register_links(TableNames.market_data_1h, 'quote_id', TableNames.ref_currency, 'symbol')
MARIADB_MANAGER.register_links(TableNames.market_data_1h, 'exchange_id', TableNames.ref_exchange, 'exchange')
MARIADB_MANAGER.register_links(TableNames.ref_active_traded_pairs, 'base_id', TableNames.ref_currency, 'symbol')
MARIADB_MANAGER.register_links(TableNames.ref_active_traded_pairs, 'quote_id', TableNames.ref_currency, 'symbol')
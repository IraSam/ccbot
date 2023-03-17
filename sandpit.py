import logging
import sys

from database.mariadb_connector import MariaDBConnector
from database.table_register import TableNames
from exchange.binance import Binance
from utils.connection_info import get_connection_details

root = logging.getLogger()
root.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)


binance = Binance('zzz', 'zzz')
md_df = binance.retrieve_market_data_all_universe()

db_crd = get_connection_details('cryptodb')
mkt_db = MariaDBConnector(db_crd['host'], int(db_crd['port']), db_crd['user'], db_crd['pwd'], db_crd['db'])
mkt_db.insert_df_into_table(md_df, TableNames.market_data_5m)

import logging
import sys

from database.mariadb_connector import MariaDB
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

mkt_db_crd = get_connection_details('marketdb')
mkt_db = MariaDB(mkt_db_crd['host'], int(mkt_db_crd['port']), mkt_db_crd['user'], mkt_db_crd['pwd'], mkt_db_crd['db'])
mkt_db.insert_df_into_table(md_df, TableNames.market_data_5m)

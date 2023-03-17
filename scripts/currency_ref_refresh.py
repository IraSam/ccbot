import logging
from argparse import ArgumentParser

from database.mariadb_connector import MariaDBConnector
from database.ref_db import RefDB
from exchange.binance import Binance
from utils.connection_info import get_connection_details
from utils.logging_utils import setup_logging, create_log_filename


def refresh_currency_ref_data(database_name: str):
    binance = Binance('mktdata', 'mktdata')  # access to mktdata endpoint is not restricted
    exchange_info = binance.get_pairs_universe()
    credentials = get_connection_details(database_name)
    connector = MariaDBConnector(database_name, credentials)
    refdb = RefDB


if __name__ == '__main__':
    log_file = create_log_filename('ref_currency')
    setup_logging(logging.INFO, log_file)

    parser = ArgumentParser()
    parser.add_argument('-d', '--database_name', help='database name to store reference data for', default='cryptodb',
                        type=str)
    args = parser.parse_args()

    logging.info(f'passed arguments {args}')

    try:
        refresh_currency_ref_data(args.database_name)
    except Exception as e:
        logging.error(e)

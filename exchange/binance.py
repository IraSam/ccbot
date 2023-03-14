import logging

import pandas as pd
from binance.spot import Spot

from assets.currency_pair import CurrencyPair
from exchange.exchange import Exchange


class Binance(Exchange):
    KLINES_COL_NAMES = ['open_timestamp', 'open', 'high', 'low', 'close', 'volume', '_', '_', '_', '_', '_', '_']

    def __init__(self, api_key: str, secret_key: str):
        self.api_key = api_key
        self.secret_key = secret_key
        self.client = Spot()
        # a comment

    def get_pairs_universe(self):
        logging.info('Retrieving exchange info')
        raw_data = self.client.exchange_info()
        #logging.info(f'Received data back from exchange {raw_data}')
        pairs = [CurrencyPair(symbol['baseAsset'], symbol['quoteAsset'], symbol['baseAssetPrecision'],
                              symbol['quotePrecision'])
                 for symbol in raw_data['symbols'] if symbol['status'] == 'TRADING']
        logging.info(f'{len(pairs)} pairs in the universe')
        return pairs

    def retrieve_market_data_all_universe(self, freq: str = '5m'):
        pairs_universe = self.get_pairs_universe()
        universe = list()

        for it, pair in enumerate(pairs_universe[:10]):
            logging.info(f'Retrieving market data for {pair.symbol}. {it}/{len(pairs_universe)} ')
            kline_pairs = self.client.klines(pair.symbol, freq)
            logging.info(f'Retrieving market data for {pair.symbol} complete')
            pair_df = pd.DataFrame(kline_pairs, columns=self.KLINES_COL_NAMES)
            pair_df.drop('_', axis=1, inplace=True)
            pair_df['symbol'] = pair.symbol
            universe.append(pair_df)
        logging.info('Concatenating across all currency pairs')
        universe_df = pd.concat(universe)
        universe_df['open_time'] = pd.to_datetime(universe_df['open_timestamp'], unit='ms')
        return universe_df

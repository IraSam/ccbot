import pandas as pd
from binance.spot import Spot

from assets.currency_pair import CurrencyPair


class Binance:
    KLINES_COL_NAMES = ['open_timestamp', 'open', 'high', 'low', 'close', 'volume', '_', '_', '_', '_', '_', '_']

    def __init__(self, api_key, secret_key):
        self.api_key = api_key
        self.secret_key = secret_key
        self.client = Spot()
        # a comment

    def get_pairs_universe(self):
        raw_data = self.client.exchange_info()
        pairs = [CurrencyPair(symbol['baseAsset'], symbol['quoteAsset'], symbol['baseAssetPrecision'],
                              symbol['quotePrecision'])
                 for symbol in raw_data['symbols'] if symbol['status'] == 'TRADING']
        return pairs

    def retrieve_market_data_all_universe(self, freq='5m'):
        pairs_universe = self.get_pairs_universe()
        universe = list()

        for pair in pairs_universe[:10]:
            kline_pairs = self.client.klines(pair.symbol, freq)
            pair_df = pd.DataFrame(kline_pairs, columns=self.KLINES_COL_NAMES)
            pair_df.drop('_', axis=1, inplace=True)
            pair_df['open_time'] = pd.to_datetime(pair_df['open_timestamp'], unit='ms')
            pair_df['symbol'] = pair.symbol
            universe.append(pair_df)

        universe_df = pd.concat(universe)
        return universe_df

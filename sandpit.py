from binance.spot import Spot
from datetime import datetime
client = Spot()


from exchange.binance import Binance


binance = Binance('zzz', 'zzz')
pairs = binance.retrieve_market_data_all_universe()


# Get server timestamp
print(client.exchange_info())
server_time = datetime.fromtimestamp(client.time()['serverTime']/1000.0)
# Get klines of BTCUSDT at 1m interval
print(client.klines("BTCUSDT", "1m"))
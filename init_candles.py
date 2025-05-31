
from data_fetcher import fetch_klines, save_candles

symbols = ["ETHUSDT", "BTCUSDT"]
interval = "5m"
limit = 3000  # побольше истории

for symbol in symbols:
    df = fetch_klines(symbol, interval, limit=limit)
    if not df.empty:
        save_candles(symbol, df, interval)

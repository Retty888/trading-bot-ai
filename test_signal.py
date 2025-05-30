from data_fetcher import fetch_all_intervals
from analysis_enhanced import generate_enhanced_signals

candles = fetch_all_intervals(["BTCUSDT"], intervals=["1h"])
df = candles["BTCUSDT"]["1h"]

signal = generate_enhanced_signals(df)
print(signal)

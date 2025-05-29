
import pandas as pd

def debug_log_analysis(candles_dict, signals):
    with open("debug_log.txt", "w", encoding="utf-8") as f:
        for symbol, timeframes in candles_dict.items():
            f.write(f"Symbol: {symbol}\n")
            for tf, df in timeframes.items():
                f.write(f"  Timeframe: {tf} - {len(df)} candles\n")
                f.write(f"    Head:\n{df.head()}\n\n")
        f.write("\nGenerated Signals:\n")
        for signal in signals:
            f.write(f"{signal}\n")

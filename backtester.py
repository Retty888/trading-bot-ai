
import json
import os
import pandas as pd
from datetime import datetime
from data_fetcher import fetch_candles_for_symbol
from analysis_utils import generate_trade_ideas

TIMEFRAMES = ["15m", "30m", "1h", "2h", "4h", "1d"]
DEFAULT_SYMBOLS = ["ETHUSDT", "BTCUSDT"]

def run_backtest(symbols=DEFAULT_SYMBOLS, limit=500):
    all_results = []
    for symbol in symbols:
        print(f"[🔍] Анализируем {symbol}...")
        for tf in TIMEFRAMES:
            try:
                df = fetch_candles_for_symbol(symbol, tf, limit=limit)
                if df is None or df.empty:
                    print(f"[⚠️] Нет данных для {symbol} на таймфрейме {tf}")
                    continue
                signal = generate_trade_ideas(symbol, df)
                if signal:
                    signal["timeframe"] = tf
                    all_results.append(signal)
            except Exception as e:
                print(f"[❌] Ошибка при анализе {symbol} {tf}: {e}")
    return all_results

def save_results(results, filename="backtest_results.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

def to_dataframe(results):
    return pd.DataFrame(results)

if __name__ == "__main__":
    results = run_backtest()
    save_results(results)
    df = to_dataframe(results)
    df.to_csv("backtest_results.csv", index=False)
    print(f"[✅] Сохранено {len(results)} сигналов в backtest_results.csv")

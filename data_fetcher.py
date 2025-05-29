
import requests
import pandas as pd
from binance.client import Client
from config import BINANCE_API_KEY, BINANCE_API_SECRET

client = Client(api_key=BINANCE_API_KEY, api_secret=BINANCE_API_SECRET)

def fetch_klines(symbol, interval, limit=1000):
    try:
        klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)
        return pd.DataFrame([{
            "time": k[0],
            "open": float(k[1]),
            "high": float(k[2]),
            "low": float(k[3]),
            "close": float(k[4]),
            "volume": float(k[5])
        } for k in klines])
    except Exception as e:
        print(f"Error fetching klines for {symbol} {interval}: {e}")
        return pd.DataFrame()

def fetch_all_intervals(symbols=["ETHUSDT", "BTCUSDT"], intervals=["1m", "5m", "15m", "1h", "4h"]):
    all_data = {}
    for symbol in symbols:
        all_data[symbol] = {}
        for interval in intervals:
            df = fetch_klines(symbol, interval)
            if not df.empty:
                all_data[symbol][interval] = df
    return all_data

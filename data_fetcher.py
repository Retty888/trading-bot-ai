import requests
import pandas as pd
import os
from binance.client import Client
from config import BINANCE_API_KEY, BINANCE_API_SECRET
from utils.candle_storage import save_candles, load_candles
from datetime import datetime, timedelta

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

def fetch_candles_for_symbol(symbol, interval="5m", limit=1000):
    try:
        os.makedirs("candle_data", exist_ok=True)

        df = load_candles(symbol, interval)
        if not df.empty:
            last_time = pd.to_datetime(df['time'].max(), unit='ms')
            if datetime.utcnow() - last_time < timedelta(minutes=5):
                print(f"[📂] Используем локальные свечи для {symbol} ({interval})")
                return df.tail(limit)

        df = fetch_klines(symbol, interval, limit=limit)
        print(f"[DEBUG] Получено {len(df)} строк")
        if not df.empty:
            save_candles(symbol, df, interval)
            print(f"[🌐] Скачано и сохранено {len(df)} свечей для {symbol} ({interval})")
        else:
            print(f"[⚠️] Нет данных от Binance для {symbol} ({interval})")

        return df

    except Exception as e:
        print(f"[❌] Ошибка в fetch_candles_for_symbol: {e}")
        return pd.DataFrame()

def fetch_all_intervals(symbols=None, intervals=None):
    if symbols is None:
        symbols = ["ETHUSDT", "BTCUSDT"]
    if intervals is None:
        intervals = ["1m", "5m", "15m", "1h", "4h"]

    all_data = {}
    for symbol in symbols:
        all_data[symbol] = {}
        for interval in intervals:
            df = fetch_candles_for_symbol(symbol, interval)  # ✅ использует кэш
            if not df.empty:
                all_data[symbol][interval] = df

    for sym in all_data:
        for tf in all_data[sym]:
            df_len = len(all_data[sym][tf])
            if df_len == 0:
                print(f"[⚠️] {sym} {tf}: Данные отсутствуют!")
            elif df_len < 50:
                print(f"[⚠️] {sym} {tf}: Слишком мало данных ({df_len} строк) — индикаторы могут не работать.")
            else:
                print(f"[✅] {sym} {tf}: Загружено {df_len} строк.")

    return all_data

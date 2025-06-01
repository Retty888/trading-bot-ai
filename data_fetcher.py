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
        local_df = load_candles(symbol, interval)

        if not local_df.empty:
            last_time = pd.to_datetime(local_df['time'].max(), unit='ms')
            now = datetime.utcnow()
            delta_minutes = int((now - last_time).total_seconds() / 60)

            interval_map = {
                "1m": 1,
                "3m": 3,
                "5m": 5,
                "15m": 15,
                "30m": 30,
                "1h": 60,
                "2h": 120,
                "4h": 240,
                "6h": 360,
                "8h": 480,
                "12h": 720,
                "1d": 1440
            }

            tf_minutes = interval_map.get(interval, 5)
            missing_bars = delta_minutes // tf_minutes

            if missing_bars < 1:
                print(f"[📂] Используем актуальные локальные свечи для {symbol} ({interval})")
                return local_df.tail(limit)
            else:
                print(f"[🔄] Обнаружено {missing_bars} недостающих свечей для {symbol} ({interval})")
                new_df = fetch_klines(symbol, interval, limit=min(missing_bars + 10, 1000))
                if not new_df.empty:
                    new_df = new_df[new_df['time'] > local_df['time'].max()]
                    if not new_df.empty:
                        updated_df = pd.concat([local_df, new_df], ignore_index=True)
                        save_candles(symbol, updated_df, interval)
                        print(f"[✅] Добавлено {len(new_df)} новых свечей в {symbol} ({interval})")
                        return updated_df.tail(limit)
                return local_df.tail(limit)
        else:
            df = fetch_klines(symbol, interval, limit=limit)
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
            df = fetch_candles_for_symbol(symbol, interval)
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

# Псевдоним для совместимости со старыми импортами
def fetch_ohlcv_binance(symbol: str, timeframe="5m", limit=100):
    return fetch_candles_for_symbol(symbol, interval=timeframe, limit=limit)

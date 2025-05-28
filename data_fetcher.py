import requests
import pandas as pd
from config import BINANCE_API_BASE, PAIR, INTERVALS, LIMITS

def fetch_klines(symbol: str, interval: str, limit: int) -> pd.DataFrame:
    url = f"{BINANCE_API_BASE}/api/v3/klines"
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    df = pd.DataFrame(data, columns=[
        "timestamp", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "number_of_trades",
        "taker_buy_base_volume", "taker_buy_quote_volume", "ignore"
    ])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df.set_index("timestamp", inplace=True)
    df = df.astype({
        "open": "float",
        "high": "float",
        "low": "float",
        "close": "float",
        "volume": "float"
    })
    return df[["open", "high", "low", "close", "volume"]]

def fetch_all_intervals() -> dict:
    all_data = {}
    for label, interval in INTERVALS.items():
        print(f"📥 Загрузка данных: {label}")
        data = fetch_klines(PAIR, interval, LIMITS[label])
        all_data[label] = data
    return all_data

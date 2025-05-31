import os
import pandas as pd

DATA_DIR = "candle_data"
os.makedirs(DATA_DIR, exist_ok=True)

def get_candle_path(symbol: str, interval: str = "5m"):
    symbol = symbol.upper()
    filename = f"{symbol}_{interval}.csv"
    return os.path.join(DATA_DIR, filename)

def save_candles(symbol: str, df: pd.DataFrame, interval: str = "5m"):
    """
    Сохраняет DataFrame со свечами в файл. Перезаписывает старые данные.
    """
    path = get_candle_path(symbol, interval)
    print(f"[DEBUG] Путь сохранения: {path}")  # ← Добавь эту строку
    df.to_csv(path, index=False)
    print(f"✅ Свечи сохранены: {path}")

def load_candles(symbol: str, interval: str = "5m") -> pd.DataFrame:
    path = get_candle_path(symbol, interval)
    if os.path.exists(path):
        try:
            df = pd.read_csv(path, dtype={"time": "int64"})  # ← вот это важно!
            print(f"📥 Свечи загружены: {path}")
            return df
        except Exception as e:
            print(f"❌ Ошибка при загрузке {path}: {e}")
            return pd.DataFrame()
    else:
        print(f"⚠️ Файл не найден: {path}")
        return pd.DataFrame()

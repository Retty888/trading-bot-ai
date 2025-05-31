import pandas as pd
import os
from utils.candle_storage import load_candles
from datetime import datetime, timedelta

LOG_DIR = "logs"
SIGNAL_LOG = os.path.join(LOG_DIR, "signal_log.csv")
os.makedirs(LOG_DIR, exist_ok=True)  # убедимся, что папка есть

def evaluate_signal(row, candles):
    direction = row['direction']
    entry = float(row['entry'])
    sl = float(row['stop_loss'])
    tp = float(row['take_profit'])

    for _, candle in candles.iterrows():
        high = candle['high']
        low = candle['low']

        if direction == "Long":
            if low <= sl:
                return "SL"
            if high >= tp:
                return "TP"
        elif direction == "Short":
            if high >= sl:
                return "SL"
            if low <= tp:
                return "TP"

    return "Active"

def evaluate_all_signals():
    try:
        df = pd.read_csv(SIGNAL_LOG)

        # Устанавливаем статус Unknown, если он отсутствует или пуст
        if 'status' not in df.columns:
            df['status'] = "Unknown"
        else:
            df['status'] = df['status'].fillna("Unknown").replace("", "Unknown")

        for i, row in df.iterrows():
            if row['status'] != "Unknown":
                continue

            symbol = row['symbol']
            interval = "5m"
            candles = load_candles(symbol, interval)
            if candles.empty:
                print(f"[⚠️] Нет свечей для {symbol}, оценка пропущена")
                continue

            status = evaluate_signal(row, candles)
            df.at[i, 'status'] = status
            print(f"[{symbol}] {row['direction']} @ {row['entry']} → {status}")

        df.to_csv(SIGNAL_LOG, index=False)
        print("✅ Обновление результатов сигналов завершено.")

    except Exception as e:
        print(f"❌ Ошибка при оценке сигналов: {e}")


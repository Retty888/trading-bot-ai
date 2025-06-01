import os
import csv
import pandas as pd
from utils.candle_storage import load_candles

def check_signal_result(signal: dict, df: pd.DataFrame) -> str:
    try:
        entry = float(signal["entry"])
        sl = float(signal["stop_loss"])
        tp = float(signal["take_profit"])
        direction = signal["direction"].lower()
        timeframe = signal.get("timeframe", "5m")

        timestamp_raw = signal.get("timestamp") or signal.get("entry_time")
        timestamp = pd.to_datetime(timestamp_raw, errors="coerce")

        if pd.isna(timestamp):
            return "unknown"

        df = df.copy()
        df['time'] = pd.to_datetime(df['time'], unit='ms', errors="coerce")
        df = df[df['time'] >= timestamp]

        for _, row in df.iterrows():
            high, low = row['high'], row['low']
            if direction == "long":
                if low <= sl:
                    return "SL"
                if high >= tp:
                    return "TP"
            elif direction == "short":
                if high >= sl:
                    return "SL"
                if low <= tp:
                    return "TP"

        if not df.empty:
            last_close = df.iloc[-1]['close']
            if (direction == "long" and last_close < entry) or (direction == "short" and last_close > entry):
                return "missed"
            return "open"

        return "open"

    except Exception as e:
        print(f"[❌] Ошибка в check_signal_result: {e}")
        return "unknown"


def update_logged_results(signal_log_path="logs/signal_log.csv"):
    if not os.path.exists(signal_log_path):
        print("⚠️ Файл логов сигналов не найден.")
        return

    updated_rows, updated_count, skipped_count, empty_candle_count = [], 0, 0, 0

    with open(signal_log_path, newline='', encoding='utf-8') as csvfile:
        reader = list(csv.DictReader(csvfile))
        for row in reader:
            result_raw = str(row.get("result", "")).strip().lower()
            if result_raw in ["tp", "sl", "open", "missed"]:
                skipped_count += 1
                updated_rows.append(row)
                continue

            symbol = row.get("symbol")
            tf = row.get("timeframe", "5m")
            candles = load_candles(symbol, interval=tf)

            if candles.empty:
                print(f"[⚠️] Нет свечей: {symbol} ({tf})")
                empty_candle_count += 1
                continue

            result = check_signal_result(row, candles)
            row["result"] = result
            print(f"[📊] {symbol} ({tf}) → {result}")
            updated_rows.append(row)
            updated_count += 1

    with open(signal_log_path, "w", newline='', encoding='utf-8') as csvfile:
        fieldnames = updated_rows[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_rows)

    print("✅ Лог сигналов обновлён.")
    print(f"🧾 Обновлено: {updated_count} | Пропущено: {skipped_count} | Нет свечей: {empty_candle_count}")

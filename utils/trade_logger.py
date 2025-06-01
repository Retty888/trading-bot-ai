import csv
import os
from datetime import datetime

LOG_FILE = "logs/signal_log.csv"
FIELDS = [
    "timestamp", "symbol", "timeframe", "direction", "entry",
    "stop_loss", "take_profit", "confidence", "score",
    "signal_score", "quality_score", "weak", "result",
    "pending", "reasoning", "ai_comment"  # ✅ добавлено
]



def log_signal(data: dict):
    try:
        # Автозаполнение недостающих полей значениями по умолчанию
        for field in FIELDS:
            if field not in data:
                if field == "timestamp":
                    data[field] = datetime.utcnow().isoformat()
                elif field in ["entry", "stop_loss", "take_profit", "score", "signal_score", "quality_score"]:
                    data[field] = 0.0
                elif field in ["symbol", "timeframe", "direction", "confidence", "result"]:
                    data[field] = ""
                elif field == "weak":
                    data[field] = False

        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True) if os.path.dirname(LOG_FILE) else None

        with open(LOG_FILE, mode="a", newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=FIELDS)
            if file.tell() == 0:
                writer.writeheader()
            writer.writerow(data)

    except Exception as e:
        print(f"[❌] Ошибка при логгировании сигнала: {e}")

def get_last_signals(n=10) -> list:
    """
    Возвращает последние n сигналов из лога в виде списка словарей.
    """
    try:
        if not os.path.exists(LOG_FILE):
            return []

        with open(LOG_FILE, mode="r", encoding="utf-8") as file:
            reader = list(csv.DictReader(file))
            return reader[-n:]

    except Exception as e:
        print(f"[❌] Ошибка при чтении последних сигналов: {e}")
        return []

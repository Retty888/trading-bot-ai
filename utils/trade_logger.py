import csv
import os

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "signal_log.csv")

# Обновлённый набор полей
FIELDS = [
    "symbol",
    "direction",
    "entry",
    "stop_loss",
    "take_profit",
    "confidence",     # Просто 'High', 'Medium', 'Low'
    "score",          # Цифровая оценка: 0–10
    "reasons",        # Сокращённые теги или символы
    "status"          # TP / SL / Active / Unknown
]

# Убедимся, что папка существует
os.makedirs(LOG_DIR, exist_ok=True)

def log_signal(data: dict):
    try:
        # Добавим статус, если его нет
        if "status" not in data:
            data["status"] = "Unknown"

        with open(LOG_FILE, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDS)
            if file.tell() == 0:
                writer.writeheader()
            writer.writerow(data)

    except Exception as e:
        print(f"[❌] Ошибка при логгировании сигнала: {e}")

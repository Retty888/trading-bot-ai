import pandas as pd
import json
import os

LOG_FILE = "logs/EvaluationLog.csv"
WEIGHTS_FILE = "config/weights.json"

# === Инициализация весов по умолчанию ===
def get_default_weights():
    return {
        "ema_order": 1.0,
        "macd_signal": 1.0,
        "rsi_zone": 1.0,
        "stochrsi_zone": 1.0,
        "adx_trend": 1.0,
        "candle_pattern": 1.0,
        "volume_above_avg": 1.0,
        "rr_ratio": 1.0
    }

# === Функция для обновления весов ===
def update_score_model(log_file=LOG_FILE, weights_file=WEIGHTS_FILE):
    if not os.path.exists(log_file):
        print(f"[❌] Файл не найден: {log_file}")
        return

    df = pd.read_csv(log_file)
    if df.empty:
        print("[⚠️] Лог пустой, нечего обучать")
        return

    successful = df[df['was_profitable'] == 1]
    if successful.empty:
        print("[⚠️] Нет успешных сделок для анализа")
        return

    # === Подсчёт средней оценки успешных сигналов ===
    avg_score_success = successful['score'].mean()
    
    # Обновим веса на основе корреляции с успешностью
    corr = df.corr(numeric_only=True)
    new_weights = get_default_weights()

    for factor in new_weights:
        if factor in corr.columns and 'was_profitable' in corr.index:
            correlation = corr.at[factor, 'was_profitable']
            new_weights[factor] = round(correlation, 3)

    os.makedirs(os.path.dirname(weights_file), exist_ok=True)
    with open(weights_file, 'w') as f:
        json.dump(new_weights, f, indent=4)

    print("[✅] Обновлённые веса признаков сохранены в", weights_file)
    print(new_weights)

# === Запуск для теста ===
if __name__ == "__main__":
    update_score_model()

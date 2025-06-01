import pandas as pd
import os

SIGNAL_LOG_PATH = "logs/signal_log.csv"
STATS_OUTPUT_PATH = "logs/signal_stats.csv"

def evaluate_all_signals():
    if not os.path.exists(SIGNAL_LOG_PATH):
        return "⚠️ Лог сигналов не найден."

    df = pd.read_csv(SIGNAL_LOG_PATH)

    # Проверка обязательных колонок
    if "result" not in df.columns or "reasoning" not in df.columns:
        return "⚠️ В логах отсутствуют нужные колонки (result / reasoning)."

    # Приведение значений к единому формату
    df["result"] = df["result"].astype(str).str.upper()
    df = df[df["result"].isin(["TP", "SL"])]
    df["successful"] = df["result"] == "TP"

    # Признаки для анализа
    features = [
        "EMA", "MACD", "RSI", "ADX", "VWAP", "OBV", 
        "Supertrend", "Паттерн", "объёмной зоны"
    ]

    stats = []
    for feat in features:
        subset = df[df["reasoning"].str.contains(feat, na=False)]
        total = len(subset)
        if total == 0:
            continue
        success_rate = subset["successful"].mean()
        stats.append({
            "feature": feat,
            "signals": total,
            "success_rate": round(success_rate * 100, 2)
        })

    if not stats:
        return "⚠️ Нет данных для анализа признаков."

    stats_df = pd.DataFrame(stats)
    stats_df.sort_values(by="success_rate", ascending=False, inplace=True)

    # Сохранение CSV
    os.makedirs(os.path.dirname(STATS_OUTPUT_PATH), exist_ok=True)
    stats_df.to_csv(STATS_OUTPUT_PATH, index=False)

    # Форматированный вывод
    message_lines = ["📊 <b>Статистика признаков</b>\n"]
    for _, row in stats_df.iterrows():
        message_lines.append(
            f"• <b>{row['feature']}</b>: {row['success_rate']}% (из {row['signals']})"
        )

    return "\n".join(message_lines)

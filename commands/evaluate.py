from telegram import Update
from telegram.ext import ContextTypes
import pandas as pd
import os

SIGNAL_LOG_PATH = "logs/signal_log.csv"
STATS_OUTPUT_PATH = "logs/signal_stats.csv"

async def handle_evaluate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        result_text = evaluate_all_signals()
        await update.message.reply_text(result_text, parse_mode='HTML')
    except Exception as e:
        print(f"[❌] Ошибка в handle_evaluate: {e}")
        await update.message.reply_text("❌ Ошибка при формировании оценки признаков.")

def evaluate_all_signals():
    if not os.path.exists(SIGNAL_LOG_PATH):
        return "⚠️ Лог сигналов не найден."

    df = pd.read_csv(SIGNAL_LOG_PATH)

    if "result" not in df.columns or "reasoning" not in df.columns:
        return "⚠️ В логах отсутствуют нужные колонки."

    df["successful"] = df["result"].str.upper() == "TP"

    features = ['EMA', 'MACD', 'RSI', 'ADX', 'VWAP', 'OBV', 'Supertrend', 'Паттерн', 'объёмной зоны']
    stats = []

    for feat in features:
        subset = df[df["reasoning"].str.contains(feat, na=False)]
        total = len(subset)
        success_rate = subset["successful"].mean() if total > 0 else 0.0
        stats.append({
            "feature": feat,
            "signals": total,
            "success_rate": round(success_rate * 100, 2)
        })

    stats_df = pd.DataFrame(stats)
    stats_df.sort_values(by="success_rate", ascending=False, inplace=True)

    os.makedirs(os.path.dirname(STATS_OUTPUT_PATH), exist_ok=True)
    stats_df.to_csv(STATS_OUTPUT_PATH, index=False)

    # Текст для Telegram
    message_lines = ["📊 <b>Статистика признаков</b>\n"]
    for _, row in stats_df.iterrows():
        message_lines.append(f"• <b>{row['feature']}</b>: {row['success_rate']}% (из {row['signals']})")

    return "\n".join(message_lines)

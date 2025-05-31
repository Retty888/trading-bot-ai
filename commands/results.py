# commands/results.py
from telegram import Update
from telegram.ext import ContextTypes
from performance_evaluator import evaluate_all_signals

async def handle_results(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📊 Оцениваем результаты сигналов...")
    df = evaluate_all_signals()

    total = len(df)
    tp = (df["result"] == "TP").sum()
    sl = (df["result"] == "SL").sum()
    open_ = (df["result"] == "Open").sum()
    error = df["result"].astype(str).str.startswith("Error").sum()

    summary = (
        f"📈 Результаты анализа сигналов:\n\n"
        f"✅ TP: {tp}\n"
        f"❌ SL: {sl}\n"
        f"⏳ Открытые: {open_}\n"
        f"⚠️ Ошибки: {error}\n"
        f"📦 Всего сигналов: {total}"
    )

    await update.message.reply_text(summary)

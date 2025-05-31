from telegram import Update
from telegram.ext import ContextTypes
from performance_evaluator import evaluate_all_signals

async def handle_evaluate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        result = evaluate_all_signals()
        await update.message.reply_text(f"✅ Результаты оценены.\n\n{result}")
    except Exception as e:
        print(f"[❌] Ошибка в handle_evaluate: {e}")
        await update.message.reply_text("❌ Ошибка при оценке сигналов.")

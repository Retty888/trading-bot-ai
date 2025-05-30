from telegram import Update
from telegram.ext import ContextTypes
from analyzer import run_signals_analysis
from formatting import format_signals_vertical

async def handle_signals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        summary_line, result = run_signals_analysis()  # ⬅️ без await
        await update.message.reply_text(f"{summary_line}\n\n{result}")
    except Exception as e:
        await update.message.reply_text("❌ Ошибка при получении сигналов. Попробуйте позже.")
        print(f"Ошибка в handle_signals: {e}")

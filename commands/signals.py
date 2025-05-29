from telegram import Update
from telegram.ext import ContextTypes
from analyzer import run_signals_analysis

async def handle_signals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    summary_line, result = await run_signals_analysis()
    await update.message.reply_text(f"{summary_line}\n\n{result}")
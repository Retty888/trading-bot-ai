from telegram import Update
from telegram.ext import ContextTypes
from analyzer import run_scalp_analysis

async def handle_scalp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    summary_line, result = await run_scalp_analysis()
    await update.message.reply_text(f"{summary_line}\n\n{result}")

from telegram import Update
from telegram.ext import ContextTypes
from analyzer import run_scalp_analysis

async def handle_scalp_eth(update: Update, context: ContextTypes.DEFAULT_TYPE):
    summary_line, result = await run_scalp_analysis(symbols=["ETHUSDT"])
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{summary_line}\n\n{result}")

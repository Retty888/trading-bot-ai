from telegram import Update
from telegram.ext import ContextTypes
from news import fetch_and_format_crypto_news

async def handle_news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    news_summary = fetch_and_format_crypto_news()
    await update.message.reply_text(news_summary)
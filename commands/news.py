from telegram import Update
from telegram.ext import ContextTypes

def fetch_and_format_crypto_news():
    return "📰 Новости временно отключены."

async def handle_news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    news_summary = fetch_and_format_crypto_news()
    await update.message.reply_text(news_summary)

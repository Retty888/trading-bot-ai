
from telegram import Update
from telegram.ext import ContextTypes
from config import OPENAI_API_KEY
from utils.openai_usage import get_openai_usage

async def handle_usage(update: Update, context: ContextTypes.DEFAULT_TYPE):
    usage = get_openai_usage(api_key=OPENAI_API_KEY)
    if usage:
        total_tokens = usage.get("total_tokens", 0)
        cost_estimate = round(total_tokens * 0.00001, 4)
        await update.message.reply_text(
            f"📊 Использование OpenAI:\nТокенов: {total_tokens}\nПримерная стоимость: ${cost_estimate}"
        )
    else:
        await update.message.reply_text("⚠️ Не удалось получить данные об использовании API.")

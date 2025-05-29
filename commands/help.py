
from telegram import Update
from telegram.ext import ContextTypes

async def handle_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "📘 <b>Справка по командам</b>\n\n"
        "/start — Запуск и приветствие\n"
        "/help — Справка по командам\n"
        "/signals — 📶 Основные сигналы (коротко- и среднесрочные)\n"
        "/scalp_eth — ⚡ Скальпинг для ETH\n"
        "/scalp_sui — ⚡ Скальпинг для SUI\n"
        "/swing — 📈 Среднесрочная торговля\n"
        "/news — 📰 Последние новости\n"
        "/usage — 📊 Использование токенов OpenAI\n"
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=help_text, parse_mode="HTML")

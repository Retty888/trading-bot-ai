
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
        "/usage — 📊 Использование токенов OpenAI\n\n"

        "📊 <b>Оценка сигнала</b>:\n\n"
        "<b>Score</b> — числовая оценка сигнала (макс: 7). Учитывает:\n"
        "- Порядок EMA\n"
        "- MACD и сигнальная линия\n"
        "- RSI и StochRSI\n"
        "- Объём выше среднего\n"
        "- Сила тренда (ADX)\n"
        "- Свечной паттерн (hammer, engulfing и др.)\n\n"
        "<b>Confidence</b> — интерпретация Score:\n"
        "0 = Very Low\n"
        "1 = Low\n"
        "2 = Medium\n"
        "3 = High\n"
        "4 = Very High\n"
        "5 = Extreme\n"
        "6+ = Ultra\n"
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=help_text, parse_mode="HTML")

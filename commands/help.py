from telegram import Update
from telegram.ext import ContextTypes

async def handle_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "📘 <b>Справка по командам</b>\n\n"

        "🔹 <b>Основные команды:</b>\n"
        "/start — Запуск и приветствие\n"
        "/help — Справка по командам\n"
        "/signals — 📶 Интрадеи-сигналы BTC/ETH (таймфреймы 15m, 30m, 1h)\n"
        "/scalp_btc — ⚡ Скальпинг BTC (анализ на 5m и 15m, данные с 1m)\n"
        "/scalp_eth — ⚡ Скальпинг ETH (анализ на 5m и 15m, данные с 1m)\n"
        "/swing — 📈 Свинг-анализ (анализ на 1h, 4h, 1d)\n"

        "\n🔹 <b>Анализ и статистика:</b>\n"
        "/results — 📋 Проверка TP/SL по прошлым сигналам\n"
        "/stats — 📈 Общая статистика сигналов по результатам\n"
        "/evaluate — 🤖 AI-анализ успешности признаков сигналов\n"

        "\n🔹 <b>Служебные:</b>\n"
        "/usage — 📊 Текущее использование токенов OpenAI (если включено)\n"
        "/news — 📰 Последние крипто-новости (если подключено)\n"

        "\n📊 <b>Оценка качества сигналов</b>:\n"
        "<b>Score</b> — числовой рейтинг (0–7), учитывающий:\n"
        "• EMA и тренд\n"
        "• MACD импульс\n"
        "• RSI / StochRSI зоны\n"
        "• ADX (сила тренда)\n"
        "• Свечной паттерн (hammer, engulfing и др.)\n"
        "• Объём и зоны интереса\n\n"

        "<b>Confidence</b> — интерпретация Score:\n"
        "0 = Very Low\n"
        "1 = Low\n"
        "2 = Medium\n"
        "3 = High\n"
        "4 = Very High\n"
        "5 = Extreme\n"
        "6+ = Ultra\n"
    )

    if update.message:
        await update.message.reply_text(help_text, parse_mode='HTML')
    elif update.callback_query:
        await update.callback_query.message.reply_text(help_text, parse_mode='HTML')

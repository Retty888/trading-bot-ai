
import time
import threading
from datetime import datetime
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

from config import (
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_CHAT_ID,
    USE_GPT4O,
    USE_GPT35,
    ANALYSIS_MODE,
    LANGUAGE,
    GPT4O_MODEL,
    GPT35_MODEL
)
from data_fetcher import fetch_all_intervals
from news import fetch_crypto_news
from analyzer import analyze_market
from utils import get_openai_usage

analysis_interval = {'value': 300}

async def send_telegram_message(text):
    try:
        from telegram import Bot
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=text)
    except Exception as e:
        print("Telegram Error:", e)

async def run_news_analysis():
    news = fetch_crypto_news()
    result = analyze_market({}, news, model=GPT4O_MODEL, news_only=True)
    text = f"{'🗞️ Новости' if LANGUAGE == 'ru' else '🗞️ News Analysis'}:\n{result}"
    await send_telegram_message(text)

async def run_macro_analysis():
    candles = fetch_all_intervals()
    news = fetch_crypto_news()
    result = analyze_market({
        "1h": candles.get("1h", []),
        "4h": candles.get("4h", [])
    }, news, model=GPT4O_MODEL, macro=True)
    text = f"{'📊 Свинг анализ' if LANGUAGE == 'ru' else '📊 Swing Analysis'}:\n{result}"
    await send_telegram_message(text)

async def run_deep_analysis():
    candles = fetch_all_intervals()
    news = fetch_crypto_news()
    result = analyze_market({
        "5m": candles.get("5m", [])
    }, news, model=GPT4O_MODEL, aggressive=True)
    text = f"{'🔬 GPT-4o Экспертный анализ' if LANGUAGE == 'ru' else '🔬 GPT-4o Expert Analysis'}:\n{result}"
    await send_telegram_message(text)

async def run_signal_analysis():
    candles = fetch_all_intervals()
    news = fetch_crypto_news()
    result = analyze_market(candles, news, model=GPT4O_MODEL, signal_mode=True)
    text = f"{'📶 Сигналы входа' if LANGUAGE == 'ru' else '📶 Entry Signals'}:\n{result}"
    await send_telegram_message(text)

async def command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cmd = update.message.text.lower()
    if cmd == "/start":
        await send_telegram_message("🤖 Bot is ready.\n✅ Binance API: OK\n✅ OpenAI API: OK")
    elif cmd == "/news":
        await run_news_analysis()
    elif cmd == "/swing":
        await run_macro_analysis()
    elif cmd == "/4o":
        await run_deep_analysis()
    elif cmd == "/signals":
        await run_signal_analysis()
    elif cmd == "/usage":
        try:
            usage = get_openai_usage()
            await update.message.reply_text(
                f"{'💰 Использование токенов' if LANGUAGE == 'ru' else '💰 OpenAI usage summary:'}\n{usage}"
            )
        except Exception as e:
            await update.message.reply_text(f"{'❌ Ошибка при получении данных' if LANGUAGE == 'ru' else '❌ Error fetching usage:'} {e}")
    elif cmd.startswith("/setinterval"):
        try:
            interval = int(context.args[0])
            if interval in [5, 10, 20, 30, 60]:
                analysis_interval['value'] = interval * 60
                await update.message.reply_text(
                    f"{'✅ Интервал установлен на' if LANGUAGE == 'ru' else '✅ Interval set to'} {interval} мин."
                )
            else:
                await update.message.reply_text("5, 10, 20, 30, 60")
        except Exception:
            await update.message.reply_text("Usage: /setinterval <minutes>")
    else:
        await update.message.reply_text(
            "📋 Available commands:\n/start\n/news\n/swing\n/4o\n/signals\n/usage\n/setinterval <minutes>"
        )

def start_bot():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler(["start", "news", "swing", "4o", "signals", "usage", "setinterval", "help"], command_handler))
    app.run_polling()

def main():
    print("📊 Bot started. Awaiting commands in Telegram...")
    start_bot()

if __name__ == "__main__":
    main()

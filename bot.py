import time
import threading
from datetime import datetime
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, CallbackContext

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

bot_instance = Bot(token=TELEGRAM_BOT_TOKEN)
analysis_interval = {'value': 300}

def send_telegram_message(text):
    try:
        bot_instance.send_message(chat_id=TELEGRAM_CHAT_ID, text=text)
    except Exception as e:
        print("Telegram Error:", e)

def run_news_analysis():
    news = fetch_crypto_news()
    result = analyze_market({}, news, model=GPT4O_MODEL, news_only=True)
    text = f"{'🗞️ Новости' if LANGUAGE == 'ru' else '🗞️ News Analysis'}:\n{result}"
    send_telegram_message(text)

def run_macro_analysis():
    candles = fetch_all_intervals()
    news = fetch_crypto_news()
    result = analyze_market({
        "1h": candles.get("1h", []),
        "4h": candles.get("4h", [])
    }, news, model=GPT4O_MODEL, macro=True)
    text = f"{'📊 Свинг анализ' if LANGUAGE == 'ru' else '📊 Swing Analysis'}:\n{result}"
    send_telegram_message(text)

def run_deep_analysis():
    candles = fetch_all_intervals()
    news = fetch_crypto_news()
    result = analyze_market({
        "5m": candles.get("5m", [])
    }, news, model=GPT4O_MODEL, aggressive=True)
    text = f"{'🔬 GPT-4o Экспертный анализ' if LANGUAGE == 'ru' else '🔬 GPT-4o Expert Analysis'}:\n{result}"
    send_telegram_message(text)

def run_signal_analysis():
    candles = fetch_all_intervals()
    news = fetch_crypto_news()
    result = analyze_market(candles, news, model=GPT4O_MODEL, signal_mode=True)
    text = f"{'📶 Сигналы входа' if LANGUAGE == 'ru' else '📶 Entry Signals'}:\n{result}"
    send_telegram_message(text)

def set_interval(update: Update, context: CallbackContext):
    try:
        interval = int(context.args[0])
        if interval in [5, 10, 20, 30, 60]:
            analysis_interval['value'] = interval * 60
            update.message.reply_text(
                f"{'✅ Интервал установлен на' if LANGUAGE == 'ru' else '✅ Interval set to'} {interval} мин."
            )
        else:
            update.message.reply_text("5, 10, 20, 30, 60")
    except Exception:
        update.message.reply_text("Usage: /setinterval <minutes>")

def usage_command(update: Update, context: CallbackContext):
    try:
        usage = get_openai_usage()
        update.message.reply_text(
            f"{'💰 Использование токенов' if LANGUAGE == 'ru' else '💰 OpenAI usage summary:'}\n{usage}"
        )
    except Exception as e:
        update.message.reply_text(f"{'❌ Ошибка при получении данных' if LANGUAGE == 'ru' else '❌ Error fetching usage:'} {e}")

def command_handler(update: Update, context: CallbackContext):
    cmd = update.message.text.lower()
    if cmd == "/start":
        send_telegram_message("🤖 Bot is ready.\n✅ Binance API: OK\n✅ OpenAI API: OK")
    elif cmd == "/news":
        run_news_analysis()
    elif cmd == "/swing":
        run_macro_analysis()
    elif cmd == "/4o":
        run_deep_analysis()
    elif cmd == "/signals":
        run_signal_analysis()
    elif cmd == "/help":
        update.message.reply_text(
            "📋 Available commands:\n/start\n/news\n/swing\n/4o\n/signals\n/usage\n/setinterval <minutes>"
        )
    elif cmd == "/usage":
        usage_command(update, context)
    elif cmd.startswith("/setinterval"):
        set_interval(update, context)
    else:
        update.message.reply_text(
            "📋 Available commands:\n"
            "/start\n/news\n/swing\n/4o\n/signals\n/usage\n/setinterval <minutes>"
        )

def start_bot():
    updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler(["start", "news", "swing", "4o", "signals", "usage", "setinterval"], command_handler))
    updater.start_polling()
    print("🤖 TelegramBot started.")

def main():
    print("📊 Bot started. Awaiting commands in Telegram...")
    threading.Thread(target=start_bot).start()

if __name__ == "__main__":
    main()
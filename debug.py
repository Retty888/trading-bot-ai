
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext

TOKEN = '7543302550:AAHJWuhGuD3a3-Z_fgeWeN-iUILNz5mwdX0'

def start(update: Update, context: CallbackContext):
    update.message.reply_text("✅ Bot is running.")

def list_commands(update: Update, context: CallbackContext):
    commands = [
        "/start - Check bot status",
        "/news - News analysis",
        "/swing - Swing timeframe analysis",
        "/4o - In-depth 5m analysis (GPT-4o)",
        "/signals - Entry signals with risk profiles",
        "/usage - OpenAI token usage",
        "/setinterval <minutes> - Set auto-analysis interval",
        "/help - Show this help message"
    ]
    update.message.reply_text("\n".join(commands))

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", list_commands))
    updater.start_polling()
    print("Bot is running... Press Ctrl+C to stop.")
    updater.idle()

if __name__ == "__main__":
    main()


from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, CallbackContext

TELEGRAM_BOT_TOKEN = "7543302550:AAHJWuhGuD3a3-Z_fgeWeN-iUILNz5mwdX0"

def start(update: Update, context: CallbackContext):
    update.message.reply_text("✅ Бот работает и готов принимать команды!")

def main():
    updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    updater.start_polling()
    print("🤖 Бот запущен и готов к работе.")
    updater.idle()

if __name__ == "__main__":
    main()

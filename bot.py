from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from config import TELEGRAM_BOT_TOKEN
from commands.start import handle_start
from commands.help import handle_help
from commands.usage import handle_usage
from commands.signals import handle_signals
from commands.scalp_eth import handle_scalp_eth
from commands.scalp_sui import handle_scalp_sui
from commands.swing import handle_swing
from commands.news import handle_news

app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

app.add_handler(CommandHandler("start", handle_start))
app.add_handler(CommandHandler("help", handle_help))
app.add_handler(CommandHandler("usage", handle_usage))
app.add_handler(CommandHandler("signals", handle_signals))
app.add_handler(CommandHandler("scalp_eth", handle_scalp_eth))
app.add_handler(CommandHandler("scalp_sui", handle_scalp_sui))
app.add_handler(CommandHandler("swing", handle_swing))
app.add_handler(CommandHandler("news", handle_news))

if __name__ == "__main__":
    print("📊 Bot started. Awaiting commands in Telegram...")
    app.run_polling()
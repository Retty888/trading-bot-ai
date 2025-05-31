from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from performance_evaluator import evaluate_all_signals  # для автооценки
from dotenv import load_dotenv
import os
from telegram import Bot

load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Функция, вызываемая после запуска приложения, до polling
async def remove_webhook(app):
    await app.bot.delete_webhook(drop_pending_updates=True)
    print("✅ Webhook удалён.")

# Импорты хендлеров
from commands.start import handle_start
from commands.help import handle_help
from commands.usage import handle_usage
from commands.signals import handle_signals
from commands.scalp_eth import handle_scalp_eth
from commands.scalp_btc import handle_scalp_btc
from commands.swing import handle_swing
from commands.news import handle_news
from commands.results import handle_results  # команда /results
from commands.evaluate import handle_evaluate
from commands.stats import handle_stats  # добавь импорт

# Отладочный хендлер
async def debug_all(update, context: ContextTypes.DEFAULT_TYPE):
    print(f"[DEBUG] Получено сообщение: {update.message.text}")


def main():
    # 1. Автооценка сигналов при запуске
    try:
        print("🔍 Проверка результатов сигналов...")
        evaluate_all_signals()
        print("✅ Готово.")
    except Exception as e:
        print(f"❌ Ошибка при автооценке сигналов: {e}")

    # 2. Инициализация бота
    # app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

 # 2. Инициализация бота с удалением вебхука
    app = (
        ApplicationBuilder()
        .token(TELEGRAM_BOT_TOKEN)
        .post_init(remove_webhook)  # 👈 вот здесь
        .build()
    )

    # 3. Регистрация команд
    app.add_handler(CommandHandler("start", handle_start))
    app.add_handler(CommandHandler("help", handle_help))
    app.add_handler(CommandHandler("usage", handle_usage))
    app.add_handler(CommandHandler("signals", handle_signals))
    app.add_handler(CommandHandler("scalp_eth", handle_scalp_eth))
    app.add_handler(CommandHandler("scalp_btc", handle_scalp_btc))
    app.add_handler(CommandHandler("swing", handle_swing))
    app.add_handler(CommandHandler("news", handle_news))
    app.add_handler(CommandHandler("results", handle_results))  # результативность
    app.add_handler(CommandHandler("evaluate", handle_evaluate))
    app.add_handler(CommandHandler("stats", handle_stats))  # добавь после других команд
            
    # 4. Отладка — любой текст
    app.add_handler(MessageHandler(filters.ALL, debug_all))

    print("📊 Bot started. Awaiting commands in Telegram...")
    app.run_polling()


if __name__ == "__main__":
    main()

from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from performance_evaluator import evaluate_all_signals  # для автооценки
from dotenv import load_dotenv
import os
from telegram import Bot
from utils.signal_result_checker import update_logged_results

# 1. Загрузка токена
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# 2. Webhook удаление
async def remove_webhook(app):
    await app.bot.delete_webhook(drop_pending_updates=True)
    print("✅ Webhook удалён.")

# 3. Импорты хендлеров
from commands.start import handle_start
from commands.help import handle_help
from commands.usage import handle_usage
from commands.signals import handle_signals
from commands.scalp_eth import handle_scalp_eth
from commands.scalp_btc import handle_scalp_btc
from commands.swing import handle_swing
from commands.news import handle_news
from commands.results import handle_results
from commands.evaluate import handle_evaluate
from commands.stats import handle_stats
from commands.altcoin_gem import handle_altcoin_gem

# 4. Отладочный хендлер
async def debug_all(update, context: ContextTypes.DEFAULT_TYPE):
    print(f"[DEBUG] Получено сообщение: {update.message.text}")


def main():
    # 🔁 1. Обновление результатов сигналов
    try:
        print("🔁 Обновление статусов сигналов (TP/SL)...")
        update_logged_results()
        print("✅ Лог сигналов обновлён.")
    except Exception as e:
        print(f"❌ Ошибка при update_logged_results: {e}")

    # 🔍 2. Автоматическая оценка при запуске
    try:
        print("🔍 Проверка результатов сигналов (AI)...")
        evaluate_all_signals()
        print("✅ Оценка завершена.")
    except Exception as e:
        print(f"❌ Ошибка при evaluate_all_signals: {e}")

    # 🤖 3. Инициализация Telegram-бота
    app = (
        ApplicationBuilder()
        .token(TELEGRAM_BOT_TOKEN)
        .post_init(remove_webhook)
        .build()
    )

    # ✅ 4. Регистрация команд
    app.add_handler(CommandHandler("start", handle_start))
    app.add_handler(CommandHandler("help", handle_help))
    app.add_handler(CommandHandler("usage", handle_usage))
    app.add_handler(CommandHandler("signals", handle_signals))
    app.add_handler(CommandHandler("scalp_eth", handle_scalp_eth))
    app.add_handler(CommandHandler("scalp_btc", handle_scalp_btc))
    app.add_handler(CommandHandler("swing", handle_swing))
    app.add_handler(CommandHandler("news", handle_news))
    app.add_handler(CommandHandler("results", handle_results))
    app.add_handler(CommandHandler("evaluate", handle_evaluate))
    app.add_handler(CommandHandler("stats", handle_stats))
    app.add_handler(CommandHandler("altcoin_gem", handle_altcoin_gem))
    app.add_handler(MessageHandler(filters.ALL, debug_all))

    print("📊 Bot started. Awaiting commands in Telegram...")
    app.run_polling()


if __name__ == "__main__":
    main()

from telegram import Update
from telegram.ext import ContextTypes
from analyzer import run_signals_analysis
from formatting import format_signals_vertical

# 🧠 Команда /signals — intraday сигналы (15m, 30m, 1h)
async def handle_signals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        args = context.args
        default_symbols = ["BTCUSDT", "ETHUSDT"]

        if args:
            symbols = [arg.upper() for arg in args if arg.upper() not in ["15M", "30M", "1H"]]
            if not symbols:
                symbols = default_symbols
        else:
            symbols = default_symbols

        # intervals теперь задаются автоматически внутри run_signals_analysis
        summary_line, signals = await run_signals_analysis(symbols=symbols)
        print("DEBUG run_signals_analysis returned:", summary_line, signals)

        signals = [s for s in signals if s]
        if not signals:
            await update.message.reply_text("⚠️ Сигналы не найдены.")
            return

        formatted_message = format_signals_vertical(signals)
        await update.message.reply_text(formatted_message, parse_mode="HTML")

    except Exception as e:
        print(f"[❌] Ошибка в handle_signals: {e}")
        await update.message.reply_text("❌ Ошибка при получении сигналов.")

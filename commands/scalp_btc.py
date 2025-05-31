from telegram import Update
from telegram.ext import ContextTypes
from analyzer import run_scalp_analysis
from formatting import format_signals_vertical
import csv
import os
from datetime import datetime

# Основная команда для скальпинга BTC
async def handle_scalp_btc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Указываем явно нужный символ и таймфреймы
        symbol = "BTCUSDT"
        summary_line, signals = await run_scalp_analysis(symbols=[symbol])

        if not signals or all(s is None for s in signals):
            await update.message.reply_text("⚠️ Сигналы не найдены.")
            return

        signals = [s for s in signals if s is not None]
        formatted = format_signals_vertical(signals, strategy_name="скальпинг BTC")
        await update.message.reply_text(f"{summary_line}\n\n{formatted}", parse_mode="HTML")

        # === Логгирование сигналов ===
        log_path = "logs/signal_log.csv"
        os.makedirs("logs", exist_ok=True)
        log_fields = ["timestamp", "symbol", "direction", "entry", "stop_loss", "take_profit", "confidence", "score", "reasons"]

        for signal in signals:
            with open(log_path, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=log_fields)
                if file.tell() == 0:
                    writer.writeheader()
                writer.writerow({
                    "timestamp": datetime.utcnow().isoformat(),
                    "symbol": signal["symbol"],
                    "direction": signal["direction"],
                    "entry": signal["entry"],
                    "stop_loss": signal["stop_loss"],
                    "take_profit": signal["take_profit"],
                    "confidence": signal["confidence"],
                    "score": signal["score"],
                    "reasons": "; ".join(signal["reasons"]) if isinstance(signal["reasons"], list) else signal["reasons"]
                })

    except Exception as e:
        print(f"[❌] Ошибка в handle_scalp_btc: {e}")
        await update.message.reply_text("❌ Ошибка при получении BTC-сигналов.")

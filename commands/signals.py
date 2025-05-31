from telegram import Update
from telegram.ext import ContextTypes
from analyzer import run_signals_analysis
from formatting import format_signals_vertical
import csv
import os

async def handle_signals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        summary_line, signals = run_signals_analysis(symbols=["ETHUSDT", "BTCUSDT"])
        print("DEBUG run_signals_analysis returned:", summary_line, signals)

        if not signals:
            await update.message.reply_text("⚠️ Сигналы не найдены.")
            return

        signals = [s for s in signals if s is not None]
        print("DEBUG signals after filtering None:", signals)

        if not signals:
            await update.message.reply_text("⚠️ Сигналы не найдены после фильтрации.")
            return

        formatted_message = format_signals_vertical(signals)
        await update.message.reply_text(formatted_message, parse_mode="HTML")

        # === Логгирование сигналов ===
        log_path = "signal_log.csv"
        log_fields = ["timestamp", "symbol", "direction", "entry", "stop_loss", "take_profit", "confidence", "score", "reasons"]

        for signal in signals:
            with open(log_path, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=log_fields)
                if file.tell() == 0:
                    writer.writeheader()
                writer.writerow({
            "timestamp": datetime.utcnow().isoformat(),  # ← добавлено время UTC
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
        await update.message.reply_text("❌ Ошибка при получении сигналов. Попробуйте позже.")
        print(f"Ошибка в handle_signals: {e}")

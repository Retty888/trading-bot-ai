from telegram import Update
from telegram.ext import ContextTypes
from analyzer import run_scalp_analysis
from formatting import format_signals_vertical
from datetime import datetime, timedelta
import csv
import os

async def handle_scalp_eth(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        summary_line, signals = await run_scalp_analysis(symbols=["ETHUSDT"])

        if not signals or all(s is None for s in signals):
            await context.bot.send_message(chat_id=update.effective_chat.id, text="⚠️ Сигналы по ETH не найдены.")
            return

        signals = [s for s in signals if s is not None]

        formatted = format_signals_vertical(signals, strategy_name="скальпинг ETH")
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{summary_line}\n\n{formatted}", parse_mode="HTML")

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
        print(f"[❌] Ошибка в handle_scalp_eth: {e}")
        await context.bot.send_message(chat_id=update.effective_chat.id, text="❌ Ошибка при получении сигналов по ETH.")

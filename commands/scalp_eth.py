from telegram import Update
from telegram.ext import ContextTypes
from analyzer import run_scalp_analysis
from formatting import format_signals_vertical
from utils.trade_logger import log_signal
from datetime import datetime
from data_fetcher import fetch_all_intervals

# 📈 Команда /scalp_eth — скальпинг ETH на основе 5m/15m
async def handle_scalp_eth(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # ⏬ Проверка и загрузка актуальных свечей
        fetch_all_intervals(symbols=["ETHUSDT"], intervals=["1m", "5m", "15m"])

        summary_line, signals = await run_scalp_analysis(symbols=["ETHUSDT"])

        if not signals or all(s is None for s in signals):
            await context.bot.send_message(chat_id=update.effective_chat.id, text="⚠️ Сигналы по ETH не найдены.")
            return

        signals = [s for s in signals if s is not None]

        formatted = format_signals_vertical(signals, strategy_name="Скальпинг ETH")
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{summary_line}\n\n{formatted}", parse_mode="HTML")

        # ✅ Логгирование сигналов
        for signal in signals:
            signal.update({
                "timestamp": signal.get("timestamp", datetime.utcnow().isoformat()),
                "timeframe": signal.get("timeframe", "5m"),
                "signal_score": signal.get("signal_score", 4),
                "quality_score": signal.get("quality_score", 0),
                "weak": signal.get("weak", False),
                "result": signal.get("result", "")
            })
            log_signal(signal)

    except Exception as e:
        print(f"[❌] Ошибка в handle_scalp_eth: {e}")
        await context.bot.send_message(chat_id=update.effective_chat.id, text="❌ Ошибка при получении сигналов по ETH.")

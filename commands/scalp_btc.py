from telegram import Update
from telegram.ext import ContextTypes
from analyzer import run_scalp_analysis
from formatting import format_signals_vertical
from utils.trade_logger import log_signal
from data_fetcher import fetch_all_intervals
from datetime import datetime

# 📈 Команда /scalp_btc — скальпинг BTC на основе 5m/15m свечей
async def handle_scalp_btc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # 🔄 Предзагрузка необходимых таймфреймов
        fetch_all_intervals(symbols=["BTCUSDT"], intervals=["1m", "5m", "15m"])

        # 📊 Основной анализ
        summary_line, signals = await run_scalp_analysis(symbols=["BTCUSDT"])

        if not signals or all(s is None for s in signals):
            await update.message.reply_text("⚠️ Сигналы не найдены.")
            return

        signals = [s for s in signals if s is not None]
        formatted = format_signals_vertical(signals, strategy_name="Скальпинг BTC")
        await update.message.reply_text(f"{summary_line}\n\n{formatted}", parse_mode="HTML")

        # ✅ Логирование всех сигналов
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
        print(f"[❌] Ошибка в handle_scalp_btc: {e}")
        await update.message.reply_text("❌ Ошибка при получении скальпинг-сигналов.")

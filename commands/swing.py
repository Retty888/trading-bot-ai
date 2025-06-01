from telegram import Update
from telegram.ext import ContextTypes
from analyzer import run_swing_analysis
from formatting import format_signals_vertical
from utils.trade_logger import log_signal
from datetime import datetime

# 🎯 Команда /swing — сигналы для свинг-трейдинга (1h, 4h, 1d)
async def handle_swing(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        summary_line, signals = await run_swing_analysis()

        if not signals or all(s is None for s in signals):
            await update.message.reply_text("⚠️ Swing сигналы не найдены.")
            return

        signals = [s for s in signals if s is not None]

        formatted = format_signals_vertical(signals, strategy_name="Swing")
        await update.message.reply_text(f"{summary_line}\n\n{formatted}", parse_mode="HTML")

        # ✅ Логгирование в полном формате
        for signal in signals:
            signal.update({
                "timestamp": signal.get("timestamp", datetime.utcnow().isoformat()),
                "timeframe": signal.get("timeframe", "1h"),  # по умолчанию
                "signal_score": signal.get("signal_score", 4),
                "quality_score": signal.get("quality_score", 0),
                "weak": signal.get("weak", False),
                "result": signal.get("result", "")
            })
            log_signal(signal)

    except Exception as e:
        print(f"[❌] Ошибка в handle_swing: {e}")
        await update.message.reply_text("❌ Произошла ошибка при получении Swing-сигналов.")

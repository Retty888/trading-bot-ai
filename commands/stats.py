import pandas as pd
from telegram import Update
from telegram.ext import ContextTypes

SIGNAL_LOG = "logs/signal_log.csv"

async def handle_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        df = pd.read_csv(SIGNAL_LOG)

        if 'result' not in df.columns:
            await update.message.reply_text("⚠️ Колонка 'result' отсутствует в логах.")
            return

        df['result'] = df['result'].fillna("none").str.strip().str.lower()
        total = len(df)

        tp_count = (df['result'] == 'tp').sum()
        sl_count = (df['result'] == 'sl').sum()
        missed_count = (df['result'] == 'missed').sum()
        open_count = (df['result'] == 'open').sum()
        none_count = (df['result'] == 'none').sum()

        def pct(count):
            return f"{(count / total * 100):.1f}%" if total else "0.0%"

        msg = (
            f"📊 <b>Общая статистика сигналов</b>\n\n"
            f"Всего: <b>{total}</b>\n"
            f"✅ TP: {tp_count} ({pct(tp_count)})\n"
            f"❌ SL: {sl_count} ({pct(sl_count)})\n"
            f"🚫 Missed: {missed_count} ({pct(missed_count)})\n"
            f"⏳ Open: {open_count} ({pct(open_count)})\n"
            f"❓ None: {none_count} ({pct(none_count)})\n\n"
            f"<i>Источник: logs/signal_log.csv</i>"
        )

        await update.message.reply_text(msg, parse_mode='HTML')

    except Exception as e:
        print(f"[❌] Ошибка в handle_stats: {e}")
        await update.message.reply_text(f"❌ Ошибка при формировании статистики: {e}")

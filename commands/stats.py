# 📁 Файл: commands/stats.py

import pandas as pd
from telegram import Update
from telegram.ext import ContextTypes

SIGNAL_LOG = "logs/signal_log.csv"

async def handle_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        df = pd.read_csv(SIGNAL_LOG)
        if 'status' not in df.columns:
            await update.message.reply_text("⚠️ В логах нет информации о результатах сигналов.")
            return

        total = len(df)
        tp = len(df[df['status'] == 'TP'])
        sl = len(df[df['status'] == 'SL'])
        active = len(df[df['status'] == 'Active'])

        msg = f"\U0001F4CA <b>Статистика сигналов</b>\n"
        msg += f"\n<b>Всего:</b> {total} сигналов"
        msg += f"\n<b>TP:</b> {tp} ({tp/total*100:.1f}%)"
        msg += f"\n<b>SL:</b> {sl} ({sl/total*100:.1f}%)"
        msg += f"\n<b>В процессе:</b> {active} ({active/total*100:.1f}%)"

        await update.message.reply_text(msg, parse_mode='HTML')

    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка при формировании статистики: {e}")

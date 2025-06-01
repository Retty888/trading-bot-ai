from telegram import Update
from telegram.ext import ContextTypes
import pandas as pd
import os

LOG_PATH = "logs/signal_log.csv"

async def handle_results(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not os.path.exists(LOG_PATH):
        await update.message.reply_text("⚠️ Файл результатов не найден.")
        return

    try:
        df = pd.read_csv(LOG_PATH)
        if 'result' not in df.columns:
            await update.message.reply_text("⚠️ Колонка 'result' отсутствует в данных.")
            return

        df['result'] = df['result'].fillna("none").str.strip().str.lower()

        # 🔍 Фильтрация по символу
        args = context.args
        if args:
            symbol = args[0].upper()
            df = df[df['symbol'].astype(str).str.upper() == symbol]
            if df.empty:
                await update.message.reply_text(f"⚠️ Нет сигналов по {symbol}.")
                return
        else:
            symbol = None

        # 📊 Общая статистика
        tp_count = (df['result'] == 'tp').sum()
        sl_count = (df['result'] == 'sl').sum()
        missed_count = (df['result'] == 'missed').sum()
        open_count = (df['result'] == 'open').sum()
        none_count = (df['result'] == 'none').sum()
        total = len(df)

        winrate = tp_count / (tp_count + sl_count) * 100 if (tp_count + sl_count) > 0 else 0

        response = (
            f"📋 <b>Результативность сигналов</b>{f' для <code>{symbol}</code>' if symbol else ''}\n\n"
            f"Всего: <b>{total}</b>\n"
            f"✅ TP: {tp_count}\n"
            f"❌ SL: {sl_count}\n"
            f"🚫 Missed: {missed_count}\n"
            f"⏳ Open: {open_count}\n"
            f"❓ None: {none_count}\n\n"
            f"📈 Winrate: <b>{winrate:.2f}%</b>\n"
        )

        # 🕒 Последние 3 сигнала
        time_col = 'timestamp' if 'timestamp' in df.columns else 'entry_time' if 'entry_time' in df.columns else None
        if time_col:
            df['__sort_time'] = pd.to_datetime(df[time_col], errors='coerce')
            last_signals = df.dropna(subset=['__sort_time']).sort_values(by='__sort_time', ascending=False).head(3)

            response += "\n<b>📌 Последние сигналы:</b>\n"
            for _, row in last_signals.iterrows():
                ts_raw = row.get(time_col, "")
                ts = str(ts_raw)[:19].replace("T", " ")
                symbol_disp = row.get("symbol", "?")
                direction_disp = row.get("direction", "?").upper()
                result_disp = row.get("result", "?")
                response += f"• <code>{symbol_disp}</code> | {direction_disp} | {result_disp} | {ts}\n"
        else:
            response += "\n❗ Не найдено поле времени для сортировки последних сигналов."

        await update.message.reply_text(response, parse_mode="HTML")

    except Exception as e:
        print(f"[❌] Ошибка в handle_results: {e}")
        await update.message.reply_text("❌ Ошибка при обработке результатов.")

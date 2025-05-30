
import pandas as pd
import matplotlib.pyplot as plt
from data_fetcher import fetch_all_intervals
from ta.trend import EMAIndicator
from dotenv import load_dotenv
import os
import io
from telegram import Bot

# Загрузка переменных среды
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Загрузка данных
symbol = "BTCUSDT"
interval = "1h"
candles = fetch_all_intervals([symbol], intervals=[interval])
df = candles[symbol][interval]

# Скользящие средние
df["ema20"] = EMAIndicator(close=df["close"], window=20).ema_indicator()
df["ema50"] = EMAIndicator(close=df["close"], window=50).ema_indicator()
df["ema200"] = EMAIndicator(close=df["close"], window=200).ema_indicator()

# Уровни поддержки и сопротивления
df["local_max"] = df["high"][(df["high"].shift(1) < df["high"]) & (df["high"].shift(-1) < df["high"])]
df["local_min"] = df["low"][(df["low"].shift(1) > df["low"]) & (df["low"].shift(-1) > df["low"])]
resistance_levels = df["local_max"].dropna().tail(5)
support_levels = df["local_min"].dropna().tail(5)

# Визуализация
plt.figure(figsize=(12, 6))
plt.plot(df.index, df["close"], label="Close")
plt.plot(df.index, df["ema20"], label="EMA 20")
plt.plot(df.index, df["ema50"], label="EMA 50")
plt.plot(df.index, df["ema200"], label="EMA 200")

for level in resistance_levels:
    plt.axhline(level, color='red', linestyle='--', linewidth=0.7, label='Resistance')

for level in support_levels:
    plt.axhline(level, color='green', linestyle='--', linewidth=0.7, label='Support')

plt.title("BTCUSDT — Уровни и EMA")
plt.legend(loc="upper left")
plt.grid(True)
plt.tight_layout()

# Сохраняем график в память
buf = io.BytesIO()
plt.savefig(buf, format="png")
buf.seek(0)

# Отправка в Telegram
bot = Bot(token=TOKEN)
bot.send_photo(chat_id=CHAT_ID, photo=buf, caption="📊 BTCUSDT: Уровни и EMA")

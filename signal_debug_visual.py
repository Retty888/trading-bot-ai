
import pandas as pd
import matplotlib.pyplot as plt
from data_fetcher import fetch_all_intervals
from analysis_enhanced import generate_enhanced_signals

from ta.trend import EMAIndicator, MACD, ADXIndicator
from ta.momentum import RSIIndicator
from ta.volatility import AverageTrueRange

# Получаем данные
symbol = "BTCUSDT"
interval = "1h"
candles = fetch_all_intervals([symbol], intervals=[interval])
df = candles[symbol][interval]

# Индикаторы
df["ema20"] = EMAIndicator(close=df["close"], window=20).ema_indicator()
df["ema50"] = EMAIndicator(close=df["close"], window=50).ema_indicator()
df["ema200"] = EMAIndicator(close=df["close"], window=200).ema_indicator()
df["macd"] = MACD(close=df["close"]).macd()
df["macd_signal"] = MACD(close=df["close"]).macd_signal()
df["rsi"] = RSIIndicator(close=df["close"], window=14).rsi()
df["adx"] = ADXIndicator(high=df["high"], low=df["low"], close=df["close"], window=14).adx()
df["atr"] = AverageTrueRange(high=df["high"], low=df["low"], close=df["close"], window=14).average_true_range()
df["volume_sma"] = df["volume"].rolling(window=20).mean()

# Логика сигнала
signal_data = generate_enhanced_signals(df)
print("\n📌 Сигнал:", signal_data)

# Диагностика — лог отклонённых фильтров
last = df.iloc[-1]
checks = {
    "EMA uptrend": last["ema20"] > last["ema50"] > last["ema200"],
    "MACD bullish": last["macd"] > last["macd_signal"],
    "RSI < 70": last["rsi"] < 70,
    "ADX > 20": last["adx"] > 20,
    "Volume OK": last["volume"] > last["volume_sma"],
}
print("\n🔍 Диагностика условий:")
for name, passed in checks.items():
    print(f"  {'✅' if passed else '❌'} {name}")

# Визуализация
plt.figure(figsize=(12, 6))
plt.plot(df.index, df["close"], label="Close")
plt.plot(df.index, df["ema20"], label="EMA20")
plt.plot(df.index, df["ema50"], label="EMA50")
plt.plot(df.index, df["ema200"], label="EMA200")
plt.title(f"{symbol} Price and EMAs ({interval})")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

plt.figure(figsize=(12, 3))
plt.plot(df.index, df["rsi"], label="RSI")
plt.axhline(70, color="red", linestyle="--", linewidth=0.5)
plt.axhline(30, color="green", linestyle="--", linewidth=0.5)
plt.title("RSI")
plt.grid(True)
plt.tight_layout()
plt.show()

plt.figure(figsize=(12, 3))
plt.plot(df.index, df["macd"], label="MACD")
plt.plot(df.index, df["macd_signal"], label="Signal")
plt.title("MACD")
plt.grid(True)
plt.tight_layout()
plt.show()

plt.figure(figsize=(12, 3))
plt.plot(df.index, df["adx"], label="ADX")
plt.axhline(20, color="orange", linestyle="--", linewidth=0.5)
plt.title("ADX")
plt.grid(True)
plt.tight_layout()
plt.show()

buf = io.BytesIO()
plt.savefig(buf, format='png')
buf.seek(0)

bot = Bot(token="ТВОЙ_ТОКЕН")
chat_id = "ТВОЙ_CHAT_ID"
bot.send_photo(chat_id=chat_id, photo=buf, caption="📊 График с уровнями и EMA")
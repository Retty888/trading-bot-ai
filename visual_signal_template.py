
import pandas as pd
import matplotlib.pyplot as plt
from ta.trend import EMAIndicator, MACD, ADXIndicator
from ta.momentum import RSIIndicator
from ta.volatility import AverageTrueRange

# Пример данных (замени на реальные данные)
data = {
    "open": [100, 102, 104, 103, 105, 106, 108, 109, 110, 111, 110],
    "high": [102, 104, 105, 106, 107, 108, 110, 112, 113, 114, 115],
    "low": [98, 100, 103, 101, 102, 105, 107, 108, 109, 110, 108],
    "close": [101, 103, 104, 105, 106, 107, 109, 111, 112, 113, 110],
    "volume": [1000, 1500, 1300, 1400, 1600, 1700, 1800, 1900, 2000, 2100, 2200],
}
df = pd.DataFrame(data)
df['datetime'] = pd.date_range(end=pd.Timestamp.now(), periods=len(df), freq='H')
df.set_index('datetime', inplace=True)

# Индикаторы
df["ema20"] = EMAIndicator(close=df["close"], window=20).ema_indicator()
df["ema50"] = EMAIndicator(close=df["close"], window=50).ema_indicator()
df["ema200"] = EMAIndicator(close=df["close"], window=200).ema_indicator()
df["macd"] = MACD(close=df["close"]).macd()
df["macd_signal"] = MACD(close=df["close"]).macd_signal()
df["rsi"] = RSIIndicator(close=df["close"], window=14).rsi()
df["adx"] = ADXIndicator(high=df["high"], low=df["low"], close=df["close"], window=14).adx()
df["atr"] = AverageTrueRange(high=df["high"], low=df["low"], close=df["close"], window=14).average_true_range()

# Графики
plt.figure(figsize=(12, 6))
plt.plot(df.index, df["close"], label="Close")
plt.plot(df.index, df["ema20"], label="EMA 20")
plt.plot(df.index, df["ema50"], label="EMA 50")
plt.plot(df.index, df["ema200"], label="EMA 200")
plt.title("Цены и скользящие средние")
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(12, 3))
plt.plot(df.index, df["rsi"], label="RSI")
plt.axhline(70, color='red', linestyle='--', linewidth=0.5)
plt.axhline(30, color='green', linestyle='--', linewidth=0.5)
plt.title("RSI")
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(12, 3))
plt.plot(df.index, df["macd"], label="MACD")
plt.plot(df.index, df["macd_signal"], label="Signal")
plt.title("MACD")
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(12, 3))
plt.plot(df.index, df["adx"], label="ADX")
plt.axhline(20, color='orange', linestyle='--', linewidth=0.5)
plt.title("ADX")
plt.legend()
plt.grid(True)
plt.show()

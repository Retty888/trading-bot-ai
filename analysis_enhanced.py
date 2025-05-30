import pandas as pd
from ta.trend import EMAIndicator, MACD, ADXIndicator
from ta.momentum import RSIIndicator
from ta.volatility import AverageTrueRange

def generate_enhanced_signals(df):
    if df.empty or 'close' not in df.columns:
        return None

    df['ema20'] = EMAIndicator(close=df['close'], window=20).ema_indicator()
    df['ema50'] = EMAIndicator(close=df['close'], window=50).ema_indicator()
    df['ema200'] = EMAIndicator(close=df['close'], window=200).ema_indicator()
    df['rsi'] = RSIIndicator(close=df['close'], window=14).rsi()
    df['atr'] = AverageTrueRange(high=df['high'], low=df['low'], close=df['close'], window=14).average_true_range()
    macd_obj = MACD(close=df['close'])
    df['macd'] = macd_obj.macd()
    df['macd_signal'] = macd_obj.macd_signal()
    df['adx'] = ADXIndicator(high=df['high'], low=df['low'], close=df['close'], window=14).adx()
    df['volume_sma'] = df['volume'].rolling(window=20).mean()

    last = df.iloc[-1]

    signal = None
    reasons = []

    # Лонг
    if (last['ema20'] > last['ema50'] > last['ema200'] and
        last['macd'] > last['macd_signal'] and
        last['rsi'] < 70 and
        last['adx'] > 20 and
        last['volume'] > last['volume_sma']):
        signal = "LONG"
        reasons.extend(["Uptrend EMA", "MACD bullish", "RSI ok", "ADX strong", "Volume supported"])

    # Шорт
    elif (last['ema20'] < last['ema50'] < last['ema200'] and
          last['macd'] < last['macd_signal'] and
          last['rsi'] > 30 and
          last['adx'] > 20 and
          last['volume'] > last['volume_sma']):
        signal = "SHORT"
        reasons.extend(["Downtrend EMA", "MACD bearish", "RSI ok", "ADX strong", "Volume supported"])

    return {"signal": signal, "reasons": reasons, "price": last['close']}

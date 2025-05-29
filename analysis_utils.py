
import pandas as pd
import numpy as np
from ta.trend import EMAIndicator
from ta.momentum import RSIIndicator
from ta.volatility import AverageTrueRange

def generate_trade_ideas(candles_dict, scalp_mode=False):
    trade_signals = []

    for symbol, timeframes in candles_dict.items():
        seen_signals = set()
        for tf, df in timeframes.items():
            try:
                if not isinstance(df, pd.DataFrame) or df.empty or 'close' not in df.columns:
                    continue

                df['ema20'] = EMAIndicator(close=df['close'], window=20).ema_indicator()
                df['ema50'] = EMAIndicator(close=df['close'], window=50).ema_indicator()
                df['rsi'] = RSIIndicator(close=df['close'], window=14).rsi()
                df['atr'] = AverageTrueRange(high=df['high'], low=df['low'], close=df['close'], window=14).average_true_range()

                last = df.iloc[-1]
                prev = df.iloc[-2]

                direction = None
                confidence = "Low"

                if last['ema20'] > last['ema50'] and last['rsi'] < 70 and last['close'] > last['ema20']:
                    direction = "Long"
                elif last['ema20'] < last['ema50'] and last['rsi'] > 30 and last['close'] < last['ema20']:
                    direction = "Short"

                if direction:
                    price = last['close']
                    atr = max(last['atr'], price * 0.002)  # Ensure minimum ATR-based SL distance
                    sl = price - atr if direction == "Long" else price + atr
                    tp = price + atr * 2 if direction == "Long" else price - atr * 2

                    risk = "2%"
                    confidence = "Medium"
                    if last['atr'] < price * 0.005:
                        confidence = "Low"
                    if (last['ema20'] > last['ema50'] and direction == "Long") or (last['ema20'] < last['ema50'] and direction == "Short"):
                        confidence = "High"

                    entry_key = (round(price, 4), direction, tf)
                    if entry_key in seen_signals:
                        continue
                    seen_signals.add(entry_key)

                    signal = {
                        "symbol": symbol,
                        "timeframe": tf,
                        "direction": direction,
                        "entry": round(price, 4),
                        "stop_loss": round(sl, 4),
                        "take_profit": round(tp, 4),
                        "risk": risk,
                        "confidence": confidence
                    }
                    trade_signals.append(signal)

            except Exception as e:
                print(f"⚠️ Error processing {symbol} {tf}: {e}")

    return trade_signals

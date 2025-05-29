
import pandas as pd
import numpy as np
from ta.trend import EMAIndicator
from ta.momentum import RSIIndicator
from ta.volatility import AverageTrueRange


import pandas as pd
import numpy as np
from ta.trend import EMAIndicator, MACD
from ta.momentum import RSIIndicator, StochRSIIndicator
from ta.volatility import AverageTrueRange


import pandas as pd
import numpy as np
from ta.trend import EMAIndicator, MACD
from ta.momentum import RSIIndicator, StochRSIIndicator
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

                macd_obj = MACD(close=df['close'])
                df['macd'] = macd_obj.macd()
                df['macd_signal'] = macd_obj.macd_signal()

                stoch_rsi = StochRSIIndicator(close=df['close'], window=14)
                df['stoch_rsi'] = stoch_rsi.stochrsi_k()

                last = df.iloc[-1]
                price = last['close']
                atr = max(last['atr'], price * 0.002)
                recent_window = df.iloc[-20:]
                buffer = atr * 0.5

                # Определяем направление сделки — даже если неидеальное
                long_bias = last['ema20'] > last['ema50']
                short_bias = last['ema20'] < last['ema50']

                if long_bias:
                    direction = "Long"
                    local_min = recent_window['low'].min()
                    sl = min(price - atr, local_min - buffer)
                    tp = price + (price - sl) * 1.8
                elif short_bias:
                    direction = "Short"
                    local_max = recent_window['high'].max()
                    sl = max(price + atr, local_max + buffer)
                    tp = price - (sl - price) * 1.8
                else:
                    continue  # если нет направленного тренда, пропускаем

                # Расчёт score по критериям
                score = 0
                if long_bias or short_bias:
                    score += 1
                if direction == "Long" and last['macd'] > last['macd_signal']:
                    score += 1
                if direction == "Short" and last['macd'] < last['macd_signal']:
                    score += 1
                if direction == "Long" and last['stoch_rsi'] < 0.2:
                    score += 1
                if direction == "Short" and last['stoch_rsi'] > 0.8:
                    score += 1
                if direction == "Long" and last['rsi'] < 70:
                    score += 1
                if direction == "Short" and last['rsi'] > 30:
                    score += 1

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
                    "score": score,
                    "confidence": ["Very Low", "Low", "Medium", "High", "Very High", "Extreme"][min(score, 5)]
                }
                trade_signals.append(signal)

            except Exception as e:
                print(f"⚠️ Error processing {symbol} {tf}: {e}")

    return sorted(trade_signals, key=lambda x: x['score'], reverse=True)



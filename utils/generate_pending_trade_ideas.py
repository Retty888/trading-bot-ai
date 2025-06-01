import pandas as pd
import traceback
from datetime import datetime
from ta.volatility import AverageTrueRange
from ta.volume import MFIIndicator
from data_fetcher import fetch_candles_for_symbol
from utils.trade_logger import log_signal


def determine_trend(df: pd.DataFrame, short_ema=20, long_ema=50):
    df = df.copy()
    df['ema_short'] = df['close'].ewm(span=short_ema).mean()
    df['ema_long'] = df['close'].ewm(span=long_ema).mean()
    if df['ema_short'].iloc[-1] > df['ema_long'].iloc[-1]:
        return "up"
    elif df['ema_short'].iloc[-1] < df['ema_long'].iloc[-1]:
        return "down"
    return "sideways"


def identify_support_resistance(df, lookback=100):
    highs = df['high'].tail(lookback)
    lows = df['low'].tail(lookback)
    resistance = highs.max()
    support = lows.min()
    return support, resistance


def generate_pending_trade_ideas(symbol, df):
    try:
        df = df.copy()
        df['atr'] = AverageTrueRange(df['high'], df['low'], df['close']).average_true_range()

        # Добавляем MFI вместо moneyflow
        mfi = MFIIndicator(high=df['high'], low=df['low'], close=df['close'], volume=df['volume'])
        df['mfi'] = mfi.money_flow_index()

        if df['mfi'].iloc[-1] < 40:
            return None  # слабый сигнал по объему, фильтруем

        trend_df = fetch_candles_for_symbol(symbol, interval="1h")
        trend = determine_trend(trend_df) if not trend_df.empty else "unknown"
        support, resistance = identify_support_resistance(df)

        direction = "long" if trend == "up" else "short" if trend == "down" else None
        if direction is None:
            return None

        atr = df['atr'].iloc[-1]
        buffer = 0.5 * atr

        if direction == "long":
            entry = support
            stop_loss = entry - buffer
            take_profit = entry + 3 * atr
        else:
            entry = resistance
            stop_loss = entry + buffer
            take_profit = entry - 3 * atr

        rr = abs(take_profit - entry) / abs(entry - stop_loss)
        if rr < 1.3:
            return None

        score = round(min(10, rr * 2), 2)
        confidence = "medium" if rr < 2 else "high" if rr < 3 else "very high"

        result = {
            "symbol": symbol,
            "entry": round(entry, 2),
            "stop_loss": round(stop_loss, 2),
            "take_profit": round(take_profit, 2),
            "direction": direction,
            "confidence": confidence,
            "score": score,
            "pending": True,
            "reasoning": f"Trend: {trend}, Entry from {'support' if direction == 'long' else 'resistance'} zone",
            "ai_comment": f"📌 Ждем цену у {'поддержки' if trend == 'up' else 'сопротивления'} перед входом в сторону тренда ({trend})"
        }

        log_signal({
            "timestamp": datetime.utcnow().isoformat(),
            "symbol": symbol,
            "timeframe": df.attrs.get("timeframe", "?"),
            "direction": direction,
            "entry": result["entry"],
            "stop_loss": result["stop_loss"],
            "take_profit": result["take_profit"],
            "confidence": confidence,
            "score": score,
            "signal_score": 3,
            "quality_score": round(score * 10, 2),
            "weak": True,
            "result": ""
        })
        
        return result

    except Exception as e:
        print(f"[❌] Ошибка в generate_pending_trade_ideas для {symbol}: {e}")
        traceback.print_exc()
        return None

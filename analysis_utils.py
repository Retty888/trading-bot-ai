import pandas as pd
import numpy as np
import traceback
from ta.trend import EMAIndicator, MACD, ADXIndicator
from ta.momentum import RSIIndicator
from ta.volatility import AverageTrueRange, BollingerBands
from data_fetcher import fetch_candles_for_symbol
from utils.openai_analysis import get_openai_analysis
from datetime import datetime
from utils.generate_pending_trade_ideas import generate_pending_trade_ideas
from utils.plot_signal_chart import plot_trade_signal
from utils.signal_ranker import rank_signal

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

def generate_trade_ideas(symbol, df, swing_mode=False):
    try:
        if df.attrs.get("timeframe", "") == "1m":
            print(f"[ℹ️] Пропущен сигнал по {symbol} (таймфрейм 1m).")
            return None

        df = df.copy()

        # Индикаторы
        df['atr'] = AverageTrueRange(df['high'], df['low'], df['close']).average_true_range()
        df['rsi'] = RSIIndicator(df['close']).rsi()
        macd = MACD(df['close'])
        df['macd'] = macd.macd()
        df['macd_signal'] = macd.macd_signal()
        df['adx'] = ADXIndicator(df['high'], df['low'], df['close']).adx()
        bb = BollingerBands(df['close'])
        df['bb_upper'] = bb.bollinger_hband()
        df['bb_lower'] = bb.bollinger_lband()

        trend_df = fetch_candles_for_symbol(symbol, interval="1h")
        trend = determine_trend(trend_df) if not trend_df.empty else "unknown"
        support, resistance = identify_support_resistance(df)

        last = df.iloc[-1]
        direction = "long" if last['close'] >= last['open'] * 0.998 else "short"
        buffer = 0.5 * last['atr']

        if direction == "long":
            stop_loss = support - buffer
            take_profit = last['close'] + 3.5 * last['atr']
        else:
            stop_loss = resistance + buffer
            take_profit = last['close'] - 3.5 * last['atr']

        rr = abs(take_profit - last['close']) / abs(last['close'] - stop_loss)

        # Фильтрация
        if rr < 2.5:
            raise ValueError("RR слишком низкий")
        if last['adx'] <= 25:
            raise ValueError("ADX слабый")
        if (direction == "long" and last['rsi'] >= 30) or (direction == "short" and last['rsi'] <= 70):
            raise ValueError("RSI не подтверждает сигнал")
        if (direction == "long" and last['macd'] <= last['macd_signal']) or (direction == "short" and last['macd'] >= last['macd_signal']):
            raise ValueError("MACD не подтверждает сигнал")
        if (direction == "long" and last['close'] > last['bb_lower']) or (direction == "short" and last['close'] < last['bb_upper']):
            raise ValueError("Цена не у края канала")

        confidence = "very high"
        score = round(min(10, rr * 2), 2)
        quality_score = rank_signal({
            "confidence": confidence,
            "score": score,
            "trend_strength": float(last['adx']),
            "confirmation_count": 4,
            "is_pending": False
        }) * 100

        result = {
            "symbol": symbol,
            "entry": round(last['close'], 2),
            "stop_loss": round(stop_loss, 2),
            "take_profit": round(take_profit, 2),
            "direction": direction,
            "confidence": confidence,
            "score": score,
            "signal_score": 4,
            "quality_score": round(quality_score, 2),
            "pending": False,
            "weak": False,
            "reasoning": f"Trend: {trend}, ADX strong, MACD + RSI confirm, near BB edge"
        }

        result["ai_comment"] = get_openai_analysis(
            symbol=symbol,
            timeframe=df.attrs.get("timeframe", "?"),
            trend=trend,
            indicators=f"RSI: {round(last['rsi'], 1)}, MACD: {round(last['macd'], 3)} > Signal: {round(last['macd_signal'], 3)}, ADX: {round(last['adx'], 1)}",
            reasoning=result["reasoning"],
            entry=result["entry"],
            stop_loss=result["stop_loss"],
            take_profit=result["take_profit"],
            direction=direction,
            confidence=confidence,
            score=score
        )

        # График (если получится)
        try:
            chart_path = plot_trade_signal(
                df=df,
                entry=result["entry"],
                stop_loss=result["stop_loss"],
                take_profit=result["take_profit"],
                signal_type=direction,
                symbol=symbol
            )
            result["chart_path"] = chart_path
        except Exception as chart_err:
            print(f"[❌] Ошибка при построении графика для {symbol}: {chart_err}")
            result["chart_path"] = None

        # ⏺️ Логгирование сигнала
        result.update({
            "timestamp": datetime.utcnow().isoformat(),
            "symbol": symbol,
            "timeframe": df.attrs.get("timeframe", "?"),
            "direction": direction,
            "entry": result["entry"],
            "stop_loss": result["stop_loss"],
            "take_profit": result["take_profit"],
            "confidence": confidence,
            "score": score,
            "signal_score": 4,
            "quality_score": round(quality_score, 2),
            "weak": False,
            "result": ""
        })

        log_signal(result)
        return result

    except Exception as e:
        print(f"[⚠️] Не найдено качественных сигналов для {symbol}, пробуем сгенерировать отложенный...")
        return generate_pending_trade_ideas(symbol, df)

# Обёртка
def analyze_symbol(symbol, df, swing_mode=False):
    return generate_trade_ideas(symbol, df, swing_mode)

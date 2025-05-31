
# analysis_utils.py
import pandas as pd
import numpy as np
import traceback
from ta.trend import EMAIndicator, MACD, ADXIndicator
from ta.momentum import RSIIndicator, StochRSIIndicator
from ta.volatility import AverageTrueRange, BollingerBands
from data_fetcher import fetch_candles_for_symbol
from utils.openai_analysis import get_openai_analysis
from utils.trade_logger import log_signal  # ← ДОБАВЬ СЮДА, не внутрь try!
from indicators.vumanchu_cipher import compute_vumanchu


def calculate_obv(df):
    obv = [0]
    for i in range(1, len(df)):
        if df['close'].iloc[i] > df['close'].iloc[i - 1]:
            obv.append(obv[-1] + df['volume'].iloc[i])
        elif df['close'].iloc[i] < df['close'].iloc[i - 1]:
            obv.append(obv[-1] - df['volume'].iloc[i])
        else:
            obv.append(obv[-1])
    return obv

def detect_candle_pattern(row):
    body = abs(row['close'] - row['open'])
    upper_wick = row['high'] - max(row['close'], row['open'])
    lower_wick = min(row['close'], row['open']) - row['low']
    if body < (upper_wick + lower_wick) * 0.3:
        return "doji"
    if row['close'] > row['open'] and body > upper_wick and body > lower_wick:
        return "bullish"
    if row['close'] < row['open'] and body > upper_wick and body > lower_wick:
        return "bearish"
    if row['close'] > row['open'] and lower_wick > 2 * body:
        return "hammer"
    if row['close'] < row['open'] and upper_wick > 2 * body:
        return "shooting_star"
    return None

def get_volume_profile_info(df, bins=20):
    df = df.copy()
    price_min = df['close'].min()
    price_max = df['close'].max()
    bin_edges = np.linspace(price_min, price_max, bins + 1)
    df['price_bin'] = pd.cut(df['close'], bins=bin_edges)
    volume_by_bin = df.groupby('price_bin', observed=False)['volume'].sum()
    poc_bin = volume_by_bin.idxmax()
    return poc_bin

def generate_trade_ideas(symbol, df, swing_mode=False):
    df = df.copy() if isinstance(df, pd.DataFrame) else df

    if swing_mode:
        print(f"[SWING MODE] Анализ свинг-режима активирован для {symbol}")

    df['ema_fast'] = EMAIndicator(df['close'], window=5).ema_indicator()
    df['ema_slow'] = EMAIndicator(df['close'], window=20).ema_indicator()
    df['macd'] = MACD(df['close']).macd_diff()
    df['rsi'] = RSIIndicator(df['close']).rsi()
    df['stochrsi'] = StochRSIIndicator(df['close']).stochrsi_k()
    df['adx'] = ADXIndicator(df['high'], df['low'], df['close']).adx()
    df['atr'] = AverageTrueRange(df['high'], df['low'], df['close']).average_true_range()
    df['bb_bbm'] = BollingerBands(df['close'], window=20).bollinger_mavg()
    df['bb_bbh'] = BollingerBands(df['close'], window=20).bollinger_hband()
    df['bb_bbl'] = BollingerBands(df['close'], window=20).bollinger_lband()
    df['vwap'] = (df['close'] * df['volume']).cumsum() / df['volume'].cumsum()
    df['pattern'] = df.apply(detect_candle_pattern, axis=1)
    df['obv'] = calculate_obv(df)
    df = compute_vumanchu(df)


    hl2 = (df['high'] + df['low']) / 2
    atr = df['atr']
    df['upper_band'] = hl2 + 3 * atr
    df['lower_band'] = hl2 - 3 * atr
    df['supertrend'] = True
    for i in range(1, len(df)):
        if df['close'].iloc[i] > df['upper_band'].iloc[i - 1]:
            df.at[df.index[i], 'supertrend'] = True
        elif df['close'].iloc[i] < df['lower_band'].iloc[i - 1]:
            df.at[df.index[i], 'supertrend'] = False
        else:
            df.at[df.index[i], 'supertrend'] = df['supertrend'].iloc[i - 1]

    try:
        last = df.iloc[-1]
        score = 0
        reasons = []

        if last['ema_fast'] > last['ema_slow']:
            score += 1
            reasons.append("EMA указывает на восходящий тренд")
        else:
            score -= 1
            reasons.append("EMA указывает на нисходящий тренд")

        if last['macd'] > 0:
            score += 1
            reasons.append("MACD положительный")
        else:
            score -= 1
            reasons.append("MACD отрицательный")

        if 50 < last['rsi'] < 70:
            score += 1
            reasons.append("RSI в бычьей зоне")
        elif last['rsi'] < 30:
            score -= 1
            reasons.append("RSI в перепроданности")

        if last['adx'] > 20:
            score += 1
            reasons.append("Сильный тренд по ADX")

        if last['close'] > last['vwap']:
            score += 1
            reasons.append("Цена выше VWAP")
        else:
            score -= 1
            reasons.append("Цена ниже VWAP")

        if last['close'] < last['bb_bbl']:
            score += 1
            reasons.append("Цена ниже Bollinger — перепроданность")
        elif last['close'] > last['bb_bbh']:
            score -= 1
            reasons.append("Цена выше Bollinger — перекупленность")

        if df['obv'].diff().iloc[-1] > 0:
            score += 1
            reasons.append("OBV растёт")
        else:
            score -= 1
            reasons.append("OBV падает")

        if last['supertrend']:
            score += 1
            reasons.append("Supertrend в лонг")
        else:
            score -= 1
            reasons.append("Supertrend в шорт")

        if last['pattern']:
            score += 1
            reasons.append(f"Паттерн: {last['pattern']}")

        poc_bin = get_volume_profile_info(df.tail(50))
        poc_center = (poc_bin.left + poc_bin.right) / 2
        if last['close'] > poc_center:
            score += 1
            reasons.append("Цена выше объёмной зоны")
        else:
            score -= 1
            reasons.append("Цена ниже объёмной зоны")
        
        # --- VUMANCHU ---
        if last["cipher_score"] > 2:
            score += 1
            reasons.append("VuManChu: Bullish signal")
        elif last["cipher_score"] < -2:
            score -= 1
            reasons.append("VuManChu: Bearish signal")
        else:
            reasons.append("VuManChu: Neutral")

        if last['bullish_div']:
            score += 1
            reasons.append("Bullish divergence (RSI)")
        elif last['bearish_div']:
            score -= 1
            reasons.append("Bearish divergence (RSI)")
        if abs(score) < 2:
            return None

        direction = "Long" if score > 0 else "Short"
        confidence = "Very High" if abs(score) > 5 else "High" if abs(score) > 3 else "Medium"

        formatted_reasons = "\n".join([f"- {r}" for r in reasons])
        prompt = (
            f"Символ: {symbol}\n"
            f"Цена: {last['close']:.2f}\n"
            f"Показатели:\n{formatted_reasons}\n\n"
            f"Сделка планируется в направлении: {direction}.\n"
            f"Подтверди, коротко, стоит ли открывать позицию или лучше воздержаться? Ответь в 1-2 строках."
        )
        ai_result = get_openai_analysis(prompt)
        if ai_result:
            short_ai = ai_result.strip().split(". ")[0][:120]
            reasons.append(f"AI: {short_ai}")
            if "покупку" in ai_result.lower():
                score += 1
            elif "продажу" in ai_result.lower():
                score -= 1

        entry = float(last['close'])
        stop = entry - float(last['atr']) if direction == "Long" else entry + float(last['atr'])
        target = entry + 2 * float(last['atr']) if direction == "Long" else entry - 2 * float(last['atr'])

        log_signal({
            "symbol": symbol,
            "direction": direction,
            "entry": round(entry, 2),
            "stop_loss": round(stop, 4),
            "take_profit": round(target, 4),
            "confidence": confidence,
            "score": score,
            "reasons": "; ".join(reasons),
        })
        return {
            "symbol": symbol,
            "direction": direction,
            "entry": round(entry, 2),
            "stop_loss": round(stop, 4),
            "take_profit": round(target, 4),
            "confidence": confidence,
            "score": score,
            "reasons": reasons
        }


    except Exception as e:
        print(f"[❌] Ошибка в generate_trade_ideas для {symbol}: {e}")
        traceback.print_exc()
        return None

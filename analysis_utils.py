
def get_volume_profile_info(df, bins=20):
    import numpy as np
    price_min = df['close'].min()
    price_max = df['close'].max()
    bin_edges = np.linspace(price_min, price_max, bins + 1)
    df.loc[:, 'price_bin'] = pd.cut(df['close'], bins=bin_edges)
    volume_by_bin = df.groupby('price_bin', observed=False)['volume'].sum()
    poc_bin = volume_by_bin.idxmax()
    return poc_bin



import pandas as pd
import numpy as np
from ta.trend import EMAIndicator, MACD, ADXIndicator
from ta.momentum import RSIIndicator, StochRSIIndicator
from ta.volatility import AverageTrueRange
from data_fetcher import fetch_candles_for_symbol
from utils.openai_analysis import get_openai_analysis

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

def check_micro_tf_confirmation(symbol, direction):
    try:
        df = fetch_candles_for_symbol(symbol, "5m", limit=10)
        if df is None or df.empty:
            return False

        df['volume_sma'] = df['volume'].rolling(window=5).mean()
        last = df.iloc[-1]
        previous = df.iloc[-4:-1]

        if direction == "Long":
            price_condition = all(previous['close'].diff().dropna() > 0)
        else:
            price_condition = all(previous['close'].diff().dropna() < 0)

        volume_condition = last['volume'] > last['volume_sma']

        return price_condition and volume_condition
    except:
        return False

def generate_trade_ideas(symbol, df):
    try:
        df = df.copy()
        df['ema_fast'] = EMAIndicator(df['close'], window=5).ema_indicator()
        df['ema_slow'] = EMAIndicator(df['close'], window=20).ema_indicator()
        df['macd'] = MACD(df['close']).macd_diff()
        df['rsi'] = RSIIndicator(df['close']).rsi()
        df['stochrsi'] = StochRSIIndicator(df['close']).stochrsi_k()
        df['adx'] = ADXIndicator(df['high'], df['low'], df['close']).adx()
        df['atr'] = AverageTrueRange(df['high'], df['low'], df['close']).average_true_range()
        df['pattern'] = df.apply(detect_candle_pattern, axis=1)

        last = df.iloc[-1]
        previous = df.iloc[-2]

        score = 0
        reasons = []

        if last['ema_fast'] > last['ema_slow']:
            score += 1
            reasons.append("Скользящие средние указывают на восходящий тренд")
        else:
            score -= 1
            reasons.append("Скользящие средние указывают на нисходящий тренд")

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
            reasons.append("RSI в зоне перепроданности")

        if last['adx'] > 20:
            score += 1
            reasons.append("Сильный тренд по ADX")

        if last['pattern']:
            reasons.append(f"Обнаружен свечной паттерн: {last['pattern']}")
            score += 1

        recent_window = df.tail(50)
        try:
            poc_bin = get_volume_profile_info(recent_window)
            poc_center = (poc_bin.left + poc_bin.right) / 2
            if last['close'] > poc_center:
                reasons.append("Цена выше зоны объёма")
                score += 1
            else:
                reasons.append("Цена ниже зоны объёма")
                score -= 1
        except Exception as e:
            print(f"[объем] Ошибка: {e}")

        ai_result = get_openai_analysis(symbol, df)
        if ai_result:
            reasons.append(f"AI: {ai_result}")
            if "покупку" in ai_result.lower():
                score += 1
            elif "продажу" in ai_result.lower():
                score -= 1

        direction = "Long" if score > 0 else "Short"
        confidence = "Very High" if abs(score) > 5 else "High" if abs(score) > 3 else "Medium"

        entry = float(last['close'])
        atr = float(last['atr'])
        stop = entry - atr if direction == "Long" else entry + atr
        target = entry + 2 * atr if direction == "Long" else entry - 2 * atr

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
        print(f"[❌] Ошибка анализа {symbol}: {e}")
        return None


    # --- Обрезанный блок ниже закомментирован из-за ошибок синтаксиса ---
    #     for symbol, timeframes in candles_dict.items():
    #         if symbol == "SUIUSDT":
    #             continue
    #         seen_signals = set()
    #         for tf, df in timeframes.items():
    #             try:
    #                 if not isinstance(df, pd.DataFrame) or df.empty or 'close' not in df.columns:
    #                     continue
    # 
    #                 df['ema20'] = EMAIndicator(close=df['close'], window=20).ema_indicator()
    #                 df['ema50'] = EMAIndicator(close=df['close'], window=50).ema_indicator()
    #                 df['ema200'] = EMAIndicator(close=df['close'], window=200).ema_indicator()
    #                 df['rsi'] = RSIIndicator(close=df['close'], window=14).rsi()
    #                 df['atr'] = AverageTrueRange(high=df['high'], low=df['low'], close=df['close'], window=14).average_true_range()
    #                 df['adx'] = ADXIndicator(high=df['high'], low=df['low'], close=df['close'], window=14).adx()
    #                 df['volume_sma'] = df['volume'].rolling(window=20).mean()
    # 
    #                 macd_obj = MACD(close=df['close'])
    #                 df['macd'] = macd_obj.macd()
    #                 df['macd_signal'] = macd_obj.macd_signal()
    # 
    #                 stoch_rsi = StochRSIIndicator(close=df['close'], window=14)
    #                 df['stoch_rsi'] = stoch_rsi.stochrsi_k()
    # 
    #                 df['pattern'] = df.apply(detect_candle_pattern, axis=1)
    # 
    #                 last = df.iloc[-1]
    #                 price = last['close']
    #                 atr = max(last['atr'], price * 0.002)
    #                 recent_window = df.iloc[-20:]
    #                 buffer = atr * 0.5
    # 
    #                 long_bias = last['ema20'] > last['ema50'] > last['ema200']
    #                 short_bias = last['ema20'] < last['ema50'] < last['ema200']
    # 
    #                 if long_bias:
    #                     direction = "Long"
    #                     local_min = recent_window['low'].min()
    #                     sl = min(price - atr, local_min - buffer)
    #                     tp = price + (price - sl) * 1.8
    #                 elif short_bias:
    #                     direction = "Short"
    #                     local_max = recent_window['high'].max()
    #                     sl = max(price + atr, local_max + buffer)
    #                     tp = price - (sl - price) * 1.8
    #                 else:
    #                     continue
    # 
    # 
    #                 recent_high = recent_window['high'].max()
    #                 recent_low = recent_window['low'].min()
    #                 prev_close = df.iloc[-2]['close']
    # 
    #                 if direction == "Short" and prev_close > recent_high and last['close'] < recent_high:
    #                     
    #                     reasons.append("Съём ликвидности (верх)")
    # 
    #                 
    #     try:
    #                     print(f"[объем] Ошибка: {e}")
    #                     
    # 
    #                 if direction == "Long" and prev_close < recent_low and last['close'] > recent_low:
    #                     
    #                     reasons.append("Съём ликвидности (низ)")
    # 
    #                     else:
    #                         
    #                         
    #                 
    # 
    # 
    #                 
    #                 
    #                 if last['close'] > poc_center:
    #                     
    #                     
    #                 else:
    #                     
    #                     
    # 
    # 
    # 
    #                 reasons = []
    #                 score = 0
    # 
    #                 if long_bias or short_bias:
    #                     
    #                     reasons.append("EMA порядок")
    # 
    #                 if direction == "Long" and last['macd'] > last['macd_signal']:
    #                     
    #                     reasons.append("MACD > сигн.")
    #                 if direction == "Short" and last['macd'] < last['macd_signal']:
    #                     
    #                     reasons.append("MACD < сигн.")
    # 
    #                 if direction == "Long" and last['stoch_rsi'] < 0.2:
    #                     
    #                     reasons.append("StochRSI низкий")
    #                 if direction == "Short" and last['stoch_rsi'] > 0.8:
    #                     
    #                     reasons.append("StochRSI высокий")
    # 
    #                 if direction == "Long" and last['rsi'] < 70:
    #                     
    #                     reasons.append("RSI < 70")
    #                 if direction == "Short" and last['rsi'] > 30:
    #                     
    #                     reasons.append("RSI > 30")
    # 
    #                 if last['adx'] > 20:
    #                     
    #                     reasons.append("ADX > 20")
    # 
    #                 if last['volume'] > last['volume_sma']:
    #                     
    #                     reasons.append("Объём > средн.")
    # 
    #                 if last['volume'] > last['volume_sma'] * 1.5:
    #                     
    #                     reasons.append("Объёмный всплеск")
    # 
    #                 if last['pattern'] in ["hammer", "bullish"] and direction == "Long":
    #                     
    #                     reasons.append(f"Паттерн: {last['pattern']}")
    #                 if last['pattern'] in ["shooting_star", "bearish"] and direction == "Short":
    #                     
    #                     reasons.append(f"Паттерн: {last['pattern']}")
    # 
    #                 if symbol in ["BTCUSDT", "ETHUSDT"]:
    #                     if check_micro_tf_confirmation(symbol, direction):
    #                         
    #                         reasons.append("Импульс подтверждён (5m)")
    # 
    #                 
    #                 prompt = f"Сигнал: {symbol}, направление: {direction}, цена: {price}, стоп: {sl}, тейк: {tp}, причина: {', '.join(reasons)}. Оцените обоснованность технически."
    #                 ai_result = get_openai_analysis(prompt)
    #                 reasons.append(f"AI: {ai_result}")
    # 
    #                 try:
    #                     poc_bin = get_volume_profile_info(recent_window)
    #                     poc_center = (poc_bin.left + poc_bin.right) / 2
    #                     if last['close'] > poc_center:
    #                         reasons.append("Цена выше зоны объёма")
    #                         score += 1
    #                     else:
    #                         reasons.append("Цена ниже зоны объёма")
    #                         score -= 1
    #                 except Exception as e:
    #                     print(f"[объем] Ошибка: {e}")
    # 
    #                 try:
    #                     
    #                     
    #                     if last['close'] > poc_center:
    #                         
    #                         
    #                     else:
    #                         
    #                         
    #                 
    # 
    # 
    # 
    #                 entry_key = (round(price, 4), direction, tf)
    #                 if entry_key in seen_signals:
    #                     continue
    #                 seen_signals.add(entry_key)
    # 
    #                 signal = {
    #                     "symbol": symbol,
    #                     "timeframe": tf,
    #                     "direction": direction,
    #                     "entry": round(price, 4),
    #                     "stop_loss": round(sl, 4),
    #                     "take_profit": round(tp, 4),
    #                     "score": score,
    #                     "confidence": ["Very Low", "Low", "Medium", "High", "Very High", "Extreme", "Ultra"][min(score, 6)],
    #                     "reason": ", ".join(reasons)
    #                 }
    #                 trade_signals.append(signal)
    # 
    #             except Exception as e:
    #                 print(f"⚠️ Error processing {symbol} {tf}: {e}")
    # 
    #     return sorted(trade_signals, key=lambda x: x['score'], reverse=True)

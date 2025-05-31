import pandas as pd
import traceback
from analysis_utils import generate_trade_ideas
from data_fetcher import fetch_all_intervals

def analyze_market(candles_dict, swing_mode=False):
    signals = []
    if not candles_dict:
        print("[❌] analyze_market получил пустой словарь")
        return signals

    for symbol, timeframes in candles_dict.items():
        if not timeframes:
            print(f"[⚠️] Пропущен {symbol}: нет данных таймфрейма")
            continue
        for tf, df in timeframes.items():
            if not isinstance(df, pd.DataFrame) or df.empty:
                print(f"[⚠️] Пропущен {symbol} на {tf}: некорректный DataFrame")
                continue
            try:
                result = generate_trade_ideas(symbol, df, swing_mode=swing_mode)
                if result is not None:
                    result["timeframe"] = tf
                    signals.append(result)
            except Exception as e:
                print(f"[❌] Ошибка анализа {symbol} на {tf}")
                traceback.print_exc()
    return signals

def run_signals_analysis(symbols=None):
    try:
        candles_dict = fetch_all_intervals(symbols=symbols, intervals=["15m", "1h", "4h", "1d"])
        if candles_dict is None:
            print("[❌] fetch_all_intervals вернул None")
            return "Ошибка при анализе", []

        print(f"🔍 Анализ символов: {symbols}")
        signals = analyze_market(candles_dict)
        summary_line = "📊 Сигнальный анализ завершён."
        return summary_line, signals
    except Exception as e:
        print("[❌] Ошибка в run_signals_analysis")
        traceback.print_exc()
        return "Ошибка при анализе", []

async def run_scalp_analysis(symbols=None):
    try:
        candles_dict = fetch_all_intervals(symbols=symbols, intervals=["1m", "5m", "15m", "1h"])

        if candles_dict is None:
            print("[❌] fetch_all_intervals вернул None в run_scalp_analysis")
            return "Ошибка при анализе", []

        print(f"🔍 Скальпинг-анализ символов: {symbols}")
        signals = analyze_market(candles_dict)
        summary_line = "📈 Скальпинг-анализ завершён."
        return summary_line, signals
    except Exception as e:
        print("[❌] Ошибка в run_scalp_analysis")
        traceback.print_exc()
        return "Ошибка при анализе", []

async def run_swing_analysis(symbols=None):
    try:
        candles_dict = fetch_all_intervals(symbols=symbols, intervals=["1h", "4h", "1d"])
        print(f"🔍 Swing-анализ символов: {symbols}")
        signals = analyze_market(candles_dict, swing_mode=True)
        summary_line = "🎯 Swing анализ завершён."
        return summary_line, signals
    except Exception as e:
        print("[❌] Ошибка в run_swing_analysis")
        traceback.print_exc()
        return "Ошибка при анализе", []


from analysis_utils import generate_trade_ideas
from data_fetcher import fetch_all_intervals

def analyze_market(candles_dict):
    signals = []
    for symbol, df in candles_dict.items():
        result = generate_trade_ideas(df, symbol)
        if result:
            signals.append(result)
    return signals

def run_signals_analysis(symbols=None):
    candles_dict = fetch_all_intervals(symbols=symbols)
    return analyze_market(candles_dict)

async def run_scalp_analysis(symbols=None):
    candles_dict = fetch_all_intervals(symbols=symbols)
    return None, analyze_market(candles_dict)


async def run_swing_analysis(symbols=None):
    from data_fetcher import fetch_all_intervals
    candles_dict = fetch_all_intervals(symbols, intervals=["1h", "4h", "1d"])
    result = analyze_market(candles_dict, swing_mode=True)
    summary_line = "🎯 Swing analysis complete."
    return summary_line, result

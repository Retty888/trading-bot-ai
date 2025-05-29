
from data_fetcher import fetch_all_intervals
from analysis_utils import generate_trade_ideas
from formatting import format_signals_vertical

def analyze_market(candles_dict, news=None, scalp_mode=False):
    signals = generate_trade_ideas(candles_dict, scalp_mode=scalp_mode)
    summary_line = "📈 Сигналы по стратегии 'скальпинг' на основе технического анализа:" if scalp_mode else "📶 Сигналы входа:"
    return summary_line, format_signals_vertical(signals)

async def run_scalp_analysis(symbols=None):
    if symbols is None:
        symbols = ["ETHUSDT", "BTCUSDT", "SUIUSDT"]
    candles_dict = fetch_all_intervals(symbols, intervals=["1m", "5m", "15m"])
    result = analyze_market(candles_dict, scalp_mode=True)
    return result

def run_signals_analysis():
    candles_dict = fetch_all_intervals(["ETHUSDT", "BTCUSDT", "SUIUSDT"], intervals=["5m", "1h", "4h"], lookback=300)
    return analyze_market(candles_dict)

async def run_swing_analysis():
    candles_dict = fetch_all_intervals(["ETHUSDT", "BTCUSDT", "SUIUSDT"], intervals=["1d", "4h"], lookback=400)
    return analyze_market(candles_dict)

# utils/analysis_dispatcher.py

import pandas as pd
from analysis_utils import generate_trade_ideas
from data_fetcher import fetch_all_intervals
from utils.results_logger import log_result
from utils.trade_logger import log_signal
from utils.signal_ranker import rank_signal
from utils.plot_signal_chart import plot_trade_signal
from utils.generate_pending_trade_ideas import generate_pending_trade_ideas

def run_signals_analysis(
    swing_mode: bool = False,
    symbols: list = None,
    intervals: list = None,
    limit: int = 500
):
    if symbols is None:
        symbols = ["BTCUSDT", "ETHUSDT"]
    if intervals is None:
        intervals = ["15m", "30m", "1h"] if not swing_mode else ["1h", "4h", "1d"]

    print(f"[⚙️] Загрузка актуальных свечей для: {symbols} ({intervals})")
    candles_dict = fetch_all_intervals(symbols, intervals)

    if not candles_dict:
        print("[❌] Не удалось загрузить свечи")
        return []

    print(f"[📊] Генерация сигналов...")
    signals = generate_trade_ideas(candles_dict, swing_mode=swing_mode)

    if not signals:
        print("⚠️ Сигналы не найдены, попробуем сгенерировать отложенные сигналы.")
        pending = generate_pending_trade_ideas(candles_dict)
        return pending

    ranked = rank_signal(signals)

    for signal in ranked:
        log_signal(signal)
        plot_trade_signal(signal)

    return ranked

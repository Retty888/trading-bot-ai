import mplfinance as mpf
import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_trade_signal(
    df: pd.DataFrame,
    entry: float,
    stop_loss: float,
    take_profit: float,
    signal_type: str,
    symbol: str = "ETHUSDT"
) -> str:
    """
    Рисует график с сигналом и сохраняет как PNG.
    """
    df = df.copy()
    df.index.name = 'Date'

    # 🧽 Приведение названий колонок к ожидаемым
    df = df.rename(columns={
        'open': 'Open',
        'high': 'High',
        'low': 'Low',
        'close': 'Close',
        'volume': 'Volume'
    })

    # EMA линии (если нет — рассчитываем)
    if 'EMA20' not in df.columns:
        df['EMA20'] = df['Close'].ewm(span=20, adjust=False).mean()
    if 'EMA50' not in df.columns:
        df['EMA50'] = df['Close'].ewm(span=50, adjust=False).mean()

    color = 'green' if signal_type == 'long' else 'red'

    # Добавление линий на график
    apds = [
        mpf.make_addplot(df['EMA20'], color='blue'),
        mpf.make_addplot(df['EMA50'], color='purple'),
        mpf.make_addplot([entry] * len(df), color=color, linestyle='--', width=1),
        mpf.make_addplot([stop_loss] * len(df), color='red', linestyle='--', width=1),
        mpf.make_addplot([take_profit] * len(df), color='cyan', linestyle='--', width=1)
    ]

    # Убедись, что директория charts/ существует
    chart_dir = os.path.join(os.path.dirname(__file__), '..', 'charts')
    os.makedirs(chart_dir, exist_ok=True)

    filename = f"{symbol}_{signal_type}_chart.png"
    filepath = os.path.join(chart_dir, filename)

    # Строим и сохраняем график
    fig, axlist = mpf.plot(
        df,
        type='candle',
        addplot=apds,
        volume=True,
        style='charles',
        returnfig=True,
        title=f"{symbol} Signal: {signal_type.upper()}"
    )
    fig.savefig(filepath, dpi=150)
    plt.close(fig)

    return os.path.abspath(filepath)


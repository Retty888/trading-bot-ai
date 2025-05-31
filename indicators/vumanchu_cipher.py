# indicators/vumanchu_cipher.py
import pandas as pd
import numpy as np


def compute_vumanchu(df: pd.DataFrame) -> pd.DataFrame:
    """
    Расчёт упрощённой версии индикатора VuManChu Cipher B + Divergences
    """
    df = df.copy()

    # Typical Price
    df['tp'] = (df['high'] + df['low'] + df['close']) / 3

    # Money Flow Index (MFI-like proxy)
    df['raw_money_flow'] = df['tp'] * df['volume']
    df['positive_flow'] = np.where(df['tp'] > df['tp'].shift(1), df['raw_money_flow'], 0)
    df['negative_flow'] = np.where(df['tp'] < df['tp'].shift(1), df['raw_money_flow'], 0)
    df['mfi'] = 100 * (df['positive_flow'].rolling(14).sum() /
                      (df['positive_flow'].rolling(14).sum() + df['negative_flow'].rolling(14).sum()))

    # EMA от TP
    df["ema_8"] = df["tp"].ewm(span=8).mean()
    df["ema_21"] = df["tp"].ewm(span=21).mean()

    # Momentum Wave (difference between price and SMA)
    df['sma_9'] = df['close'].rolling(9).mean()
    df['momentum_wave'] = df['close'] - df['sma_9']

    # MACD
    df["ema12"] = df["close"].ewm(span=12).mean()
    df["ema26"] = df["close"].ewm(span=26).mean()
    df["macd"] = df["ema12"] - df["ema26"]
    df["signal"] = df["macd"].ewm(span=9).mean()
    df["histogram"] = df["macd"] - df["signal"]

    # RSI Divergence (simplified)
    delta = df['close'].diff()
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)
    avg_gain = pd.Series(gain).rolling(14).mean()
    avg_loss = pd.Series(loss).rolling(14).mean()
    rs = avg_gain / avg_loss
    df['rsi'] = 100 - (100 / (1 + rs))

    # Cipher-like logic (условно)
    df["cipher_score"] = (
        (df["rsi"] - 50) / 10 +
        (df["histogram"] * 2) +
        (df["ema_8"] > df["ema_21"]).astype(int) * 2
    )

    df['bullish_div'] = ((df['close'] < df['close'].shift(5)) & (df['rsi'] > df['rsi'].shift(5))).astype(int)
    df['bearish_div'] = ((df['close'] > df['close'].shift(5)) & (df['rsi'] < df['rsi'].shift(5))).astype(int)

    return df
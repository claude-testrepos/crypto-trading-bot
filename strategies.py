import pandas as pd


def sma_crossover(df: pd.DataFrame, fast=20, slow=50) -> pd.Series:
    """1 = long, 0 = flat."""
    f = df["close"].rolling(fast).mean()
    s = df["close"].rolling(slow).mean()
    return (f > s).astype(int)


def rsi(series: pd.Series, period=14) -> pd.Series:
    delta = series.diff()
    gain = delta.clip(lower=0).ewm(alpha=1 / period, adjust=False).mean()
    loss = -delta.clip(upper=0).ewm(alpha=1 / period, adjust=False).mean()
    rs = gain / loss
    return 100 - 100 / (1 + rs)


def rsi_reversion(df: pd.DataFrame, low=30, high=70) -> pd.Series:
    r = rsi(df["close"])
    pos = pd.Series(float("nan"), index=df.index)
    pos[r < low] = 1
    pos[r > high] = 0
    return pos.ffill().fillna(0).astype(int)


STRATEGIES = {"sma": sma_crossover, "rsi": rsi_reversion}

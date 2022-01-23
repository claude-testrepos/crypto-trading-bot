import time
from pathlib import Path

import ccxt
import pandas as pd

CACHE = Path("data")


def fetch_ohlcv(symbol="BTC/USDT", timeframe="1h", since="2021-01-01", exchange="binance"):
    """Download candles (cached as CSV)."""
    CACHE.mkdir(exist_ok=True)
    path = CACHE / f"{exchange}_{symbol.replace('/', '-')}_{timeframe}.csv"
    if path.exists():
        return pd.read_csv(path, index_col="ts", parse_dates=True)

    ex = getattr(ccxt, exchange)({"enableRateLimit": True})
    since_ms = ex.parse8601(f"{since}T00:00:00Z")
    rows = []
    while True:
        batch = ex.fetch_ohlcv(symbol, timeframe, since=since_ms, limit=1000)
        if not batch:
            break
        rows += batch
        since_ms = batch[-1][0] + 1
        if len(batch) < 1000:
            break
        time.sleep(ex.rateLimit / 1000)

    df = pd.DataFrame(rows, columns=["ts", "open", "high", "low", "close", "volume"])
    df["ts"] = pd.to_datetime(df["ts"], unit="ms")
    df = df.set_index("ts")
    df.to_csv(path)
    return df

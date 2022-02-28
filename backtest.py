from data import fetch_ohlcv
from strategies import sma_crossover

df = fetch_ohlcv()
pos = sma_crossover(df)
ret = df["close"].pct_change() * pos.shift(1)
print("strategy:", (1 + ret).prod())
print("buy & hold:", df["close"].iloc[-1] / df["close"].iloc[0])

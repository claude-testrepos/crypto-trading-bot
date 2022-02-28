import argparse

import matplotlib.pyplot as plt
import numpy as np

from data import fetch_ohlcv
from strategies import STRATEGIES

FEE = 0.001  # 0.1% per trade (binance taker)


def run(df, strategy, fee=FEE):
    pos = STRATEGIES[strategy](df)
    trades = pos.diff().abs().fillna(0)
    ret = df["close"].pct_change().fillna(0) * pos.shift(1).fillna(0) - trades * fee
    equity = (1 + ret).cumprod()
    return equity, int(trades.sum())


def stats(equity, periods_per_year=24 * 365):
    ret = equity.pct_change().dropna()
    sharpe = np.sqrt(periods_per_year) * ret.mean() / ret.std() if ret.std() else 0
    drawdown = (equity / equity.cummax() - 1).min()
    return {"total": equity.iloc[-1] - 1, "sharpe": sharpe, "max_dd": drawdown}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--symbol", default="BTC/USDT")
    p.add_argument("--timeframe", default="1h")
    p.add_argument("--since", default="2021-01-01")
    p.add_argument("--strategy", choices=STRATEGIES, default="sma")
    p.add_argument("--plot", action="store_true")
    args = p.parse_args()

    df = fetch_ohlcv(args.symbol, args.timeframe, args.since)
    equity, n = run(df, args.strategy)
    hold = df["close"] / df["close"].iloc[0]
    for name, eq in (("strategy", equity), ("buy&hold", hold)):
        s = stats(eq)
        print(f"{name:>9}: return {s['total']:+.1%}  sharpe {s['sharpe']:.2f}  max dd {s['max_dd']:.1%}")
    print(f"trades: {n}")

    if args.plot:
        ax = equity.plot(label=args.strategy, figsize=(11, 5))
        hold.plot(ax=ax, label="buy & hold", alpha=.6)
        ax.set_yscale("log")
        ax.legend()
        plt.title(f"{args.symbol} {args.timeframe}")
        plt.show()


if __name__ == "__main__":
    main()

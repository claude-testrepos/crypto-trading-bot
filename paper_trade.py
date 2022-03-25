"""Paper trade a strategy live against exchange prices. No real orders are sent."""
import argparse
import json
import time
from datetime import datetime
from pathlib import Path

import ccxt
import pandas as pd

from notify import notify
from strategies import STRATEGIES

STATE = Path("paper_state.json")


def load_state(cash):
    if STATE.exists():
        return json.loads(STATE.read_text())
    return {"cash": cash, "coins": 0.0, "trades": []}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--symbol", default="BTC/USDT")
    p.add_argument("--strategy", choices=STRATEGIES, default="sma")
    p.add_argument("--cash", type=float, default=1000)
    p.add_argument("--interval", type=int, default=3600)
    args = p.parse_args()

    ex = ccxt.binance({"enableRateLimit": True})
    state = load_state(args.cash)
    while True:
        candles = ex.fetch_ohlcv(args.symbol, "1h", limit=200)
        df = pd.DataFrame(candles, columns=["ts", "open", "high", "low", "close", "volume"])
        want_long = STRATEGIES[args.strategy](df).iloc[-1] == 1
        price = df["close"].iloc[-1]

        if want_long and state["coins"] == 0:
            state["coins"] = state["cash"] * 0.999 / price
            state["cash"] = 0
            state["trades"].append({"t": datetime.utcnow().isoformat(), "side": "buy", "price": price})
            notify(f"🟢 BUY {args.symbol} @ {price:,.2f}")
        elif not want_long and state["coins"] > 0:
            state["cash"] = state["coins"] * price * 0.999
            state["coins"] = 0
            state["trades"].append({"t": datetime.utcnow().isoformat(), "side": "sell", "price": price})
            notify(f"🔴 SELL {args.symbol} @ {price:,.2f}  (portfolio ${state['cash']:,.2f})")

        value = state["cash"] + state["coins"] * price
        print(f"{datetime.now():%Y-%m-%d %H:%M} {args.symbol} {price:,.2f}  portfolio ${value:,.2f}")
        STATE.write_text(json.dumps(state, indent=2))
        time.sleep(args.interval)


if __name__ == "__main__":
    main()

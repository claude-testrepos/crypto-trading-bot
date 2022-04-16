# Crypto Trading Bot

Backtester and paper-trading bot I wrote while learning about crypto markets in early 2022 (spoiler: buy & hold lost a lot this year too). **Educational only, not financial advice.**

## Backtest

```
python backtest.py --symbol ETH/USDT --strategy rsi --plot
```

## Paper trade

```
python paper_trade.py --strategy sma --cash 1000
```

## Strategies

- `sma`: 20/50 SMA crossover
- `rsi`: buy RSI<30, sell RSI>70
- `macd`: MACD line above signal

## Notifications

Set `DISCORD_WEBHOOK_URL` to get a Discord message on every paper trade.

## TODO

- [ ] add more tests
- [ ] add screenshots
- [ ] clean up the code

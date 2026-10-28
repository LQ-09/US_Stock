# US Stock Factor Research

An exploratory Python project for computing daily equity factors and comparing them with next-day returns.

## What the code does

- Computes momentum, volatility, moving averages, and RSI from adjusted closing prices.
- Creates next-day price and return labels from daily Parquet files.
- Samples up to 500 stocks and reports average within-stock factor/next-day-return correlations.

The main files are `factors/factor.py`, `backtest/gen_prediction.py`, `backtest/gen_factor.py`, and `backtest/backtest_time.py`.

## Setup and entry point

The source imports pandas and tqdm; Parquet access also requires a compatible engine such as pyarrow. No dependency lockfile is supplied.

From the repository root, the current research entry point is:

```sh
python backtest/backtest_time.py
```

It prompts for a factor name; an empty response selects all factors. Expected inputs are in `data/daily_folder/`, with `Adj. Close` and a time index. Existing factors are read from `factors/stock_factors/`.

## Current limitations

This is an incomplete research prototype. The current `compute_factors()` collects newly calculated factor frames but does not write them to disk, so the entry point relies on already stored factor files. `backtest/strategy/strategy1.py` is empty.

The label-generation script overwrites input Parquet files when adding target columns. Work on copies of data.

Reported correlations are exploratory associations, not out-of-sample portfolio returns. No verified strategy performance is claimed. Sampling, survivorship bias, corporate actions, execution costs, and time splits need explicit validation. The repository includes market-data files; their redistribution rights require review.

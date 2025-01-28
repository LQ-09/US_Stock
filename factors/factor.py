# Data: Open	High	Low	Close	Adj. Close	Volume	Dividend	Shares Outstanding

import pandas as pd

def calculate_momentum(df, lookback_period=20):
    """ 计算动量因子: (当前价格 / N 天前价格) - 1 """
    df[f"Momentum_{lookback_period}D"] = (df["Adj. Close"] / df["Adj. Close"].shift(lookback_period)) - 1
    return df[[f"Momentum_{lookback_period}D"]]

def calculate_volatility(df, lookback_period=20):
    """ 计算波动率因子: N 天收益率的标准差 """
    df[f"Volatility_{lookback_period}D"] = df["Adj. Close"].pct_change().rolling(lookback_period).std()
    return df[[f"Volatility_{lookback_period}D"]]

def calculate_moving_average(df, lookback_period=20):
    """ 计算均线因子: N 天移动平均 """
    df[f"MA_{lookback_period}D"] = df["Adj. Close"].rolling(lookback_period).mean()
    return df[[f"MA_{lookback_period}D"]]

def calculate_rsi(df, lookback_period=14):
    """ 计算 RSI 因子 """
    delta = df["Adj. Close"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(lookback_period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(lookback_period).mean()
    rs = gain / loss
    df[f"RSI_{lookback_period}D"] = 100 - (100 / (1 + rs))
    return df[[f"RSI_{lookback_period}D"]]

# 映射因子名称到计算函数
FACTOR_FUNCTIONS = {
    "Momentum_20D": lambda df: calculate_momentum(df, 20),
    "Momentum_60D": lambda df: calculate_momentum(df, 60),
    "Volatility_20D": lambda df: calculate_volatility(df, 20),
    "Volatility_60D": lambda df: calculate_volatility(df, 60),
    "MA_20D": lambda df: calculate_moving_average(df, 20),
    "MA_60D": lambda df: calculate_moving_average(df, 60),
    "RSI_14D": lambda df: calculate_rsi(df, 14),
}

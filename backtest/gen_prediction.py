import os
import pandas as pd

# 设定数据目录
DATA_DIR = "data/daily_folder/"

def compute_prediction_target(stock_file):
    """
    在原 Parquet 文件中直接增加：
    - Future_Return_1D: 未来 1 天收益率
    - Future_Price_1D: 未来 1 天价格
    - 如果列已存在，则跳过
    """
    file_path = os.path.join(DATA_DIR, stock_file)

    # 读取 Parquet 文件
    df = pd.read_parquet(file_path)

    # 检测是否已有目标列，防止重复计算
    if "Future_Return_1D" in df.columns and "Future_Price_1D" in df.columns:
        # print(f"{stock_file} 已包含目标列，跳过计算")
        return

    # 计算未来 1 天的 return 和 price
    df["Future_Return_1D"] = df["Adj. Close"].shift(-1) / df["Adj. Close"] - 1
    df["Future_Price_1D"] = df["Adj. Close"].shift(-1)

    # 直接覆盖原 Parquet 文件
    df.to_parquet(file_path, index=True)
    # print(f"{stock_file} 目标值已添加并更新到原文件")

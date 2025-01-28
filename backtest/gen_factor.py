import sys
import os
import pandas as pd
from random_stock import get_random_stocks  # 导入随机选股函数

# 获取 backtest 的上级目录（US_Stock）
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from factors.factor import FACTOR_FUNCTIONS  # 现在可以正确导入

# 设定数据目录和输出目录
DATA_DIR = "data/daily_folder/"
OUTPUT_DIR = "factors/stock_factors/"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def compute_factors(stock_file, factor_name=None):
    """
    计算股票的因子，并保存到 factors/stock_factors/ 目录。
    - 如果 factor_name=None，则计算所有因子
    - 如果 factor_name 指定某个因子，则只计算该因子
    - 如果某个因子已经存在，则跳过计算
    """
    file_path = os.path.join(DATA_DIR, stock_file)
    output_file = os.path.join(OUTPUT_DIR, stock_file)

    # 读取原始数据
    df = pd.read_parquet(file_path)

    # 读取已有的因子数据（如果存在）
    if os.path.exists(output_file):
        df_factors = pd.read_parquet(output_file)
    else:
        df_factors = pd.DataFrame(index=df.index)  # 创建空 DataFrame

    # 选择需要计算的因子
    if factor_name:
        factors_to_compute = {factor_name: FACTOR_FUNCTIONS[factor_name]} if factor_name in FACTOR_FUNCTIONS else {}
    else:
        factors_to_compute = FACTOR_FUNCTIONS  # 计算所有因子

    # 存储新计算的因子
    new_factors = []

    for name, func in factors_to_compute.items():
        if name in df_factors.columns:
            # print(f"{stock_file}: {name} 已存在，跳过计算")
            continue
        else:
            print(f"计算因子: {name} for {stock_file}")
            factor_df = func(df)  # 计算因子
            new_factors.append(factor_df)


# 测试用 main
# if __name__ == "__main__":
#     print("开始测试 compute_factors()")

#     # 选取随机股票
#     selected_stocks = get_random_stocks(1)  # 选 1 只股票进行测试
#     if not selected_stocks:
#         print("没有找到股票数据，请检查 data/daily_folder/")
#     else:
#         test_stock = selected_stocks[0]
#         print(f"测试股票: {test_stock}")
#         compute_factors(test_stock)

#     print("测试完成！")
import os
import pandas as pd
from random_stock import get_random_stocks
from gen_prediction import compute_prediction_target
from gen_factor import compute_factors
from tqdm import tqdm 

def compute_factor_correlation(stock_file, factor_name=None):
    """
    计算单只股票的因子和 Future_Return_1D 的相关性
    - factor_name: 如果指定，则计算单个因子的相关性，否则计算所有因子
    """
    factors_path = os.path.join("factors/stock_factors/", stock_file)
    stock_path = os.path.join("data/daily_folder/", stock_file)

    # 读取数据
    df_factors = pd.read_parquet(factors_path)
    df_stock = pd.read_parquet(stock_path)

    # 确保 `Future_Return_1D` 存在
    if "Future_Return_1D" not in df_stock.columns:
        # print(f"{stock_file} 没有 Future_Return_1D，跳过计算相关性")
        return None

    # 只计算指定因子的相关性
    if factor_name and factor_name in df_factors.columns:
        df = df_stock[["Future_Return_1D"]].join(df_factors[[factor_name]], how="inner")
    else:
        df = df_stock[["Future_Return_1D"]].join(df_factors, how="inner")

    # 计算相关性
    correlation = df.corr().iloc[0, 1:]  # 计算因子与 `Future_Return_1D` 的相关性
    return correlation

def main(factor_name=None):
    """ 
    主函数：随机选股，计算预测目标，计算因子，并计算相关性 
    - factor_name: 如果指定，只计算该因子；否则计算所有因子
    """
    selected_stocks = get_random_stocks(500)

    # 计算未来目标值，添加进度条
    print("计算预测目标（Future Return 和 Price）：")
    for stock in tqdm(selected_stocks, desc="预测目标进度", unit="stock"):
        compute_prediction_target(stock)

    # 计算所有因子或单一因子
    print(f"计算 {'所有因子' if factor_name is None else factor_name}：")
    for stock in tqdm(selected_stocks, desc="因子计算进度", unit="stock"):
        compute_factors(stock, factor_name)

    # 计算因子与 Future_Return_1D 的相关性
    print(f"计算 {'所有因子' if factor_name is None else factor_name} 与 Future_Return_1D 的相关性：")
    correlations = []
    for stock in tqdm(selected_stocks, desc="相关性计算进度", unit="stock"):
        corr = compute_factor_correlation(stock, factor_name)
        if corr is not None:
            correlations.append(corr)

    # 合并所有相关性结果并求均值
    if correlations:
        avg_correlation = pd.DataFrame(correlations).mean()
        print(f"\n{factor_name if factor_name else '所有因子'} 对 Future_Return_1D 的平均相关性:\n{avg_correlation}")

if __name__ == "__main__":
    factor_to_test = input("请输入要测试的因子名称（留空计算所有因子）：").strip()
    factor_to_test = None if factor_to_test == "" else factor_to_test
    main(factor_to_test)

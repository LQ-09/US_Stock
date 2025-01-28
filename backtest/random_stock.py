import os
import random

# 设定数据目录
DATA_DIR = "data/daily_folder/"

def get_random_stocks(num_stocks=500):
    """ 从 daily_folder 目录中随机抽取指定数量的股票文件 """
    
    # 获取所有股票（即 Parquet 文件名）
    all_stocks = [f for f in os.listdir(DATA_DIR) if f.endswith(".parquet")]

    # 随机抽取 num_stocks 只股票（如果总数不足 num_stocks，则取全部）
    num_samples = min(num_stocks, len(all_stocks))
    selected_stocks = random.sample(all_stocks, num_samples)

    # 返回选中的股票列表
    return selected_stocks

# 测试函数
# if __name__ == "__main__":
#     stocks = get_random_stocks()
#     print("Random Stocks are:")
#     for stock in stocks:
#         print(stock)

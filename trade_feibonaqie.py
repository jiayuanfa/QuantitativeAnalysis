import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import datetime, timedelta
import sys

def auto_detect_swing_points(price_data, window=20):
    """
    自动检测摆动高点和低点
    """
    # 寻找局部高点和低点
    highs = price_data['High']
    lows = price_data['Low']
    
    # 使用滚动窗口检测局部极值
    local_highs = highs.rolling(window=window, center=True).max()
    local_lows = lows.rolling(window=window, center=True).min()
    
    # 找出真正的摆动点
    swing_high_idx = highs[highs == local_highs].index[-1]
    swing_low_idx = lows[lows == local_lows].index[-2]  # 使用倒数第二个低点以获得更好的趋势
    
    return swing_high_idx, swing_low_idx

def calculate_fibonacci_levels(high, low, is_uptrend=True):
    """
    计算斐波那契回撤和扩展水平
    """
    # 价格差
    price_range = high - low
    
    # 斐波那契回撤水平
    fib_retracement_levels = {
        '0%': high if is_uptrend else low,
        '23.6%': high - 0.236 * price_range if is_uptrend else low + 0.236 * price_range,
        '38.2%': high - 0.382 * price_range if is_uptrend else low + 0.382 * price_range,
        '50%': high - 0.5 * price_range if is_uptrend else low + 0.5 * price_range,
        '61.8%': high - 0.618 * price_range if is_uptrend else low + 0.618 * price_range,
        '78.6%': high - 0.786 * price_range if is_uptrend else low + 0.786 * price_range,
        '100%': low if is_uptrend else high
    }
    
    # 斐波那契扩展水平
    fib_extension_levels = {
        '100%': high if is_uptrend else low,
        '127.2%': high + 0.272 * price_range if is_uptrend else low - 0.272 * price_range,
        '161.8%': high + 0.618 * price_range if is_uptrend else low - 0.618 * price_range,
        '261.8%': high + 1.618 * price_range if is_uptrend else low - 1.618 * price_range
    }
    
    return fib_retracement_levels, fib_extension_levels

def plot_fibonacci_analysis(symbol):
    """
    主函数：只需输入股票代码即可进行斐波那契分析
    """
    # 设置日期范围（最近一年）
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
    
    # 获取股票数据
    print(f"正在获取 {symbol} 的数据...")
    stock_data = yf.download(symbol, start=start_date, end=end_date)
    
    if stock_data.empty:
        print("未能获取数据，请检查股票代码")
        return
    
    # 自动检测摆动点
    print("正在分析价格走势...")
    swing_high_idx, swing_low_idx = auto_detect_swing_points(stock_data)
    
    # 确定趋势方向
    swing_high_date = stock_data.index.get_loc(swing_high_idx)
    swing_low_date = stock_data.index.get_loc(swing_low_idx)
    is_uptrend = swing_high_date > swing_low_date
    
    # 获取摆动高点和低点价格
    if is_uptrend:
        swing_high = stock_data.loc[swing_high_idx, 'High']
        swing_low = stock_data.loc[swing_low_idx, 'Low']
        print(f"检测到上升趋势：低点 {swing_low:.2f} (日期: {swing_low_idx.strftime('%Y-%m-%d')}) -> 高点 {swing_high:.2f} (日期: {swing_high_idx.strftime('%Y-%m-%d')})")
    else:
        swing_high = stock_data.loc[swing_low_idx, 'High']  # 交换高低点
        swing_low = stock_data.loc[swing_high_idx, 'Low']
        print(f"检测到下降趋势：高点 {swing_high:.2f} (日期: {swing_high_idx.strftime('%Y-%m-%d')}) -> 低点 {swing_low:.2f} (日期: {swing_low_idx.strftime('%Y-%m-%d')})")
    
    # 计算斐波那契水平
    fib_retracement, fib_extension = calculate_fibonacci_levels(swing_high, swing_low, is_uptrend)
    
    # 创建图表
    plt.figure(figsize=(14, 10))
    
    # 绘制价格走势
    plt.plot(stock_data.index, stock_data['Close'], label='收盘价', linewidth=2, color='black')
    
    # 标记摆动点
    if is_uptrend:
        plt.scatter(swing_low_idx, swing_low, color='green', s=100, zorder=5, label='摆动低点')
        plt.scatter(swing_high_idx, swing_high, color='red', s=100, zorder=5, label='摆动高点')
    else:
        plt.scatter(swing_high_idx, swing_high, color='red', s=100, zorder=5, label='摆动高点')
        plt.scatter(swing_low_idx, swing_low, color='green', s=100, zorder=5, label='摆动低点')
    
    # 绘制斐波那契回撤水平线
    colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'brown']
    retracement_labels_added = set()
    
    for i, (level, price) in enumerate(fib_retracement.items()):
        color = colors[i % len(colors)]
        label = f'回撤 {level}' if level not in retracement_labels_added else ""
        plt.axhline(y=price, color=color, linestyle='-', alpha=0.7, label=label)
        plt.text(stock_data.index[-1], price, f' {level} ({price:.2f})', 
                verticalalignment='center', fontsize=9, color=color)
        retracement_labels_added.add(level)
    
    # 绘制斐波那契扩展水平线
    extension_labels_added = set()
    
    for i, (level, price) in enumerate(fib_extension.items()):
        color = colors[(i + len(fib_retracement)) % len(colors)]
        label = f'扩展 {level}' if level not in extension_labels_added else ""
        plt.axhline(y=price, color=color, linestyle='--', alpha=0.7, label=label)
        plt.text(stock_data.index[-1], price, f' {level} ({price:.2f})', 
                verticalalignment='center', fontsize=9, color=color)
        extension_labels_added.add(level)
    
    # 添加图例和标题
    plt.title(f'{symbol} 斐波那契回撤与扩展分析', fontsize=16, fontweight='bold')
    plt.xlabel('日期')
    plt.ylabel('价格')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # 显示图表
    plt.show()
    
    # 打印斐波那契水平
    print("\n斐波那契回撤水平:")
    for level, price in sorted(fib_retracement.items(), key=lambda x: float(x[0].replace('%', ''))):
        print(f"{level}: {price:.2f}")
    
    print("\n斐波那契扩展水平:")
    for level, price in sorted(fib_extension.items(), key=lambda x: float(x[0].replace('%', ''))):
        print(f"{level}: {price:.2f}")
    
    # 显示当前价格相对于斐波那契水平的位置
    current_price = stock_data['Close'].iloc[-1]
    print(f"\n当前价格: {current_price:.2f}")
    
    # 找出当前价格所处的斐波那契区间
    all_levels = {**fib_retracement, **fib_extension}
    sorted_levels = sorted(all_levels.items(), key=lambda x: x[1])
    
    for i in range(len(sorted_levels)-1):
        if sorted_levels[i][1] <= current_price <= sorted_levels[i+1][1]:
            print(f"当前处于 {sorted_levels[i][0]} 和 {sorted_levels[i+1][0]} 之间")
            break

# 使用示例
if __name__ == "__main__":
    # 检查命令行参数
    if len(sys.argv) > 1:
        symbol = sys.argv[1].strip().upper()
    else:
        # 如果没有命令行参数，尝试交互式输入
        try:
            symbol = input("请输入股票代码（例如：AAPL、TSLA、0005.HK）: ").strip().upper()
        except EOFError:
            print("错误：无法获取输入。请使用命令行参数：")
            print("python3 trade_feibonaqie.py AAPL")
            print("python3 trade_feibonaqie.py TSLA")
            print("python3 trade_feibonaqie.py 0005.HK")
            sys.exit(1)
    
    if not symbol:
        print("错误：请输入有效的股票代码")
        sys.exit(1)
    
    # 进行斐波那契分析
    plot_fibonacci_analysis(symbol)
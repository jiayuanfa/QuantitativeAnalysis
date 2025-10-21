#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def calculate_fibonacci_levels(high, low, is_uptrend=True):
    """
    计算斐波那契回撤和扩展水平
    
    参数:
    - high: 摆动高点价格
    - low: 摆动低点价格  
    - is_uptrend: 是否为上升趋势（True=上升趋势，False=下降趋势）
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

def print_fibonacci_analysis(high, low, is_uptrend=True, current_price=None):
    """
    打印斐波那契分析结果
    """
    fib_retracement, fib_extension = calculate_fibonacci_levels(high, low, is_uptrend)
    
    trend_text = "上升趋势" if is_uptrend else "下降趋势"
    print(f"\n=== 斐波那契分析 ({trend_text}) ===")
    print(f"摆动高点: {high:.2f}")
    print(f"摆动低点: {low:.2f}")
    print(f"价格区间: {abs(high - low):.2f}")
    
    print(f"\n📉 斐波那契回撤水平:")
    for level, price in sorted(fib_retracement.items(), key=lambda x: float(x[0].replace('%', ''))):
        print(f"  {level:>6}: {price:>8.2f}")
    
    print(f"\n📈 斐波那契扩展水平:")
    for level, price in sorted(fib_extension.items(), key=lambda x: float(x[0].replace('%', ''))):
        print(f"  {level:>6}: {price:>8.2f}")
    
    if current_price is not None:
        print(f"\n💰 当前价格: {current_price:.2f}")
        
        # 找出当前价格所处的斐波那契区间
        all_levels = {**fib_retracement, **fib_extension}
        sorted_levels = sorted(all_levels.items(), key=lambda x: x[1])
        
        for i in range(len(sorted_levels)-1):
            if sorted_levels[i][1] <= current_price <= sorted_levels[i+1][1]:
                print(f"📍 当前处于 {sorted_levels[i][0]} 和 {sorted_levels[i+1][0]} 之间")
                break

def main():
    """
    主函数：交互式斐波那契计算器
    """
    print("🎯 斐波那契回撤与扩展计算器")
    print("=" * 50)
    
    try:
        # 获取摆动高点
        high = float(input("请输入摆动高点价格: "))
        
        # 获取摆动低点
        low = float(input("请输入摆动低点价格: "))
        
        # 检查价格合理性
        if high <= low:
            print("❌ 错误：高点价格必须大于低点价格")
            return
        
        # 确定趋势方向
        trend_input = input("趋势方向 (u=上升趋势, d=下降趋势) [默认: u]: ").strip().lower()
        is_uptrend = trend_input != 'd'
        
        # 获取当前价格（可选）
        current_price_input = input("请输入当前价格 (可选，直接回车跳过): ").strip()
        current_price = float(current_price_input) if current_price_input else None
        
        # 计算并显示结果
        print_fibonacci_analysis(high, low, is_uptrend, current_price)
        
        # 提供交易建议
        if current_price is not None:
            print(f"\n💡 交易建议:")
            fib_retracement, fib_extension = calculate_fibonacci_levels(high, low, is_uptrend)
            
            # 找出最接近的斐波那契水平
            all_levels = {**fib_retracement, **fib_extension}
            closest_level = min(all_levels.items(), key=lambda x: abs(x[1] - current_price))
            
            distance = abs(closest_level[1] - current_price)
            percentage = (distance / current_price) * 100
            
            print(f"  最接近的斐波那契水平: {closest_level[0]} ({closest_level[1]:.2f})")
            print(f"  距离: {distance:.2f} ({percentage:.1f}%)")
            
            if percentage < 2:
                print("  ⚠️  当前价格非常接近关键斐波那契水平，注意可能的支撑/阻力")
            elif percentage < 5:
                print("  📊 当前价格接近斐波那契水平，可作为参考")
            else:
                print("  📈 当前价格距离斐波那契水平较远，继续观察")
        
    except ValueError:
        print("❌ 错误：请输入有效的数字")
    except KeyboardInterrupt:
        print("\n👋 程序已退出")
    except Exception as e:
        print(f"❌ 发生错误: {e}")

if __name__ == "__main__":
    main()


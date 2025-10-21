#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

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

def print_fibonacci_analysis(high, low, is_uptrend=True, current_price=None, use_current_as_high=False):
    """
    打印斐波那契分析结果
    """
    fib_retracement, fib_extension = calculate_fibonacci_levels(high, low, is_uptrend)
    
    trend_text = "上升趋势" if is_uptrend else "下降趋势"
    print(f"\n=== 斐波那契分析 ({trend_text}) ===")
    print(f"摆动高点: {high:.2f}")
    print(f"摆动低点: {low:.2f}")
    print(f"价格区间: {abs(high - low):.2f}")
    
    if use_current_as_high:
        print("📈 模式: 无明确高点，以当前价为高点计算扩展目标")
    
    # 只在非"无明确高点"模式下显示回撤水平
    if not use_current_as_high:
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
        if use_current_as_high:
            # 无明确高点模式：只比较扩展水平
            all_levels = fib_extension
        
        sorted_levels = sorted(all_levels.items(), key=lambda x: x[1])
        
        for i in range(len(sorted_levels)-1):
            if sorted_levels[i][1] <= current_price <= sorted_levels[i+1][1]:
                print(f"📍 当前处于 {sorted_levels[i][0]} 和 {sorted_levels[i+1][0]} 之间")
                break

def show_usage():
    """
    显示使用方法
    """
    print("🎯 斐波那契回撤与扩展计算器")
    print("=" * 50)
    print("使用方法:")
    print("  python3 fibonacci_simple.py <高点> <低点> [趋势] [当前价格] [--use-current-as-high]")
    print("")
    print("参数说明:")
    print("  高点: 摆动高点价格 (必需，或使用 --use-current-as-high 时忽略)")
    print("  低点: 摆动低点价格 (必需)")
    print("  趋势: u=上升趋势, d=下降趋势 (可选，默认: u)")
    print("  当前价格: 当前价格 (必需，当使用 --use-current-as-high 时)")
    print("  --use-current-as-high: 将当前价作为高点，计算扩展目标")
    print("")
    print("示例:")
    print("  python3 fibonacci_simple.py 100 75                    # 标准用法")
    print("  python3 fibonacci_simple.py 100 75 u 85              # 带当前价格")
    print("  python3 fibonacci_simple.py 100 75 d 80              # 下降趋势")
    print("  python3 fibonacci_simple.py 0 75 u 90 --use-current-as-high  # 无明确高点")
    print("")
    print("💡 无参考高点场景:")
    print("  当股票创新高或没有明确高点时，使用 --use-current-as-high")
    print("  脚本会以当前价为高点，计算扩展目标位")

def main():
    """
    主函数：命令行斐波那契计算器
    """
    if len(sys.argv) < 3:
        show_usage()
        return
    
    # 解析参数
    use_current_as_high = "--use-current-as-high" in sys.argv
    
    # 过滤掉 --use-current-as-high 参数
    args = [arg for arg in sys.argv[1:] if arg != "--use-current-as-high"]
    
    try:
        # 解析命令行参数
        high = float(args[0]) if not use_current_as_high else 0
        low = float(args[1])
        
        # 趋势方向
        is_uptrend = True
        if len(args) > 2:
            trend = args[2].lower()
            if trend == 'd':
                is_uptrend = False
            elif trend != 'u':
                print("❌ 错误：趋势参数只能是 'u' (上升) 或 'd' (下降)")
                return
        
        # 当前价格
        current_price = None
        if len(args) > 3:
            current_price = float(args[3])
        elif use_current_as_high:
            print("❌ 错误：使用 --use-current-as-high 时必须提供当前价格")
            return
        
        # 特殊处理：使用当前价作为高点
        if use_current_as_high:
            if current_price is None:
                print("❌ 错误：使用 --use-current-as-high 时必须提供当前价格")
                return
            high = current_price
            print(f"🔍 无明确高点模式：将当前价 {current_price} 作为高点")
        
        # 检查价格合理性
        if high <= low:
            print("❌ 错误：高点价格必须大于低点价格")
            return
        
        # 计算并显示结果
        print_fibonacci_analysis(high, low, is_uptrend, current_price, use_current_as_high)
        
        # 提供交易建议
        if current_price is not None:
            print(f"\n💡 交易建议:")
            fib_retracement, fib_extension = calculate_fibonacci_levels(high, low, is_uptrend)
            
            # 找出最接近的斐波那契水平
            all_levels = {**fib_retracement, **fib_extension}
            if use_current_as_high:
                all_levels = fib_extension
            
            closest_level = min(all_levels.items(), key=lambda x: abs(x[1] - current_price))
            
            distance = abs(closest_level[1] - current_price)
            percentage = (distance / current_price) * 100
            
            print(f"  最接近的斐波那契水平: {closest_level[0]} ({closest_level[1]:.2f})")
            print(f"  距离: {distance:.2f} ({percentage:.1f}%)")
            
            if use_current_as_high:
                print(f"\n🎯 无明确高点策略建议:")
                print(f"  • 当前价作为临时高点，关注扩展目标位")
                print(f"  • 127.2% 目标: {fib_extension['127.2%']:.2f}")
                print(f"  • 161.8% 目标: {fib_extension['161.8%']:.2f}")
                print(f"  • 261.8% 目标: {fib_extension['261.8%']:.2f}")
                print(f"  • 突破当前高点后，可重新计算斐波那契水平")
            else:
                if percentage < 2:
                    print("  ⚠️  当前价格非常接近关键斐波那契水平，注意可能的支撑/阻力")
                elif percentage < 5:
                    print("  📊 当前价格接近斐波那契水平，可作为参考")
                else:
                    print("  📈 当前价格距离斐波那契水平较远，继续观察")
        
    except ValueError:
        print("❌ 错误：请输入有效的数字")
    except Exception as e:
        print(f"❌ 发生错误: {e}")

if __name__ == "__main__":
    main()
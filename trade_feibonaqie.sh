#!/bin/bash

# 斐波那契回撤与扩展计算器
# 使用方法: ./trade_feibonaqie.sh <高点> <低点> [趋势] [当前价格] [--use-current-as-high]

# 检查参数数量
if [ $# -lt 2 ]; then
    echo "🎯 斐波那契回撤与扩展计算器"
    echo "=================================================="
    echo "使用方法:"
    echo "  $0 <高点> <低点> [趋势] [当前价格] [--use-current-as-high]"
    echo ""
    echo "参数说明:"
    echo "  高点: 摆动高点价格 (必需，或使用 --use-current-as-high 时忽略)"
    echo "  低点: 摆动低点价格 (必需)"
    echo "  趋势: u=上升趋势, d=下降趋势 (可选，默认: u)"
    echo "  当前价格: 当前价格 (必需，当使用 --use-current-as-high 时)"
    echo "  --use-current-as-high: 将当前价作为高点，计算扩展目标"
    echo ""
    echo "示例:"
    echo "  $0 100 75                    # 标准用法"
    echo "  $0 100 75 u 85              # 带当前价格"
    echo "  $0 100 75 d 80              # 下降趋势"
    echo "  $0 0 75 u 90 --use-current-as-high  # 无明确高点，用当前价90当高点"
    echo ""
    echo "💡 无参考高点场景:"
    echo "  当股票创新高或没有明确高点时，使用 --use-current-as-high"
    echo "  脚本会以当前价为高点，计算扩展目标位"
    exit 1
fi

# 初始化变量
USE_CURRENT_AS_HIGH=false
HIGH=""
LOW=""
TREND="u"
CURRENT_PRICE=""

# 解析参数
ARGS=("$@")
for ((i=0; i<${#ARGS[@]}; i++)); do
    if [ "${ARGS[i]}" = "--use-current-as-high" ]; then
        USE_CURRENT_AS_HIGH=true
    elif [ -z "$HIGH" ] && [[ "${ARGS[i]}" =~ ^[0-9]+\.?[0-9]*$ ]]; then
        HIGH="${ARGS[i]}"
    elif [ -z "$LOW" ] && [[ "${ARGS[i]}" =~ ^[0-9]+\.?[0-9]*$ ]]; then
        LOW="${ARGS[i]}"
    elif [ "${ARGS[i]}" = "u" ] || [ "${ARGS[i]}" = "d" ]; then
        TREND="${ARGS[i]}"
    elif [[ "${ARGS[i]}" =~ ^[0-9]+\.?[0-9]*$ ]] && [ -n "$LOW" ]; then
        CURRENT_PRICE="${ARGS[i]}"
    fi
done

# 特殊处理：使用当前价作为高点
if [ "$USE_CURRENT_AS_HIGH" = true ]; then
    if [ -z "$CURRENT_PRICE" ]; then
        echo "❌ 错误：使用 --use-current-as-high 时必须提供当前价格"
        exit 1
    fi
    HIGH="$CURRENT_PRICE"
    echo "🔍 无明确高点模式：将当前价 $CURRENT_PRICE 作为高点"
fi

# 验证必需参数
if [ -z "$HIGH" ] || [ -z "$LOW" ]; then
    echo "❌ 错误：缺少必需的高点或低点价格"
    exit 1
fi

# 检查高点是否大于低点
if (( $(echo "$HIGH <= $LOW" | bc -l) )); then
    echo "❌ 错误：高点价格必须大于低点价格"
    exit 1
fi

# 计算价格区间
RANGE=$(echo "$HIGH - $LOW" | bc -l)

# 确定趋势方向
if [ "$TREND" = "d" ]; then
    TREND_TEXT="下降趋势"
    IS_UPTREND=false
else
    TREND_TEXT="上升趋势"
    IS_UPTREND=true
fi

echo ""
echo "=== 斐波那契分析 ($TREND_TEXT) ==="
echo "摆动高点: $(printf "%.2f" $HIGH)"
echo "摆动低点: $(printf "%.2f" $LOW)"
echo "价格区间: $(printf "%.2f" $RANGE)"

if [ "$USE_CURRENT_AS_HIGH" = true ]; then
    echo "📈 模式: 无明确高点，以当前价为高点计算扩展目标"
fi

# 只在非"无明确高点"模式下显示回撤水平
if [ "$USE_CURRENT_AS_HIGH" = false ]; then
    echo ""
    echo "📉 斐波那契回撤水平:"
    
    # 计算回撤水平
    if [ "$IS_UPTREND" = true ]; then
        echo "      0%: $(printf "%8.2f" $HIGH)"
        echo "   23.6%: $(printf "%8.2f" $(echo "$HIGH - 0.236 * $RANGE" | bc -l))"
        echo "   38.2%: $(printf "%8.2f" $(echo "$HIGH - 0.382 * $RANGE" | bc -l))"
        echo "     50%: $(printf "%8.2f" $(echo "$HIGH - 0.5 * $RANGE" | bc -l))"
        echo "   61.8%: $(printf "%8.2f" $(echo "$HIGH - 0.618 * $RANGE" | bc -l))"
        echo "   78.6%: $(printf "%8.2f" $(echo "$HIGH - 0.786 * $RANGE" | bc -l))"
        echo "    100%: $(printf "%8.2f" $LOW)"
    else
        echo "      0%: $(printf "%8.2f" $LOW)"
        echo "   23.6%: $(printf "%8.2f" $(echo "$LOW + 0.236 * $RANGE" | bc -l))"
        echo "   38.2%: $(printf "%8.2f" $(echo "$LOW + 0.382 * $RANGE" | bc -l))"
        echo "     50%: $(printf "%8.2f" $(echo "$LOW + 0.5 * $RANGE" | bc -l))"
        echo "   61.8%: $(printf "%8.2f" $(echo "$LOW + 0.618 * $RANGE" | bc -l))"
        echo "   78.6%: $(printf "%8.2f" $(echo "$LOW + 0.786 * $RANGE" | bc -l))"
        echo "    100%: $(printf "%8.2f" $HIGH)"
    fi
fi

echo ""
echo "📈 斐波那契扩展水平:"

# 计算扩展水平
if [ "$IS_UPTREND" = true ]; then
    echo "    100%: $(printf "%8.2f" $HIGH)"
    echo "  127.2%: $(printf "%8.2f" $(echo "$HIGH + 0.272 * $RANGE" | bc -l))"
    echo "  161.8%: $(printf "%8.2f" $(echo "$HIGH + 0.618 * $RANGE" | bc -l))"
    echo "  261.8%: $(printf "%8.2f" $(echo "$HIGH + 1.618 * $RANGE" | bc -l))"
else
    echo "    100%: $(printf "%8.2f" $LOW)"
    echo "  127.2%: $(printf "%8.2f" $(echo "$LOW - 0.272 * $RANGE" | bc -l))"
    echo "  161.8%: $(printf "%8.2f" $(echo "$LOW - 0.618 * $RANGE" | bc -l))"
    echo "  261.8%: $(printf "%8.2f" $(echo "$LOW - 1.618 * $RANGE" | bc -l))"
fi

# 如果有当前价格，显示分析
if [ -n "$CURRENT_PRICE" ]; then
    echo ""
    echo "💰 当前价格: $(printf "%.2f" $CURRENT_PRICE)"
    
    # 计算最接近的斐波那契水平
    if [ "$IS_UPTREND" = true ]; then
        if [ "$USE_CURRENT_AS_HIGH" = true ]; then
            # 无明确高点模式：只比较扩展水平
            LEVELS="$HIGH $(echo "$HIGH + 0.272 * $RANGE" | bc -l) $(echo "$HIGH + 0.618 * $RANGE" | bc -l) $(echo "$HIGH + 1.618 * $RANGE" | bc -l)"
        else
            LEVELS="$HIGH $(echo "$HIGH - 0.236 * $RANGE" | bc -l) $(echo "$HIGH - 0.382 * $RANGE" | bc -l) $(echo "$HIGH - 0.5 * $RANGE" | bc -l) $(echo "$HIGH - 0.618 * $RANGE" | bc -l) $(echo "$HIGH - 0.786 * $RANGE" | bc -l) $LOW $(echo "$HIGH + 0.272 * $RANGE" | bc -l) $(echo "$HIGH + 0.618 * $RANGE" | bc -l) $(echo "$HIGH + 1.618 * $RANGE" | bc -l)"
        fi
    else
        if [ "$USE_CURRENT_AS_HIGH" = true ]; then
            LEVELS="$LOW $(echo "$LOW - 0.272 * $RANGE" | bc -l) $(echo "$LOW - 0.618 * $RANGE" | bc -l) $(echo "$LOW - 1.618 * $RANGE" | bc -l)"
        else
            LEVELS="$LOW $(echo "$LOW + 0.236 * $RANGE" | bc -l) $(echo "$LOW + 0.382 * $RANGE" | bc -l) $(echo "$LOW + 0.5 * $RANGE" | bc -l) $(echo "$LOW + 0.618 * $RANGE" | bc -l) $(echo "$LOW + 0.786 * $RANGE" | bc -l) $HIGH $(echo "$LOW - 0.272 * $RANGE" | bc -l) $(echo "$LOW - 0.618 * $RANGE" | bc -l) $(echo "$LOW - 1.618 * $RANGE" | bc -l)"
        fi
    fi
    
    # 找到最接近的水平
    MIN_DISTANCE=999999
    CLOSEST_LEVEL=""
    for level in $LEVELS; do
        distance=$(echo "scale=2; ($CURRENT_PRICE - $level)^2" | bc -l)
        distance=$(echo "sqrt($distance)" | bc -l)
        if (( $(echo "$distance < $MIN_DISTANCE" | bc -l) )); then
            MIN_DISTANCE=$distance
            CLOSEST_LEVEL=$level
        fi
    done
    
    percentage=$(echo "scale=1; $MIN_DISTANCE / $CURRENT_PRICE * 100" | bc -l)
    
    echo ""
    echo "💡 交易建议:"
    echo "  最接近的斐波那契水平: $(printf "%.2f" $CLOSEST_LEVEL)"
    echo "  距离: $(printf "%.2f" $MIN_DISTANCE) ($(printf "%.1f" $percentage)%)"
    
    if [ "$USE_CURRENT_AS_HIGH" = true ]; then
        echo ""
        echo "🎯 无明确高点策略建议:"
        echo "  • 当前价作为临时高点，关注扩展目标位"
        echo "  • 127.2% 目标: $(printf "%.2f" $(echo "$HIGH + 0.272 * $RANGE" | bc -l))"
        echo "  • 161.8% 目标: $(printf "%.2f" $(echo "$HIGH + 0.618 * $RANGE" | bc -l))"
        echo "  • 261.8% 目标: $(printf "%.2f" $(echo "$HIGH + 1.618 * $RANGE" | bc -l))"
        echo "  • 突破当前高点后，可重新计算斐波那契水平"
    else
        if (( $(echo "$percentage < 2" | bc -l) )); then
            echo "  ⚠️  当前价格非常接近关键斐波那契水平，注意可能的支撑/阻力"
        elif (( $(echo "$percentage < 5" | bc -l) )); then
            echo "  📊 当前价格接近斐波那契水平，可作为参考"
        else
            echo "  📈 当前价格距离斐波那契水平较远，继续观察"
        fi
    fi
fi

echo ""
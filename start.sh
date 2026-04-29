#!/bin/bash
# 自适应学习Agent系统 - 启动脚本

echo "=========================================="
echo "  🎓 自适应学习Agent系统"
echo "  Adaptive Learning Agent System"
echo "=========================================="
echo ""

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到Python3，请先安装Python 3.7+"
    exit 1
fi

echo "[OK] Python version: $(python3 --version)"

# 安装依赖
echo ""
echo "📦 安装依赖..."
pip3 install -r requirements.txt --break-system-packages -q

echo ""
echo "🚀 启动系统..."
echo "   访问地址: http://localhost:5000"
echo "   按 Ctrl+C 停止"
echo ""

cd "$(dirname "$0")"
python3 app.py

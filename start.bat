@echo off
chcp 65001 >nul
echo ==========================================
echo   🎓 自适应学习Agent系统
echo   Adaptive Learning Agent System
echo ==========================================
echo.

echo 📦 安装依赖...
pip install -r requirements.txt -q

echo.
echo 🚀 启动系统...
echo    访问地址: http://localhost:5000
echo    按 Ctrl+C 停止
echo.

cd /d "%~dp0"
python app.py
pause

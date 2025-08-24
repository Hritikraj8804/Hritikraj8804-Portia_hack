@echo off
echo 🚀 Starting DevOps AI Assistant
echo ===============================
echo.

echo 🔧 Starting Backend...
start "Backend" python backend/simple_backend.py

echo ⏳ Waiting 2 seconds...
timeout /t 2 /nobreak >nul

echo 🎨 Starting Frontend...
python -m streamlit run frontend/app.py

echo.
pause
@echo off
echo 🚀 Quick Start - DevOps AI Assistant
echo.

echo Starting backend server...
start "Backend API" cmd /k "cd backend & python simple_server.py"

timeout /t 3 /nobreak > nul

echo Starting frontend dashboard...
start "Frontend Dashboard" cmd /k "python -m streamlit run frontend/app.py --server.port 8501"

echo.
echo ✅ Both services starting...
echo 📊 Dashboard: http://localhost:8501
echo 🔧 API: http://localhost:8000
echo.
echo Press any key to open dashboard...
pause > nul
start http://localhost:8501
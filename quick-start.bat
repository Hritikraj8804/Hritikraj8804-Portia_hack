@echo off
echo 🚀 DevOps AI Assistant - Quick Start
echo =====================================
echo.

echo.
echo 🔧 Starting Backend (Port 8000)...
start "Backend" cmd /k "echo Backend running at http://localhost:8000 && python backend/simple_backend.py"

echo ⏳ Waiting for backend to start...
timeout /t 3 /nobreak >nul

echo 🎨 Starting Frontend (Port 8501)...
start "Frontend" cmd /k "echo Frontend running at http://localhost:8501 && python -m streamlit run frontend/app.py"

echo.
echo 🎉 Application started successfully!
echo.
echo 📱 Access your app at: http://localhost:8501
echo 📚 API docs at: http://localhost:8000
echo.
echo Press any key to exit (this will NOT stop the servers)
pause >nul
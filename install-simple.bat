@echo off
echo 🔧 Simple Installation - DevOps AI Assistant...
echo.

echo Installing core dependencies only...
pip install fastapi uvicorn pydantic streamlit python-dotenv httpx

echo.
echo ✅ Core installation complete!
echo.
echo To start:
echo 1. Run: start-backend.bat
echo 2. Run: start-frontend.bat
echo.
pause
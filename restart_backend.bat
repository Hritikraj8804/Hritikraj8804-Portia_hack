@echo off
echo Stopping existing backend server...
taskkill /f /im python.exe 2>nul
timeout /t 2 /nobreak >nul

echo Starting backend server...
cd /d "%~dp0"
start "Backend Server" python backend/simple_backend.py

echo Backend server restarted!
echo Check the new window for debug output.
pause
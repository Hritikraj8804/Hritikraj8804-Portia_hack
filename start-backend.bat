@echo off
echo 🚀 Starting DevOps Assistant Backend...
echo.

cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

echo.
echo Backend started at http://localhost:8000
echo API Documentation: http://localhost:8000/docs
pause
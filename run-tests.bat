@echo off
echo 🧪 Running DevOps AI Assistant Test Suite...
echo.
python test_app.py
echo.
if %ERRORLEVEL% EQU 0 (
    echo ✅ All tests passed! Ready to start the application.
    echo.
    echo Next steps:
    echo 1. Run start-backend.bat in one terminal
    echo 2. Run start-frontend.bat in another terminal
    echo 3. Open http://localhost:8501 in your browser
) else (
    echo ❌ Some tests failed. Please fix the issues before running the application.
)
echo.
pause
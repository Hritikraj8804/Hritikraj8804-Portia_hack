@echo off
echo 📦 Installing DevOps AI Assistant Dependencies...
echo.

echo 🔧 Installing required packages...
pip install -r requirements.txt

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ Installation completed successfully!
    echo.
    echo 🚀 Ready to start! Run: quick-start.bat
) else (
    echo.
    echo ❌ Installation failed. Please check the error messages above.
)

echo.
pause
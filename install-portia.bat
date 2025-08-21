@echo off
echo 🔧 Installing Portia SDK...
echo.

echo Installing portia-sdk-python...
pip install portia-sdk-python[google]

echo.
echo Testing installation...
python -c "from portia import Portia; print('✅ Portia SDK installed successfully')"

echo.
echo ✅ Ready to test Portia integration!
echo Run: python test-portia.py
pause
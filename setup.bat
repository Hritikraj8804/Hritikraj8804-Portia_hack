@echo off
echo 🔧 Setting up DevOps AI Assistant...
echo.

echo 1. Installing Python dependencies...
pip install -r requirements.txt

echo.
echo 2. Setting up environment...
if not exist .env (
    copy .env.example .env
    echo Created .env file - please add your API keys
) else (
    echo .env file already exists
)

echo.
echo 3. Testing backend...
cd backend
python -c "from main import app; print('✅ Backend imports successfully')"
cd ..

echo.
echo 4. Testing frontend...
python -c "import streamlit; print('✅ Streamlit installed successfully')"

echo.
echo ✅ Setup complete!
echo.
echo Next steps:
echo 1. Add your API keys to .env file
echo 2. Run start-backend.bat to start the API
echo 3. Run start-frontend.bat to start the dashboard
echo 4. Upload portia-agents/*.py to Portia Labs dashboard
echo.
pause
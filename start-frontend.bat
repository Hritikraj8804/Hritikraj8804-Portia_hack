@echo off
echo 🎨 Starting DevOps AI Assistant Frontend...
echo.
echo Frontend will be available at: http://localhost:8501
echo Make sure backend is running at: http://localhost:8000
echo.
python -m streamlit run frontend/app.py
pause
@echo off
echo 🎨 Starting DevOps Assistant Frontend...
echo.

streamlit run frontend/app.py --server.port 8501

echo.
echo Frontend started at http://localhost:8501
pause
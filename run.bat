@echo off
echo =========================================
echo  Starting AI Virtual Team Builder Servers
echo =========================================

REM Check if .venv exists
if not exist .venv (
    echo [ERROR] Virtual environment not found! Please run setup.bat first.
    pause
    exit /b 1
)

REM Start FastAPI Backend in a separate window
echo Launching FastAPI Backend (Port 8000)...
start "FastAPI Backend" cmd /k "call .venv\Scripts\activate.bat && uvicorn app.api.main:app --reload --port 8000"

REM Wait a brief moment
timeout /t 2 /nobreak >nul

REM Start Streamlit Frontend
echo Launching Streamlit Frontend (Port 8501)...
call .venv\Scripts\activate.bat
streamlit run app/main.py --server.port 8501

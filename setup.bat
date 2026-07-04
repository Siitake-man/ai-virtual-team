@echo off
echo =========================================
echo  Starting AI Virtual Team Builder Setup  
echo =========================================

REM Create virtual environment
if not exist .venv (
    echo [1/4] Creating virtual environment (.venv)...
    python -m venv .venv
    echo Virtual environment created.
) else (
    echo [1/4] Virtual environment (.venv) already exists. Skipping.
)

REM Install dependencies
echo [2/4] Installing dependencies from requirements.txt...
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
echo Dependencies installed successfully.

REM Create directories
echo [3/4] Creating local directories...
if not exist data\projects mkdir data\projects
if not exist data\presets mkdir data\presets
if not exist exports mkdir exports
echo Directories checked/created.

REM Setup .env
echo [4/4] Setting up environment configuration...
if not exist .env (
    copy .env.example .env
    echo Created .env from .env.example. Please update your API keys in .env!
) else (
    echo .env already exists. Skipping.
)

echo =========================================
echo  Setup Completed Successfully!
echo  Use run.ps1 or run.bat to start the app.
echo =========================================
pause

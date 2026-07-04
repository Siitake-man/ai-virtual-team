# Start script for AI Virtual Team Builder (FastAPI + Streamlit in parallel)
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host " Starting AI Virtual Team Builder Servers" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

# Check if .venv exists
if (-not (Test-Path .venv)) {
    Write-Error "Virtual environment not found! Please run setup.ps1 first."
    Exit 1
}

# Start FastAPI in a background command window
Write-Host "Launching FastAPI Backend (Port 8000)..." -ForegroundColor Yellow
Start-Process cmd -ArgumentList "/k", "title FastAPI Backend && .\.venv\Scripts\activate.bat && uvicorn app.api.main:app --reload --port 8000"

# Wait a brief moment for FastAPI to initialize
Start-Sleep -Seconds 2

# Start Streamlit in this window
Write-Host "Launching Streamlit Frontend (Port 8501)..." -ForegroundColor Yellow
& .venv\Scripts\Activate.ps1
streamlit run app/main.py --server.port 8501

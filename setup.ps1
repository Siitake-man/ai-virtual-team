# Setup script for AI Virtual Team Builder (Windows PowerShell)
$ErrorActionPreference = "Stop"

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host " Starting AI Virtual Team Builder Setup  " -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

# Create Python virtual environment if it doesn't exist
if (-not (Test-Path .venv)) {
    Write-Host "[1/4] Creating virtual environment (.venv)..." -ForegroundColor Yellow
    python -m venv .venv
    Write-Host "Virtual environment created." -ForegroundColor Green
} else {
    Write-Host "[1/4] Virtual environment (.venv) already exists. Skipping creation." -ForegroundColor Green
}

# Install / Upgrade dependencies
Write-Host "[2/4] Installing dependencies from requirements.txt..." -ForegroundColor Yellow
& .venv\Scripts\pip install --upgrade pip
& .venv\Scripts\pip install -r requirements.txt
Write-Host "Dependencies installed successfully." -ForegroundColor Green

# Create required directories
Write-Host "[3/4] Creating local directories..." -ForegroundColor Yellow
$dirs = @("data\projects", "data\presets", "exports")
foreach ($dir in $dirs) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "Created directory: $dir" -ForegroundColor Green
    } else {
        Write-Host "Directory already exists: $dir" -ForegroundColor Green
    }
}

# Create .env file if it doesn't exist
Write-Host "[4/4] Setting up environment configuration..." -ForegroundColor Yellow
if (-not (Test-Path .env)) {
    Copy-Item .env.example .env
    Write-Host "Created .env from .env.example. Please update your API keys in .env!" -ForegroundColor Yellow
} else {
    Write-Host ".env already exists. Skipping copy." -ForegroundColor Green
}

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host " Setup Completed Successfully!" -ForegroundColor Cyan
Write-Host " Use run.ps1 or run.bat to start the app." -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

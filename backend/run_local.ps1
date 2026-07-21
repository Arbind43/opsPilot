# OpsPilot Backend — Local Run Script
# Run from: opspilot/backend/

$ErrorActionPreference = "Stop"

Write-Host "Starting OpsPilot Backend..." -ForegroundColor Cyan

# Activate virtual environment
$venvActivate = Join-Path $PSScriptRoot "venv\Scripts\Activate.ps1"
if (!(Test-Path $venvActivate)) {
    Write-Error "Virtual environment not found. Run setup first."
    exit 1
}

& $venvActivate

# Set env vars from .env file in parent directory
$envFile = Join-Path $PSScriptRoot "..\..env" | Resolve-Path -ErrorAction SilentlyContinue
if (!$envFile) {
    $envFile = Join-Path $PSScriptRoot "..\.env"
}

# Start the backend
Write-Host "Launching FastAPI on http://localhost:8000" -ForegroundColor Green
Write-Host "API docs: http://localhost:8000/docs" -ForegroundColor Yellow
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --env-file ..\\.env

# OpsPilot Backend — Local Celery Worker Script
# Run from: opspilot/backend/

$ErrorActionPreference = "Stop"

Write-Host "Starting OpsPilot Celery Worker..." -ForegroundColor Cyan

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

# Add backend and parent directory to PYTHONPATH
$env:PYTHONPATH = "$PSScriptRoot;$(Split-Path $PSScriptRoot -Parent)"

Write-Host "Launching Celery Worker" -ForegroundColor Green
# Using pool=solo for Windows compatibility
celery -A worker.celery_app worker -l info --pool=solo

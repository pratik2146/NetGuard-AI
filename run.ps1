# PowerShell Automation Script for NetGuard AI

Write-Host "=================================================" -ForegroundColor Cyan
Write-Host " NetGuard AI - Enterprise Setup & Execution Script" -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan

# 1. Virtual Environment Setup
if (-not (Test-Path "venv")) {
    Write-Host "[1/4] Creating Python Virtual Environment..." -ForegroundColor Yellow
    python -m venv venv
}

Write-Host "[2/4] Cleaning site-packages & Installing Dependencies..." -ForegroundColor Yellow
if (Test-Path "venv\Lib\site-packages") {
    Get-ChildItem -Path "venv\Lib\site-packages" -Filter "~*" -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
}

.\venv\Scripts\python.exe -m pip install -q --disable-pip-version-check -r requirements.txt
.\venv\Scripts\python.exe -m pip install -q --disable-pip-version-check -e .

# 3. Model Pipeline Execution
Write-Host "[3/4] Running Model Training Pipeline & Artifact Generation..." -ForegroundColor Yellow
.\venv\Scripts\python.exe train_model.py

# 4. Streamlit App Launch
Write-Host "[4/4] Launching NetGuard AI Streamlit Platform..." -ForegroundColor Green
if (Test-Path ".\venv\Scripts\python.exe") {
    .\venv\Scripts\python.exe -m streamlit run app.py
} else {
    python -m streamlit run app.py
}

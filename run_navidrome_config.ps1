# Navidrome Configuration GUI Launcher (PowerShell)
# ================================================

Write-Host "Navidrome Configuration GUI Launcher" -ForegroundColor Cyan
Write-Host "===================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python from https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host "Make sure to check 'Add Python to PATH' during installation" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Checking dependencies..." -ForegroundColor Yellow

# Check if toml module is installed
try {
    python -c "import toml" 2>$null
    Write-Host "Dependencies are already installed." -ForegroundColor Green
} catch {
    Write-Host "Installing required dependencies..." -ForegroundColor Yellow
    try {
        pip install -r requirements.txt
        Write-Host "Dependencies installed successfully." -ForegroundColor Green
    } catch {
        Write-Host "ERROR: Failed to install dependencies" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}

Write-Host "Starting Navidrome Configuration GUI..." -ForegroundColor Green
try {
    python navidrome_config_gui.py
} catch {
    Write-Host ""
    Write-Host "An error occurred while running the GUI." -ForegroundColor Red
    Read-Host "Press Enter to exit"
}

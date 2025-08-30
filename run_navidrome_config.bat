@echo off
echo Navidrome Configuration GUI Launcher
echo ===================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo Python found. Checking dependencies...

REM Check if toml module is installed
python -c "import toml" >nul 2>&1
if errorlevel 1 (
    echo Installing required dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
    echo Dependencies installed successfully.
)

echo Starting Navidrome Configuration GUI...
python navidrome_config_gui.py

if errorlevel 1 (
    echo.
    echo An error occurred while running the GUI.
    pause
)

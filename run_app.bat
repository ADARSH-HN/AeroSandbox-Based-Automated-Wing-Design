@echo off
REM Wing Analyzer Pro - Windows Launcher
REM Double-click this file to launch the application

echo ============================================================
echo   Wing Analyzer Pro - Quick Launcher
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo Checking dependencies...
pip show streamlit >nul 2>&1
if errorlevel 1 (
    echo.
    echo Installing required packages...
    pip install -r requirements.txt
)

echo.
echo Starting Wing Analyzer Pro...
echo The application will open in your default browser.
echo.
echo To stop the application, close this window or press Ctrl+C
echo ============================================================
echo.

streamlit run app.py

pause

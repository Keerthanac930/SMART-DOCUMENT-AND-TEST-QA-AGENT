@echo off
echo 🚀 Starting Smart Document QA Agent...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

REM Check if requirements are installed
echo 📦 Checking dependencies...
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo 📦 Installing dependencies...
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Failed to install dependencies
        pause
        exit /b 1
    )
)

REM Create necessary directories
if not exist "vector_db" mkdir vector_db
if not exist "embeddings_cache" mkdir embeddings_cache
if not exist "uploads" mkdir uploads

REM Check for API key
if "%GOOGLE_AI_API_KEY%"=="" (
    echo ⚠️  No Google AI API key found
    echo    The app will run in limited mode
    echo    Set GOOGLE_AI_API_KEY environment variable for full functionality
    echo.
)

REM Start the application
echo 🚀 Starting application...
echo 📱 Open your browser to http://localhost:8501
echo.
python run.py

pause

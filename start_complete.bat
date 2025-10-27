@echo off
echo ============================================
echo  Smart Document QA Agent - Complete Setup
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.10+ from https://www.python.org/
    pause
    exit /b 1
)

echo [1/6] Setting up backend...
cd backend_fastapi

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing backend dependencies...
pip install -r requirements.txt

REM Create necessary directories
if not exist "uploads\" mkdir uploads
if not exist "vector_db\" mkdir vector_db

echo.
echo [2/6] Starting backend server...
start "Backend Server" cmd /k "venv\Scripts\activate.bat && python main.py"

cd ..

REM Wait a bit for backend to start
timeout /t 5 /nobreak >nul

echo.
echo [3/6] Setting up frontend...
cd frontend_react

REM Check if node_modules exists
if not exist "node_modules\" (
    echo Installing frontend dependencies...
    call npm install
)

echo.
echo [4/6] Starting frontend server...
start "Frontend Server" cmd /k "npm run dev"

cd ..

echo.
echo [5/6] Creating startup script...
echo.
echo ============================================
echo  Setup Complete!
echo ============================================
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo API Docs: http://localhost:8000/docs
echo.
echo Note: To stop the servers, close the command windows
echo.

timeout /t 3 /nobreak >nul

REM Open browser to frontend
start http://localhost:3000

echo.
echo Setup complete! The application should be running.
pause


#!/bin/bash

echo "============================================"
echo " Smart Document QA Agent - Complete Setup"
echo "============================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python is not installed"
    echo "Please install Python 3.10+ from https://www.python.org/"
    exit 1
fi

echo "[1/6] Setting up backend..."
cd backend_fastapi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing backend dependencies..."
pip install -r requirements.txt

# Create necessary directories
mkdir -p uploads vector_db

echo ""
echo "[2/6] Starting backend server..."
gnome-terminal -- bash -c "cd backend_fastapi && source venv/bin/activate && python main.py; exec bash" 2>/dev/null || \
osascript -e 'tell app "Terminal" to do script "cd backend_fastapi && source venv/bin/activate && python main.py"' 2>/dev/null || \
xterm -e "cd backend_fastapi && source venv/bin/activate && python main.py" &

cd ..

# Wait a bit for backend to start
sleep 5

echo ""
echo "[3/6] Setting up frontend..."
cd frontend_react

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install
fi

echo ""
echo "[4/6] Starting frontend server..."
gnome-terminal -- bash -c "cd frontend_react && npm run dev; exec bash" 2>/dev/null || \
osascript -e 'tell app "Terminal" to do script "cd frontend_react && npm run dev"' 2>/dev/null || \
xterm -e "cd frontend_react && npm run dev" &

cd ..

echo ""
echo "[5/6] Creating startup script..."
echo ""
echo "============================================"
echo " Setup Complete!"
echo "============================================"
echo ""
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:3000"
echo "API Docs: http://localhost:8000/docs"
echo ""
echo "Note: To stop the servers, close the terminal windows"
echo ""

sleep 3

# Open browser to frontend
if command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:3000
elif command -v open &> /dev/null; then
    open http://localhost:3000
fi

echo ""
echo "Setup complete! The application should be running."


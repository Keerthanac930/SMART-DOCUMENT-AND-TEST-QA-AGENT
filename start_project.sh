#!/bin/bash

echo "🚀 Starting QA Agent Project..."
echo "=========================================="
echo "This script will start both backend and frontend servers"
echo "=========================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed or not in PATH"
    echo "Please install Python 3.10+ and try again"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed or not in PATH"
    echo "Please install Node.js 18+ and try again"
    exit 1
fi

echo "✅ Python and Node.js are installed"
echo "=========================================="

# Make the script executable
chmod +x start_project.py

# Start the project
python3 start_project.py

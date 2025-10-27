#!/bin/bash

echo "🚀 Starting Smart Document QA Agent..."
echo

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed or not in PATH"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

# Check if requirements are installed
echo "📦 Checking dependencies..."
python3 -c "import streamlit" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📦 Installing dependencies..."
    python3 -m pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install dependencies"
        exit 1
    fi
fi

# Create necessary directories
mkdir -p vector_db embeddings_cache uploads

# Check for API key
if [ -z "$GOOGLE_AI_API_KEY" ]; then
    echo "⚠️  No Google AI API key found"
    echo "   The app will run in limited mode"
    echo "   Set GOOGLE_AI_API_KEY environment variable for full functionality"
    echo
fi

# Start the application
echo "🚀 Starting application..."
echo "📱 Open your browser to http://localhost:8501"
echo
python3 run.py

#!/usr/bin/env python3
"""
Main runner for Smart Document QA Agent
Choose between Frontend (Streamlit) or Backend (Flask API)
"""
import subprocess
import sys
import os

def run_frontend():
    """Run the Streamlit frontend"""
    print("🚀 Starting Frontend (Streamlit)...")
    os.chdir('frontend')
    os.environ['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'
    subprocess.run([sys.executable, '-m', 'streamlit', 'run', 'app.py', '--server.headless', 'true'])

def run_backend():
    """Run the Flask backend API"""
    print("🚀 Starting Backend (Flask API)...")
    os.chdir('backend')
    subprocess.run([sys.executable, 'api.py'])

def main():
    """Main runner - Start Frontend directly"""
    print("📚 Smart Document QA Agent - Starting Frontend...")
    run_frontend()

if __name__ == "__main__":
    main()

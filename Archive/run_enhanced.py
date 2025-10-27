#!/usr/bin/env python3
"""
Enhanced runner for Smart Document QA Agent
"""
import subprocess
import sys
import os
import time
import webbrowser
from threading import Thread

def run_backend():
    """Run the enhanced backend API"""
    print("🚀 Starting Enhanced Backend API...")
    os.chdir('backend')
    try:
        subprocess.run([sys.executable, 'enhanced_api.py'])
    except KeyboardInterrupt:
        print("Backend stopped")

def run_frontend():
    """Run the enhanced frontend"""
    print("🚀 Starting Enhanced Frontend...")
    time.sleep(3)  # Wait for backend to start
    os.chdir('frontend')
    os.environ['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'
    try:
        subprocess.run([sys.executable, '-m', 'streamlit', 'run', 'enhanced_app.py', '--server.headless', 'true'])
    except KeyboardInterrupt:
        print("Frontend stopped")

def open_browser():
    """Open browser after delay"""
    time.sleep(5)
    try:
        webbrowser.open('http://localhost:8501')
    except:
        pass

def main():
    """Main runner"""
    print("🤖 Enhanced QA Agent - Starting...")
    print("Features: Images, Voice, Google Drive, Mobile Support")
    print("=" * 60)
    
    # Start backend in background
    backend_thread = Thread(target=run_backend, daemon=True)
    backend_thread.start()
    
    # Open browser
    browser_thread = Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    # Start frontend (main process)
    try:
        run_frontend()
    except KeyboardInterrupt:
        print("\n👋 Enhanced QA Agent stopped")

if __name__ == "__main__":
    main()

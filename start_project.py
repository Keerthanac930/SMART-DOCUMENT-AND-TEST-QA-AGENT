#!/usr/bin/env python3
"""
Simple startup script for QA Agent project
This script will start both backend and frontend automatically
"""
import os
import sys
import subprocess
import time
import threading
from pathlib import Path

def run_backend():
    """Run the backend server"""
    print("Starting backend server...")
    backend_path = Path("backend_fastapi")
    
    if not backend_path.exists():
        print("Backend directory not found!")
        return False
    
    try:
        # Change to backend directory and run
        os.chdir(backend_path)
        
        # Check if virtual environment exists
        venv_path = Path("venv")
        if not venv_path.exists():
            print("Creating virtual environment...")
            subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        
        # Determine the correct python executable
        if os.name == 'nt':  # Windows
            python_exe = venv_path / "Scripts" / "python.exe"
            pip_exe = venv_path / "Scripts" / "pip.exe"
        else:  # Linux/macOS
            python_exe = venv_path / "bin" / "python"
            pip_exe = venv_path / "bin" / "pip"
        
        # Install dependencies
        print("Installing backend dependencies...")
        subprocess.run([str(pip_exe), "install", "-r", "requirements.txt"], check=True)
        
        # Run the backend
        print("Starting backend server...")
        subprocess.run([str(python_exe), "run_simple.py"], check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"Backend error: {e}")
        return False
    except KeyboardInterrupt:
        print("\nBackend stopped by user")
        return True

def run_frontend():
    """Run the frontend server"""
    print("Starting frontend server...")
    frontend_path = Path("frontend_react")
    
    if not frontend_path.exists():
        print("Frontend directory not found!")
        return False
    
    try:
        # Change to frontend directory
        os.chdir(frontend_path)
        
        # Install dependencies if needed
        node_modules = Path("node_modules")
        if not node_modules.exists():
            print("Installing frontend dependencies...")
            subprocess.run(["npm", "install"], check=True)
        
        # Run the frontend
        print("Starting frontend server...")
        subprocess.run(["npm", "run", "dev"], check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"Frontend error: {e}")
        return False
    except KeyboardInterrupt:
        print("\nFrontend stopped by user")
        return True

def main():
    """Main function"""
    print("Starting QA Agent Project...")
    print("=" * 60)
    print("This script will start both backend and frontend servers")
    print("=" * 60)
    
    # Get the project root directory
    project_root = Path(__file__).parent
    
    # Check if we're in the right directory
    if not (project_root / "backend_fastapi").exists():
        print("Please run this script from the project root directory")
        print("   Make sure you have both 'backend_fastapi' and 'frontend_react' folders")
        return
    
    print("Project structure found!")
    print("Backend: backend_fastapi/")
    print("Frontend: frontend_react/")
    print("=" * 60)
    
    # Start backend in a separate thread
    backend_thread = threading.Thread(target=run_backend)
    backend_thread.daemon = True
    backend_thread.start()
    
    # Wait a bit for backend to start
    print("Waiting for backend to start...")
    time.sleep(5)
    
    # Start frontend
    try:
        run_frontend()
    except KeyboardInterrupt:
        print("\nProject stopped by user")
        print("=" * 60)
        print("Thank you for using QA Agent!")
        print("=" * 60)

if __name__ == "__main__":
    main()

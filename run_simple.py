#!/usr/bin/env python3
"""
Simple startup script for QA Agent project - PowerShell compatible
"""
import os
import sys
import subprocess
import time
from pathlib import Path

def check_requirements():
    """Check if Python and Node.js are installed"""
    print("Checking requirements...")
    
    # Check Python
    try:
        python_version = subprocess.check_output([sys.executable, "--version"], text=True)
        print(f"Python: {python_version.strip()}")
    except:
        print("Python not found!")
        return False
    
    # Check Node.js
    try:
        node_version = subprocess.check_output(["node", "--version"], text=True)
        print(f"Node.js: {node_version.strip()}")
    except:
        print("Node.js not found!")
        return False
    
    return True

def setup_backend():
    """Setup and run backend"""
    print("\nSetting up backend...")
    
    backend_path = Path("backend_fastapi")
    if not backend_path.exists():
        print("Backend directory not found!")
        return False
    
    try:
        os.chdir(backend_path)
        
        # Create virtual environment
        venv_path = Path("venv")
        if not venv_path.exists():
            print("Creating virtual environment...")
            subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        
        # Install dependencies
        print("Installing backend dependencies...")
        if os.name == 'nt':  # Windows
            pip_exe = venv_path / "Scripts" / "pip.exe"
        else:  # Linux/macOS
            pip_exe = venv_path / "bin" / "pip"
        
        subprocess.run([str(pip_exe), "install", "-r", "requirements_simple.txt"], check=True)
        
        # Run backend
        print("Starting backend server...")
        if os.name == 'nt':  # Windows
            python_exe = venv_path / "Scripts" / "python.exe"
        else:  # Linux/macOS
            python_exe = venv_path / "bin" / "python"
        
        subprocess.run([str(python_exe), "run_simple.py"], check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"Backend error: {e}")
        return False
    except KeyboardInterrupt:
        print("\nBackend stopped by user")
        return True

def setup_frontend():
    """Setup and run frontend"""
    print("\nSetting up frontend...")
    
    frontend_path = Path("frontend_react")
    if not frontend_path.exists():
        print("Frontend directory not found!")
        return False
    
    try:
        os.chdir(frontend_path)
        
        # Install dependencies
        node_modules = Path("node_modules")
        if not node_modules.exists():
            print("Installing frontend dependencies...")
            subprocess.run(["npm", "install"], check=True)
        
        # Run frontend
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
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        print("Please install Python 3.10+ and Node.js 18+")
        return
    
    print("\nRequirements check passed!")
    print("=" * 50)
    
    # Check project structure
    project_root = Path(__file__).parent
    if not (project_root / "backend_fastapi").exists():
        print("Please run this script from the project root directory")
        print("Make sure you have both 'backend_fastapi' and 'frontend_react' folders")
        return
    
    print("Project structure found!")
    print("=" * 50)
    
    # Start backend
    try:
        setup_backend()
    except KeyboardInterrupt:
        print("\nProject stopped by user")
        print("Thank you for using QA Agent!")

if __name__ == "__main__":
    main()

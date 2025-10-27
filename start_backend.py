#!/usr/bin/env python3
"""
Backend starter script for Enhanced QA Agent
Ensures proper startup and error handling
"""
import os
import sys
import subprocess
import time
import requests
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    required_modules = [
        'flask', 'flask_cors', 'google.generativeai', 
        'sentence_transformers', 'faiss', 'numpy', 'pandas'
    ]
    
    missing_modules = []
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError:
            missing_modules.append(module)
            print(f"❌ {module}")
    
    if missing_modules:
        print(f"\n❌ Missing dependencies: {', '.join(missing_modules)}")
        print("Please install with: pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies available")
    return True

def check_config():
    """Check configuration files"""
    print("\n🔧 Checking configuration...")
    
    # Check if backend directory exists
    if not os.path.exists('backend'):
        print("❌ Backend directory not found")
        return False
    
    # Check if enhanced_api.py exists
    if not os.path.exists('backend/enhanced_api.py'):
        print("❌ enhanced_api.py not found in backend directory")
        return False
    
    # Check .env file
    if not os.path.exists('.env'):
        print("⚠️  .env file not found - creating template...")
        create_env_template()
    
    print("✅ Configuration OK")
    return True

def create_env_template():
    """Create .env template"""
    env_content = """# Google AI API Key (required for full functionality)
GOOGLE_AI_API_KEY=your_api_key_here

# Google Drive API (optional)
GOOGLE_DRIVE_API_KEY=your_drive_api_key
GOOGLE_DRIVE_CLIENT_ID=your_client_id
GOOGLE_DRIVE_CLIENT_SECRET=your_client_secret
GOOGLE_DRIVE_FOLDER_ID=your_folder_id
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Created .env template")

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    
    directories = ['vector_db', 'uploads', 'temp', 'embeddings_cache']
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ {directory}/")

def start_backend():
    """Start the backend server"""
    print("\n🚀 Starting Enhanced QA Agent Backend...")
    
    # Change to backend directory
    os.chdir('backend')
    
    try:
        # Start the server
        process = subprocess.Popen(
            [sys.executable, 'enhanced_api.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        print("⏳ Waiting for server to start...")
        
        # Wait for server to be ready
        for i in range(30):  # Wait up to 30 seconds
            try:
                response = requests.get('http://localhost:5000/api/health', timeout=2)
                if response.status_code == 200:
                    print("✅ Backend server started successfully!")
                    print("🌐 API available at: http://localhost:5000")
                    print("📖 Health check: http://localhost:5000/api/health")
                    return process
            except:
                time.sleep(1)
                print(f"⏳ Waiting... ({i+1}/30)")
        
        print("❌ Server failed to start within 30 seconds")
        process.terminate()
        return None
        
    except Exception as e:
        print(f"❌ Error starting backend: {e}")
        return None

def main():
    """Main function"""
    print("🤖 Enhanced QA Agent - Backend Starter")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check configuration
    if not check_config():
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Start backend
    process = start_backend()
    
    if process:
        try:
            print("\n📝 Backend is running. Press Ctrl+C to stop.")
            print("🔗 You can now start the frontend with: streamlit run frontend/enhanced_app.py")
            process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Stopping backend server...")
            process.terminate()
            print("✅ Backend stopped")
    else:
        print("\n❌ Failed to start backend")
        sys.exit(1)

if __name__ == "__main__":
    main()

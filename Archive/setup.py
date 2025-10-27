#!/usr/bin/env python3
"""
Setup script for Smart Document QA Agent
"""
import subprocess
import sys
import os

def install_requirements():
    """Install all required packages"""
    print("📦 Installing requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False

def setup_directories():
    """Create necessary directories"""
    print("📁 Creating directories...")
    directories = [
        "vector_db",
        "embeddings_cache", 
        "uploads"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created directory: {directory}")
    
    return True

def check_api_key():
    """Check if Google AI API key is set"""
    api_key = os.getenv('GOOGLE_AI_API_KEY')
    if api_key:
        print("✅ Google AI API key found")
        return True
    else:
        print("⚠️  Google AI API key not found")
        print("   Set it with: $env:GOOGLE_AI_API_KEY='your-api-key-here' (PowerShell)")
        print("   Or: export GOOGLE_AI_API_KEY='your-api-key-here' (Linux/Mac)")
        return False

def main():
    """Main setup function"""
    print("🚀 Setting up Smart Document QA Agent")
    print("=" * 50)
    
    # Install requirements
    if not install_requirements():
        return False
    
    # Setup directories
    if not setup_directories():
        return False
    
    # Check API key
    has_api_key = check_api_key()
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed!")
    
    if has_api_key:
        print("✅ Ready to run with full AI capabilities")
    else:
        print("⚠️  Ready to run in limited mode (no AI answers)")
        print("   Add your Google AI API key for full functionality")
    
    print("\n🚀 To start the application:")
    print("   python run.py")
    print("   or")
    print("   streamlit run frontend/app.py")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

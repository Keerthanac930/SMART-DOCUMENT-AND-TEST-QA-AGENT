#!/usr/bin/env python3
"""
Enhanced setup script for Smart Document QA Agent
"""
import os
import sys
import subprocess
import platform

def install_requirements():
    """Install requirements"""
    print("📦 Installing requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    print("📁 Creating directories...")
    directories = [
        "vector_db",
        "uploads", 
        "temp",
        "embeddings_cache"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created {directory}/")

def setup_environment():
    """Setup environment variables"""
    print("🔧 Setting up environment...")
    
    env_example = """# Google AI API Key (required for full functionality)
GOOGLE_AI_API_KEY=your_api_key_here

# Google Drive API (optional)
GOOGLE_DRIVE_API_KEY=your_drive_api_key
GOOGLE_DRIVE_CLIENT_ID=your_client_id
GOOGLE_DRIVE_CLIENT_SECRET=your_client_secret
GOOGLE_DRIVE_FOLDER_ID=your_folder_id
"""
    
    if not os.path.exists('.env'):
        with open('.env', 'w') as f:
            f.write(env_example)
        print("✅ Created .env file")
        print("⚠️  Please edit .env file with your API keys")
    else:
        print("✅ .env file already exists")

def check_system_requirements():
    """Check system requirements"""
    print("🔍 Checking system requirements...")
    
    # Check Python version
    python_version = sys.version_info
    if python_version < (3, 8):
        print("❌ Python 3.8 or higher required")
        return False
    print(f"✅ Python {python_version.major}.{python_version.minor}")
    
    # Check platform
    system = platform.system()
    print(f"✅ Platform: {system}")
    
    return True

def create_credentials_template():
    """Create Google Drive credentials template"""
    print("📋 Creating Google Drive credentials template...")
    
    credentials_template = {
        "installed": {
            "client_id": "your_client_id_here",
            "project_id": "your_project_id",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_secret": "your_client_secret_here",
            "redirect_uris": ["http://localhost"]
        }
    }
    
    if not os.path.exists('backend/credentials.json'):
        import json
        with open('backend/credentials.json', 'w') as f:
            json.dump(credentials_template, f, indent=2)
        print("✅ Created backend/credentials.json template")
        print("⚠️  Please replace with your actual Google Drive credentials")
    else:
        print("✅ credentials.json already exists")

def main():
    """Main setup function"""
    print("🚀 Enhanced QA Agent Setup")
    print("=" * 50)
    
    # Check system requirements
    if not check_system_requirements():
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Setup environment
    setup_environment()
    
    # Create credentials template
    create_credentials_template()
    
    # Install requirements
    if install_requirements():
        print("\n🎉 Setup completed successfully!")
        print("\nNext steps:")
        print("1. Edit .env file with your API keys")
        print("2. Replace backend/credentials.json with your Google Drive credentials")
        print("3. Run: python run_enhanced.py")
    else:
        print("\n❌ Setup failed")
        sys.exit(1)

if __name__ == "__main__":
    main()

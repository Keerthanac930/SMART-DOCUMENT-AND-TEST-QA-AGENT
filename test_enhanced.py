#!/usr/bin/env python3
"""
Test script for Enhanced QA Agent
"""
import sys
import os
import requests
import time

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

def test_imports():
    """Test if all modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        from enhanced_document_processor import EnhancedDocumentProcessor
        print("✅ Enhanced Document Processor")
    except Exception as e:
        print(f"❌ Enhanced Document Processor: {e}")
    
    try:
        from voice_processor import VoiceProcessor
        print("✅ Voice Processor")
    except Exception as e:
        print(f"❌ Voice Processor: {e}")
    
    try:
        from google_drive_manager import GoogleDriveManager
        print("✅ Google Drive Manager")
    except Exception as e:
        print(f"❌ Google Drive Manager: {e}")
    
    try:
        from enhanced_qa_engine import EnhancedQAEngine
        print("✅ Enhanced QA Engine")
    except Exception as e:
        print(f"❌ Enhanced QA Engine: {e}")

def test_qa_engine():
    """Test QA Engine initialization"""
    print("\n🤖 Testing QA Engine...")
    
    try:
        from enhanced_qa_engine import EnhancedQAEngine
        engine = EnhancedQAEngine()
        
        capabilities = engine.get_capabilities()
        print("✅ QA Engine initialized")
        print(f"   - Image processing: {capabilities['document_processing']['image_processing']}")
        print(f"   - Voice chat: {capabilities['voice_processing']['voice_chat_enabled']}")
        print(f"   - Google Drive: {capabilities['google_drive']['enabled']}")
        
    except Exception as e:
        print(f"❌ QA Engine test failed: {e}")

def test_api_server():
    """Test if API server can start"""
    print("\n🌐 Testing API Server...")
    
    try:
        import subprocess
        import threading
        import time
        
        # Start server in background
        def start_server():
            os.chdir('backend')
            subprocess.run([sys.executable, 'enhanced_api.py'], 
                         capture_output=True, timeout=5)
        
        server_thread = threading.Thread(target=start_server, daemon=True)
        server_thread.start()
        
        # Wait for server to start
        time.sleep(3)
        
        # Test health endpoint
        try:
            response = requests.get('http://localhost:5000/api/health', timeout=5)
            if response.status_code == 200:
                print("✅ API Server responding")
                data = response.json()
                print(f"   - Status: {data.get('status')}")
                print(f"   - Message: {data.get('message')}")
            else:
                print(f"❌ API Server error: {response.status_code}")
        except requests.exceptions.RequestException:
            print("❌ API Server not responding")
            
    except Exception as e:
        print(f"❌ API Server test failed: {e}")

def test_file_types():
    """Test supported file types"""
    print("\n📁 Testing file type support...")
    
    try:
        from config import SUPPORTED_FILE_TYPES
        
        print(f"✅ Supported file types: {len(SUPPORTED_FILE_TYPES)}")
        
        # Group by type
        docs = [ext for ext in SUPPORTED_FILE_TYPES if ext in ['.pdf', '.txt', '.docx', '.doc']]
        images = [ext for ext in SUPPORTED_FILE_TYPES if ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']]
        audio = [ext for ext in SUPPORTED_FILE_TYPES if ext in ['.mp3', '.wav', '.m4a', '.aac', '.ogg', '.flac']]
        
        print(f"   - Documents: {docs}")
        print(f"   - Images: {images}")
        print(f"   - Audio: {audio}")
        
    except Exception as e:
        print(f"❌ File types test failed: {e}")

def main():
    """Run all tests"""
    print("🧪 Enhanced QA Agent - Test Suite")
    print("=" * 50)
    
    test_imports()
    test_qa_engine()
    test_file_types()
    test_api_server()
    
    print("\n🎉 Test completed!")
    print("\nTo run the enhanced version:")
    print("1. python setup_enhanced.py")
    print("2. Edit .env file with your API keys")
    print("3. python run_enhanced.py")

if __name__ == "__main__":
    main()

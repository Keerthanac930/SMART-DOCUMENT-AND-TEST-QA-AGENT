#!/usr/bin/env python3
"""
Test connection between frontend and backend
"""
import requests
import time
import subprocess
import sys
import os

def test_backend_connection():
    """Test if backend is running"""
    print("🔍 Testing backend connection...")
    
    try:
        response = requests.get('http://localhost:5000/api/health', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Backend is running!")
            print(f"   Status: {data.get('status')}")
            print(f"   Message: {data.get('message')}")
            return True
        else:
            print(f"❌ Backend responded with status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend")
        print("   Make sure the backend is running on http://localhost:5000")
        return False
    except Exception as e:
        print(f"❌ Error testing connection: {e}")
        return False

def start_backend():
    """Start backend if not running"""
    print("\n🚀 Starting backend server...")
    
    try:
        # Change to backend directory and start server
        os.chdir('backend')
        process = subprocess.Popen(
            [sys.executable, 'enhanced_api.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait for server to start
        print("⏳ Waiting for server to start...")
        for i in range(15):
            time.sleep(1)
            if test_backend_connection():
                print("✅ Backend started successfully!")
                return process
            print(f"   Waiting... ({i+1}/15)")
        
        print("❌ Backend failed to start within 15 seconds")
        process.terminate()
        return None
        
    except Exception as e:
        print(f"❌ Error starting backend: {e}")
        return None

def test_api_endpoints():
    """Test various API endpoints"""
    print("\n🧪 Testing API endpoints...")
    
    endpoints = [
        ('/health', 'GET', None),
        ('/documents', 'GET', None),
        ('/capabilities', 'GET', None),
        ('/stats', 'GET', None),
    ]
    
    for endpoint, method, data in endpoints:
        try:
            url = f'http://localhost:5000/api{endpoint}'
            if method == 'GET':
                response = requests.get(url, timeout=5)
            elif method == 'POST':
                response = requests.post(url, json=data, timeout=5)
            
            if response.status_code == 200:
                print(f"✅ {endpoint} - OK")
            else:
                print(f"⚠️  {endpoint} - Status {response.status_code}")
                
        except Exception as e:
            print(f"❌ {endpoint} - Error: {e}")

def main():
    """Main test function"""
    print("🔧 Frontend-Backend Connection Test")
    print("=" * 40)
    
    # Test if backend is already running
    if test_backend_connection():
        test_api_endpoints()
        print("\n✅ Backend is working properly!")
        print("You can now run the frontend:")
        print("   streamlit run frontend/enhanced_app.py")
    else:
        print("\n🔄 Backend not running, attempting to start...")
        process = start_backend()
        
        if process:
            test_api_endpoints()
            print("\n✅ Backend started and working!")
            print("You can now run the frontend:")
            print("   streamlit run frontend/enhanced_app.py")
            print("\nPress Ctrl+C to stop the backend")
            
            try:
                process.wait()
            except KeyboardInterrupt:
                print("\n🛑 Stopping backend...")
                process.terminate()
        else:
            print("\n❌ Failed to start backend")
            print("Please check the error messages above")
            print("\nManual start:")
            print("   cd backend")
            print("   python enhanced_api.py")

if __name__ == "__main__":
    main()

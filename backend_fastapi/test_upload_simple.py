"""
Simple test to verify upload endpoint works
"""
import requests

# Test health
print("Testing backend health...")
response = requests.get("http://localhost:8000/api/health")
print(f"Health: {response.json()}")

# Test login to get token
print("\nTesting login...")
login_response = requests.post("http://localhost:8000/api/auth/login", json={
    "email": "test@test.com",
    "password": "password123"
})

if login_response.status_code == 200:
    token = login_response.json()['access_token']
    print(f"✅ Got token: {token[:20]}...")
    
    # Test upload
    print("\nTesting upload...")
    files = {'file': open('uploads/test_doc.txt', 'rb')}
    headers = {'Authorization': f'Bearer {token}'}
    
    upload_response = requests.post(
        "http://localhost:8000/api/user/documents",
        files=files,
        headers=headers
    )
    
    print(f"Upload status: {upload_response.status_code}")
    print(f"Upload response: {upload_response.text}")
else:
    print(f"❌ Login failed: {login_response.status_code}")
    print(f"Response: {login_response.text}")

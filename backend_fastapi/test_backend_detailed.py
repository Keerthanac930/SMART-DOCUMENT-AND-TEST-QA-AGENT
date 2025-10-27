"""
Comprehensive Backend Testing Script
Tests document upload, processing, and AI functionality
"""
import os
import sys
import requests
import json
from pathlib import Path

# API Configuration
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api"

class BackendTester:
    def __init__(self):
        self.session = requests.Session()
        self.token = None
        self.user_id = None
        self.test_results = []
        
    def log(self, message, status="INFO"):
        """Log test results"""
        color = {
            "INFO": "\033[94m",  # Blue
            "SUCCESS": "\033[92m",  # Green
            "ERROR": "\033[91m",  # Red
            "WARNING": "\033[93m"  # Yellow
        }
        reset = "\033[0m"
        print(f"{color.get(status, '')}{status}: {message}{reset}")
        
    def test_health_check(self):
        """Test if backend is running"""
        self.log("Testing backend health...", "INFO")
        try:
            response = requests.get(f"{API_BASE}/health", timeout=5)
            if response.status_code == 200:
                self.log("✓ Backend is running and healthy", "SUCCESS")
                return True
            else:
                self.log(f"✗ Backend health check failed: {response.status_code}", "ERROR")
                return False
        except Exception as e:
            self.log(f"✗ Cannot connect to backend: {str(e)}", "ERROR")
            return False
    
    def test_user_registration(self):
        """Test user registration"""
        self.log("Testing user registration...", "INFO")
        try:
            test_user = {
                "username": "testuser123",
                "email": "test123@example.com",
                "password": "test123",
                "role": "student"
            }
            
            response = requests.post(f"{API_BASE}/auth/register", json=test_user)
            
            if response.status_code == 200:
                data = response.json()
                self.token = data.get("access_token")
                self.session.headers.update({"Authorization": f"Bearer {self.token}"})
                self.log(f"✓ User registered successfully", "SUCCESS")
                return True
            elif response.status_code == 400:
                # User might already exist, try login
                self.log("User already exists, attempting login...", "WARNING")
                return self.test_user_login()
            else:
                self.log(f"✗ Registration failed: {response.text}", "ERROR")
                return False
        except Exception as e:
            self.log(f"✗ Registration error: {str(e)}", "ERROR")
            return False
    
    def test_user_login(self):
        """Test user login"""
        self.log("Testing user login...", "INFO")
        try:
            login_data = {
                "email": "test123@example.com",
                "password": "test123"
            }
            
            response = requests.post(f"{API_BASE}/auth/login", json=login_data)
            
            if response.status_code == 200:
                data = response.json()
                self.token = data.get("access_token")
                self.session.headers.update({"Authorization": f"Bearer {self.token}"})
                self.log(f"✓ User logged in successfully", "SUCCESS")
                return True
            else:
                self.log(f"✗ Login failed: {response.text}", "ERROR")
                return False
        except Exception as e:
            self.log(f"✗ Login error: {str(e)}", "ERROR")
            return False
    
    def test_document_upload(self):
        """Test document upload"""
        self.log("Testing document upload...", "INFO")
        try:
            # Create a test document
            test_file_path = "test_document.txt"
            test_content = """
            Artificial Intelligence in Business
            
            Artificial Intelligence (AI) is transforming the business landscape. 
            Companies are using AI for customer service, data analysis, and automation.
            Machine learning algorithms help businesses predict trends and make better decisions.
            Natural language processing enables chatbots to interact with customers.
            Computer vision is used in quality control and security systems.
            """
            
            with open(test_file_path, "w") as f:
                f.write(test_content)
            
            # Upload the document
            with open(test_file_path, "rb") as f:
                files = {"file": (test_file_path, f, "text/plain")}
                response = self.session.post(f"{API_BASE}/user/documents", files=files)
            
            # Clean up
            os.remove(test_file_path)
            
            if response.status_code == 200:
                data = response.json()
                self.document_id = data.get("id")
                self.log(f"✓ Document uploaded successfully (ID: {self.document_id})", "SUCCESS")
                self.log(f"  File path: {data.get('file_path')}", "INFO")
                return True
            else:
                self.log(f"✗ Document upload failed: {response.text}", "ERROR")
                return False
        except Exception as e:
            self.log(f"✗ Document upload error: {str(e)}", "ERROR")
            if os.path.exists(test_file_path):
                os.remove(test_file_path)
            return False
    
    def test_document_processing(self):
        """Test if document processing is working"""
        self.log("Testing document processing...", "INFO")
        try:
            if not hasattr(self, 'document_id'):
                self.log("✗ No document ID available", "ERROR")
                return False
            
            # Try to get document info
            response = self.session.get(f"{API_BASE}/user/documents")
            
            if response.status_code == 200:
                documents = response.json()
                if documents:
                    doc = next((d for d in documents if d['id'] == self.document_id), None)
                    if doc:
                        self.log(f"✓ Document found in database", "SUCCESS")
                        self.log(f"  Name: {doc.get('doc_name')}", "INFO")
                        self.log(f"  Processed: {doc.get('is_processed')}", "INFO")
                        self.log(f"  Words: {doc.get('total_words')}", "INFO")
                        self.log(f"  Pages: {doc.get('total_pages')}", "INFO")
                        
                        if not doc.get('is_processed'):
                            self.log("⚠ Document not yet processed!", "WARNING")
                            self.log("  This is the issue - documents aren't being processed automatically", "WARNING")
                            return False
                        return True
                    else:
                        self.log("✗ Document not found", "ERROR")
                        return False
                else:
                    self.log("✗ No documents found", "ERROR")
                    return False
            else:
                self.log(f"✗ Failed to get documents: {response.text}", "ERROR")
                return False
        except Exception as e:
            self.log(f"✗ Document processing check error: {str(e)}", "ERROR")
            return False
    
    def test_ai_question(self):
        """Test AI question answering"""
        self.log("Testing AI question answering...", "INFO")
        try:
            question_data = {
                "question": "What is artificial intelligence?",
                "document_ids": []
            }
            
            response = self.session.post(f"{API_BASE}/ai/ask", json=question_data)
            
            if response.status_code == 200:
                data = response.json()
                self.log(f"✓ AI question answered successfully", "SUCCESS")
                self.log(f"  Answer: {data.get('answer')[:100]}...", "INFO")
                self.log(f"  Source: {data.get('source')}", "INFO")
                self.log(f"  Confidence: {data.get('confidence')}", "INFO")
                return True
            else:
                self.log(f"✗ AI question failed: {response.text}", "ERROR")
                return False
        except Exception as e:
            self.log(f"✗ AI question error: {str(e)}", "ERROR")
            return False
    
    def test_ai_with_document(self):
        """Test AI question with document context"""
        self.log("Testing AI with document context...", "INFO")
        try:
            if not hasattr(self, 'document_id'):
                self.log("✗ No document ID available", "ERROR")
                return False
            
            question_data = {
                "question": "How is AI used in business?",
                "document_ids": [self.document_id]
            }
            
            response = self.session.post(f"{API_BASE}/ai/ask", json=question_data)
            
            if response.status_code == 200:
                data = response.json()
                self.log(f"✓ AI answered with document context", "SUCCESS")
                self.log(f"  Answer: {data.get('answer')[:100]}...", "INFO")
                self.log(f"  Source: {data.get('source')}", "INFO")
                self.log(f"  Citations: {data.get('citations')}", "INFO")
                return True
            else:
                self.log(f"✗ AI with document failed: {response.text}", "ERROR")
                return False
        except Exception as e:
            self.log(f"✗ AI with document error: {str(e)}", "ERROR")
            return False
    
    def run_all_tests(self):
        """Run all tests"""
        self.log("=" * 60, "INFO")
        self.log("STARTING COMPREHENSIVE BACKEND TESTS", "INFO")
        self.log("=" * 60, "INFO")
        
        tests = [
            ("Health Check", self.test_health_check),
            ("User Registration", self.test_user_registration),
            ("Document Upload", self.test_document_upload),
            ("Document Processing", self.test_document_processing),
            ("AI Question (General)", self.test_ai_question),
            ("AI Question (with Document)", self.test_ai_with_document),
        ]
        
        passed = 0
        failed = 0
        
        for test_name, test_func in tests:
            try:
                result = test_func()
                if result:
                    passed += 1
                else:
                    failed += 1
                print()  # Blank line between tests
            except Exception as e:
                self.log(f"✗ Test '{test_name}' crashed: {str(e)}", "ERROR")
                failed += 1
                print()
        
        # Summary
        self.log("=" * 60, "INFO")
        self.log("TEST SUMMARY", "INFO")
        self.log("=" * 60, "INFO")
        self.log(f"Total Tests: {passed + failed}", "INFO")
        self.log(f"Passed: {passed}", "SUCCESS")
        self.log(f"Failed: {failed}", "ERROR" if failed > 0 else "INFO")
        
        if failed > 0:
            self.log("\n⚠ IDENTIFIED ISSUES:", "WARNING")
            self.log("1. Documents are uploading but not being processed automatically", "WARNING")
            self.log("2. Need to add automatic document processing after upload", "WARNING")
            self.log("3. Vector database embeddings not being created", "WARNING")

if __name__ == "__main__":
    tester = BackendTester()
    tester.run_all_tests()


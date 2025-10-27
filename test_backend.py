#!/usr/bin/env python3
"""
Test script for Smart Document QA Agent backend components
"""
import sys
import os
sys.path.append('backend')

def test_imports():
    """Test if all backend modules can be imported"""
    try:
        from qa_engine import QAEngine
        from document_processor import DocumentProcessor
        from embedding_manager import EmbeddingManager
        from vector_database import VectorDatabase
        from config import GOOGLE_AI_API_KEY, MODEL_NAME
        
        print("✅ All backend modules imported successfully")
        return True
    except Exception as e:
        print(f"❌ Import error: {str(e)}")
        return False

def test_qa_engine():
    """Test QA Engine initialization"""
    try:
        from qa_engine import QAEngine
        
        # Test without API key
        qa_engine = QAEngine()
        print("✅ QA Engine initialized without API key")
        
        # Test with API key (if available)
        if os.getenv('GOOGLE_AI_API_KEY'):
            qa_engine = QAEngine(api_key=os.getenv('GOOGLE_AI_API_KEY'))
            print("✅ QA Engine initialized with API key")
        else:
            print("⚠️  No Google AI API key found - using limited mode")
        
        return True
    except Exception as e:
        print(f"❌ QA Engine error: {str(e)}")
        return False

def test_document_processor():
    """Test Document Processor"""
    try:
        from document_processor import DocumentProcessor
        
        processor = DocumentProcessor()
        print("✅ Document Processor initialized")
        
        # Test supported extensions
        print(f"✅ Supported extensions: {processor.supported_extensions}")
        
        return True
    except Exception as e:
        print(f"❌ Document Processor error: {str(e)}")
        return False

def test_embedding_manager():
    """Test Embedding Manager"""
    try:
        from embedding_manager import EmbeddingManager
        
        manager = EmbeddingManager()
        print("✅ Embedding Manager initialized")
        
        # Test model info
        info = manager.get_model_info()
        print(f"✅ Model info: {info['model_name']}")
        
        return True
    except Exception as e:
        print(f"❌ Embedding Manager error: {str(e)}")
        return False

def test_vector_database():
    """Test Vector Database"""
    try:
        from vector_database import VectorDatabase
        
        db = VectorDatabase()
        print("✅ Vector Database initialized")
        
        # Test stats
        stats = db.get_database_stats()
        print(f"✅ Database stats: {stats['document_count']} documents")
        
        return True
    except Exception as e:
        print(f"❌ Vector Database error: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Smart Document QA Agent Backend Components")
    print("=" * 60)
    
    tests = [
        ("Import Test", test_imports),
        ("QA Engine Test", test_qa_engine),
        ("Document Processor Test", test_document_processor),
        ("Embedding Manager Test", test_embedding_manager),
        ("Vector Database Test", test_vector_database)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name}...")
        if test_func():
            passed += 1
        print("-" * 40)
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Backend is ready to use.")
    else:
        print("⚠️  Some tests failed. Check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

"""
Quick script to check backend status and identify issues
"""
import os
import sys
from database import SessionLocal
from models import Document, User, Test, Question
from pathlib import Path

def check_backend_status():
    """Check the status of backend components"""
    
    print("=" * 70)
    print("BACKEND STATUS CHECK")
    print("=" * 70)
    
    # 1. Check database connection
    print("\n1. DATABASE CONNECTION")
    print("-" * 70)
    try:
        db = SessionLocal()
        print("✓ Database connection successful")
        
        # Check tables
        user_count = db.query(User).count()
        doc_count = db.query(Document).count()
        test_count = db.query(Test).count()
        question_count = db.query(Question).count()
        
        print(f"  - Users: {user_count}")
        print(f"  - Documents: {doc_count}")
        print(f"  - Tests: {test_count}")
        print(f"  - Questions: {question_count}")
        
    except Exception as e:
        print(f"✗ Database connection failed: {str(e)}")
        db = None
    
    # 2. Check document processing
    if db:
        print("\n2. DOCUMENT PROCESSING STATUS")
        print("-" * 70)
        
        documents = db.query(Document).all()
        processed = sum(1 for d in documents if d.is_processed)
        unprocessed = sum(1 for d in documents if not d.is_processed)
        
        print(f"  Total documents: {len(documents)}")
        print(f"  ✓ Processed: {processed}")
        print(f"  ✗ Unprocessed: {unprocessed}")
        
        if unprocessed > 0:
            print("\n  Unprocessed documents:")
            for doc in documents:
                if not doc.is_processed:
                    exists = os.path.exists(doc.file_path)
                    status = "✓ File exists" if exists else "✗ File missing"
                    print(f"    - ID {doc.id}: {doc.doc_name} ({status})")
        
        # Document details
        if documents:
            print("\n  All documents:")
            for doc in documents:
                print(f"    - ID {doc.id}: {doc.doc_name}")
                print(f"      Type: {doc.file_type}, Words: {doc.total_words}, Pages: {doc.total_pages}")
                print(f"      Processed: {doc.is_processed}, Path: {doc.file_path}")
    
    # 3. Check file system
    print("\n3. FILE SYSTEM CHECK")
    print("-" * 70)
    
    upload_dir = "uploads"
    if os.path.exists(upload_dir):
        files = os.listdir(upload_dir)
        print(f"  ✓ Upload directory exists: {upload_dir}")
        print(f"  Files in upload directory: {len(files)}")
        for f in files:
            size = os.path.getsize(os.path.join(upload_dir, f))
            print(f"    - {f} ({size} bytes)")
    else:
        print(f"  ✗ Upload directory does not exist: {upload_dir}")
    
    chroma_dir = "chroma_db"
    if os.path.exists(chroma_dir):
        print(f"  ✓ ChromaDB directory exists: {chroma_dir}")
        # List contents
        try:
            files = os.listdir(chroma_dir)
            print(f"    Files: {len(files)}")
        except:
            pass
    else:
        print(f"  ✗ ChromaDB directory does not exist: {chroma_dir}")
    
    # 4. Check AI configuration
    print("\n4. AI CONFIGURATION")
    print("-" * 70)
    
    from config import settings
    
    if settings.google_gemini_api_key:
        print(f"  ✓ Google Gemini API key configured")
        print(f"    Key: {settings.google_gemini_api_key[:20]}...")
    else:
        print(f"  ✗ Google Gemini API key NOT configured")
    
    print(f"  Embedding model: {settings.embedding_model}")
    print(f"  Vector DB path: {settings.vector_db_path}")
    
    # 5. Test AI functionality
    print("\n5. AI FUNCTIONALITY TEST")
    print("-" * 70)
    
    try:
        from utils.gemini_client import GeminiClient
        
        client = GeminiClient()
        print("  ✓ GeminiClient initialized successfully")
        
        # Try a simple query
        print("  Testing simple AI query...")
        response = client.generate_answer("What is 2+2?")
        if response and len(response) > 0:
            print(f"  ✓ AI response received: {response[:100]}...")
        else:
            print(f"  ✗ No AI response received")
    except Exception as e:
        print(f"  ✗ AI functionality test failed: {str(e)}")
    
    # 6. Test document processor
    print("\n6. DOCUMENT PROCESSOR TEST")
    print("-" * 70)
    
    try:
        from utils.document_processor import DocumentProcessor
        
        processor = DocumentProcessor()
        print("  ✓ DocumentProcessor initialized successfully")
        print(f"  Embedding model loaded: {processor.embedding_model}")
        print(f"  ChromaDB collection: {processor.collection.name}")
        
        # Check collection stats
        try:
            count = processor.collection.count()
            print(f"  ✓ Vector database has {count} embeddings")
        except:
            print(f"  ⚠ Could not get vector database count")
            
    except Exception as e:
        print(f"  ✗ DocumentProcessor test failed: {str(e)}")
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    issues = []
    
    if db is None:
        issues.append("Database connection failed")
    
    if db and unprocessed > 0:
        issues.append(f"{unprocessed} documents need processing")
    
    if not os.path.exists(chroma_dir):
        issues.append("ChromaDB directory not found")
    
    if not settings.google_gemini_api_key:
        issues.append("Google Gemini API key not configured")
    
    if issues:
        print("\n⚠ ISSUES FOUND:")
        for i, issue in enumerate(issues, 1):
            print(f"  {i}. {issue}")
        
        print("\n💡 RECOMMENDATIONS:")
        if unprocessed > 0:
            print("  - Run: python process_existing_documents.py")
        if not os.path.exists(chroma_dir):
            print("  - ChromaDB will be created on first document upload")
        if not settings.google_gemini_api_key:
            print("  - Add GOOGLE_GEMINI_API_KEY to .env file")
    else:
        print("\n✓ All systems operational!")
    
    if db:
        db.close()

if __name__ == "__main__":
    check_backend_status()


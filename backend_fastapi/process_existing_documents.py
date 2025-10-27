"""
Script to process all existing documents that haven't been processed yet
This will extract text, create embeddings, and update the database
"""
import os
import sys
from database import SessionLocal
from models import Document
from utils.document_processor import DocumentProcessor

def process_existing_documents():
    """Process all unprocessed documents"""
    db = SessionLocal()
    doc_processor = DocumentProcessor()
    
    try:
        # Get all unprocessed documents
        unprocessed_docs = db.query(Document).filter(
            Document.is_processed == False
        ).all()
        
        print(f"Found {len(unprocessed_docs)} unprocessed documents")
        
        for document in unprocessed_docs:
            print(f"\nProcessing document ID {document.id}: {document.doc_name}")
            
            if not os.path.exists(document.file_path):
                print(f"  ⚠ File not found: {document.file_path}")
                continue
            
            try:
                result = doc_processor.process_document(document.file_path, str(document.id))
                
                if result.get("success"):
                    text_content = result.get("text_content", {})
                    document.total_words = text_content.get("total_words", 0)
                    document.total_pages = text_content.get("total_pages", 0)
                    document.is_processed = True
                    
                    db.commit()
                    print(f"  ✓ Processed successfully")
                    print(f"    - Words: {document.total_words}")
                    print(f"    - Pages: {document.total_pages}")
                else:
                    print(f"  ✗ Processing failed: {result.get('error', 'Unknown error')}")
            except Exception as e:
                print(f"  ✗ Error: {str(e)}")
        
        # Get all processed documents
        processed_docs = db.query(Document).filter(
            Document.is_processed == True
        ).all()
        
        print(f"\n{'='*60}")
        print(f"Summary:")
        print(f"  Total documents: {db.query(Document).count()}")
        print(f"  Processed: {len(processed_docs)}")
        print(f"  Unprocessed: {db.query(Document).filter(Document.is_processed == False).count()}")
        print(f"{'='*60}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    print("Starting document processing...")
    process_existing_documents()
    print("\nDocument processing complete!")


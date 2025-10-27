"""
Documents router for document management and AI Q&A
"""
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import PyPDF2
import docx
import shutil
from datetime import datetime

from database import get_db
from models import Document, User
from schemas import DocumentResponse
from utils.auth import get_current_user
from utils.gemini_client import GeminiClient
from utils.text_extractors import extract_text_from_pdf, extract_text_from_docx, extract_text_from_txt
from config import settings

router = APIRouter()

@router.get("/all", response_model=List[DocumentResponse])
async def get_all_documents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all documents for the logged-in user"""
    documents = db.query(Document).filter(Document.user_id == current_user.id).all()
    
    # Format response with additional metadata
    response = []
    for doc in documents:
        doc_data = {
            "id": doc.id,
            "user_id": doc.user_id,
            "admin_id": None,  # For backward compatibility
            "doc_name": doc.doc_name,
            "file_path": doc.file_path,
            "file_type": doc.file_type,
            "total_words": doc.total_words,
            "total_pages": doc.total_pages,
            "is_processed": doc.is_processed,
            "created_at": doc.created_at,
            "size": doc.file_size if hasattr(doc, 'file_size') else 0
        }
        response.append(DocumentResponse(**doc_data))
    
    return response

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Upload a new document"""
    # Validate file type
    allowed_extensions = ['.pdf', '.docx', '.txt', '.doc']
    file_extension = os.path.splitext(file.filename)[1].lower()
    
    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed types: {', '.join(allowed_extensions)}"
        )
    
    # Create upload directory if it doesn't exist
    upload_dir = os.path.join(settings.upload_dir, str(current_user.id))
    os.makedirs(upload_dir, exist_ok=True)
    
    # Generate unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{file.filename}"
    file_path = os.path.join(upload_dir, filename)
    
    # Save file
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
    
    # Get file size
    file_size = os.path.getsize(file_path)
    
    # Extract metadata
    total_pages = 0
    total_words = 0
    
    try:
        if file_extension == '.pdf':
            text = extract_text_from_pdf(file_path)
            with open(file_path, 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                total_pages = len(pdf_reader.pages)
            total_words = len(text.split())
        elif file_extension in ['.docx', '.doc']:
            text = extract_text_from_docx(file_path)
            doc = docx.Document(file_path)
            total_pages = len(doc.element.body)
            total_words = len(text.split())
        elif file_extension == '.txt':
            text = extract_text_from_txt(file_path)
            total_words = len(text.split())
            total_pages = max(1, total_words // 500)  # Estimate pages
    except Exception as e:
        print(f"Warning: Could not extract metadata: {str(e)}")
    
    # Create database entry
    document = Document(
        user_id=current_user.id,
        doc_name=file.filename,
        file_path=file_path,
        file_type=file_extension[1:],  # Remove the dot
        file_size=file_size,
        total_words=total_words,
        total_pages=total_pages,
        is_processed=True
    )
    
    db.add(document)
    db.commit()
    db.refresh(document)
    
    return {
        "message": "Document uploaded successfully",
        "document_id": document.id,
        "filename": file.filename,
        "size": file_size,
        "pages": total_pages
    }

@router.get("/{doc_id}/content")
async def get_document_content(
    doc_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get document content as text"""
    # Find document
    document = db.query(Document).filter(
        Document.id == doc_id,
        Document.user_id == current_user.id
    ).first()
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Extract text based on file type
    try:
        if document.file_type == 'pdf':
            text = extract_text_from_pdf(document.file_path)
        elif document.file_type in ['docx', 'doc']:
            text = extract_text_from_docx(document.file_path)
        elif document.file_type == 'txt':
            text = extract_text_from_txt(document.file_path)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")
        
        return {
            "document_id": doc_id,
            "filename": document.doc_name,
            "content": text,
            "word_count": len(text.split()),
            "pages": document.total_pages
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to extract content: {str(e)}")

@router.post("/ask")
async def ask_document_question(
    doc_id: int,
    question: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Ask a question about a document using Gemini AI"""
    # Find document
    document = db.query(Document).filter(
        Document.id == doc_id,
        Document.user_id == current_user.id
    ).first()
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Extract document text
    try:
        if document.file_type == 'pdf':
            text = extract_text_from_pdf(document.file_path)
        elif document.file_type in ['docx', 'doc']:
            text = extract_text_from_docx(document.file_path)
        elif document.file_type == 'txt':
            text = extract_text_from_txt(document.file_path)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read document: {str(e)}")
    
    # Use Gemini AI to answer the question
    try:
        gemini_client = GeminiClient()
        
        # Create prompt
        prompt = f"""Based on the following document content, please answer this question:

Question: {question}

Document Content:
{text[:8000]}  

Please provide a clear and concise answer based only on the information in the document."""
        
        answer = gemini_client.generate_response(prompt)
        
        return {
            "question": question,
            "answer": answer,
            "document_name": document.doc_name,
            "document_id": doc_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI processing failed: {str(e)}")

@router.get("/{doc_id}/download")
async def download_document(
    doc_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Download a document"""
    document = db.query(Document).filter(
        Document.id == doc_id,
        Document.user_id == current_user.id
    ).first()
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    if not os.path.exists(document.file_path):
        raise HTTPException(status_code=404, detail="File not found on server")
    
    return FileResponse(
        path=document.file_path,
        filename=document.doc_name,
        media_type='application/octet-stream'
    )

@router.delete("/{doc_id}")
async def delete_document(
    doc_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a document"""
    document = db.query(Document).filter(
        Document.id == doc_id,
        Document.user_id == current_user.id
    ).first()
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Delete physical file
    try:
        if os.path.exists(document.file_path):
            os.remove(document.file_path)
    except Exception as e:
        print(f"Warning: Could not delete file: {str(e)}")
    
    # Delete database entry
    db.delete(document)
    db.commit()
    
    return {"message": "Document deleted successfully"}

@router.get("/stats")
async def get_document_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get document statistics for the current user"""
    documents = db.query(Document).filter(Document.user_id == current_user.id).all()
    
    total_size = sum(doc.file_size if hasattr(doc, 'file_size') else 0 for doc in documents)
    pdf_count = sum(1 for doc in documents if doc.file_type == 'pdf')
    other_count = len(documents) - pdf_count
    
    # Format size
    if total_size >= 1024 * 1024:
        size_str = f"{total_size / (1024 * 1024):.1f} MB"
    elif total_size >= 1024:
        size_str = f"{total_size / 1024:.1f} KB"
    else:
        size_str = f"{total_size} B"
    
    return {
        "totalDocuments": len(documents),
        "totalSize": size_str,
        "pdfFiles": pdf_count,
        "otherFiles": other_count
    }


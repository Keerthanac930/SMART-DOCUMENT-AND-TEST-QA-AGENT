"""
AI router for AI-powered features
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models import User, Document
from schemas import QuestionRequest, AIQuestionResponse
from utils.auth import get_current_user
from utils.gemini_client import GeminiClient
from utils.document_processor import DocumentProcessor

router = APIRouter()

@router.post("/ask", response_model=AIQuestionResponse)
async def ask_question(
    question_request: QuestionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Ask a question using AI and document search"""
    try:
        # Initialize AI client and document processor
        gemini_client = GeminiClient()
        doc_processor = DocumentProcessor()
        
        # If document IDs are specified, search in those documents first
        if question_request.document_ids:
            documents = db.query(Document).filter(
                Document.id.in_(question_request.document_ids),
                Document.is_processed == True
            ).all()
            
            # Search for relevant content in documents
            relevant_content = doc_processor.search_documents(
                question_request.question,
                documents
            )
            
            if relevant_content:
                # Generate answer based on document content
                answer = gemini_client.generate_answer_from_context(
                    question_request.question,
                    relevant_content
                )
                
                return AIQuestionResponse(
                    answer=answer,
                    source="document",
                    confidence=0.9,
                    citations=relevant_content.get("citations", []),
                    page_numbers=relevant_content.get("page_numbers", [])
                )
        
        # Fallback to general AI response
        ai_response = gemini_client.generate_answer(question_request.question)
        
        return AIQuestionResponse(
            answer=ai_response,
            source="ai",
            confidence=0.7,
            citations=None,
            page_numbers=None
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing question: {str(e)}"
        )

@router.post("/generate-questions")
async def generate_questions_from_document(
    document_id: int,
    num_questions: int = 5,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generate quiz questions from a document"""
    try:
        # Get document
        document = db.query(Document).filter(Document.id == document_id).first()
        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found"
            )
        
        # Initialize AI client and document processor
        gemini_client = GeminiClient()
        doc_processor = DocumentProcessor()
        
        # Extract text from document
        document_content = doc_processor.extract_text_from_document(document.file_path)
        document_text = document_content.get("full_text", "")
        
        # Generate questions using Gemini
        questions = gemini_client.generate_quiz_questions(
            document_text,
            num_questions
        )
        
        return {"questions": questions}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating questions: {str(e)}"
        )

@router.post("/summarize-document")
async def summarize_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generate a summary of a document"""
    try:
        # Get document
        document = db.query(Document).filter(Document.id == document_id).first()
        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found"
            )
        
        # Initialize AI client and document processor
        gemini_client = GeminiClient()
        doc_processor = DocumentProcessor()
        
        # Extract text from document
        document_content = doc_processor.extract_text_from_document(document.file_path)
        document_text = document_content.get("full_text", "")
        
        # Generate summary using Gemini
        summary = gemini_client.generate_summary(document_text)
        
        return {"summary": summary}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating summary: {str(e)}"
        )

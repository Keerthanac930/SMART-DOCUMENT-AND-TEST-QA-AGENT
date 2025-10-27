"""
Admin router for administrative functions
"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import User, Test, Question, Document, Result
from schemas import (
    UserResponse, TestCreate, TestResponse, 
    DocumentResponse, DashboardStats, UserStats, TestStats, DocumentStats
)
from utils.auth import get_current_admin
from utils.gemini_client import GeminiClient

router = APIRouter()

@router.get("/profile", response_model=UserResponse)
async def get_admin_profile(
    current_admin: User = Depends(get_current_admin)
):
    """Get current admin profile"""
    return UserResponse(
        id=current_admin.id,
        username=current_admin.username,
        email=current_admin.email,
        role=current_admin.role.value,
        test_history=current_admin.test_history or [],
        created_at=current_admin.created_at
    )

@router.get("/users", response_model=List[UserResponse])
async def get_all_users(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """Get all users"""
    users = db.query(User).all()
    return [UserResponse(
        id=u.id,
        username=u.username,
        email=u.email,
        role=u.role.value if hasattr(u.role, 'value') else u.role,
        test_history=u.test_history or [],
        created_at=u.created_at
    ) for u in users]

@router.get("/user/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """Get specific user details"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        role=user.role.value if hasattr(user.role, 'value') else user.role,
        test_history=user.test_history or [],
        created_at=user.created_at
    )

@router.delete("/user/{user_id}")
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """Delete a user"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}

@router.post("/tests/generate")
async def generate_test_with_ai(
    test_name: str,
    topic: str,
    num_questions: int = 25,
    difficulty: str = "medium",
    time_limit_minutes: int = 20,
    description: str = None,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """Generate a test using Gemini AI"""
    try:
        # Initialize Gemini client
        gemini_client = GeminiClient()
        
        # Generate questions with context
        questions_data = gemini_client.generate_test_questions(
            topic=topic,
            num_questions=num_questions,
            difficulty=difficulty,
            test_name=test_name,
            description=description
        )
        
        # Create test
        test = Test(
            admin_id=current_admin.id,
            test_name=test_name,
            topic=topic,
            description=description or f"AI-generated {difficulty} test on {topic}",
            time_limit_minutes=time_limit_minutes
        )
        
        db.add(test)
        db.flush()  # Get the test ID
        
        # Create questions from AI-generated data
        for q_data in questions_data:
            question = Question(
                test_id=test.id,
                question_text=q_data.get("question_text", ""),
                correct_answer=q_data.get("correct_answer", "A"),
                options=q_data.get("options", {}),
                explanation=q_data.get("explanation", ""),
                difficulty=q_data.get("difficulty", difficulty)
            )
            db.add(question)
        
        db.commit()
        db.refresh(test)
        
        return {
            "message": "Test generated successfully",
            "test_id": test.id,
            "test_name": test.test_name,
            "num_questions": len(questions_data)
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate test: {str(e)}"
        )

@router.post("/tests", response_model=TestResponse)
async def create_test(
    test_data: TestCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """Create a new test manually"""
    # Create test
    test = Test(
        admin_id=current_admin.id,
        test_name=test_data.test_name,
        topic=test_data.topic,
        description=test_data.description,
        time_limit_minutes=test_data.time_limit_minutes
    )
    
    db.add(test)
    db.flush()  # Get the test ID
    
    # Create questions
    for question_data in test_data.questions:
        question = Question(
            test_id=test.id,
            question_text=question_data.question_text,
            correct_answer=question_data.correct_answer,
            options=question_data.options,
            explanation=question_data.explanation,
            difficulty=question_data.difficulty
        )
        db.add(question)
    
    db.commit()
    db.refresh(test)
    return test

@router.get("/tests", response_model=List[TestResponse])
async def get_admin_tests(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """Get all tests created by current admin"""
    tests = db.query(Test).filter(Test.admin_id == current_admin.id).all()
    return tests

@router.get("/tests/{test_id}", response_model=TestResponse)
async def get_test(
    test_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """Get specific test details"""
    test = db.query(Test).filter(
        Test.id == test_id,
        Test.admin_id == current_admin.id
    ).first()
    
    if not test:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Test not found"
        )
    
    return test

@router.put("/tests/{test_id}")
async def update_test(
    test_id: int,
    test_data: dict,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """Update a test"""
    test = db.query(Test).filter(
        Test.id == test_id,
        Test.admin_id == current_admin.id
    ).first()
    
    if not test:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Test not found"
        )
    
    # Update test fields
    for field, value in test_data.items():
        if hasattr(test, field):
            setattr(test, field, value)
    
    db.commit()
    return {"message": "Test updated successfully"}

@router.delete("/tests/{test_id}")
async def delete_test(
    test_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """Delete a test"""
    test = db.query(Test).filter(
        Test.id == test_id,
        Test.admin_id == current_admin.id
    ).first()
    
    if not test:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Test not found"
        )
    
    db.delete(test)
    db.commit()
    return {"message": "Test deleted successfully"}

@router.get("/documents", response_model=List[DocumentResponse])
async def get_all_documents(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """Get all documents"""
    documents = db.query(Document).all()
    return documents

@router.post("/documents", response_model=DocumentResponse)
async def upload_admin_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """Upload a document as admin and process it"""
    import os
    from datetime import datetime
    from utils.document_processor import DocumentProcessor
    
    # Create uploads directory if it doesn't exist
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    
    # Generate unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{file.filename}"
    file_path = os.path.join(upload_dir, filename)
    
    # Save file
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    # Determine file type from extension
    file_extension = os.path.splitext(file.filename)[1].lower()
    file_type_map = {
        '.pdf': 'pdf',
        '.docx': 'docx',
        '.doc': 'doc',
        '.txt': 'txt',
        '.png': 'image',
        '.jpg': 'image',
        '.jpeg': 'image'
    }
    file_type = file_type_map.get(file_extension, 'unknown')
    
    # Create document record (admin documents don't have user_id)
    document = Document(
        user_id=None,  # Admin documents
        doc_name=file.filename,
        file_path=file_path,
        file_type=file_type,
        total_words=0,
        total_pages=0,
        is_processed=False
    )
    
    db.add(document)
    db.commit()
    db.refresh(document)
    
    # Process the document
    try:
        doc_processor = DocumentProcessor()
        result = doc_processor.process_document(file_path, str(document.id))
        
        if result.get("success"):
            text_content = result.get("text_content", {})
            document.total_words = text_content.get("total_words", 0)
            document.total_pages = text_content.get("total_pages", 0)
            document.is_processed = True
            
            db.commit()
            db.refresh(document)
    except Exception as e:
        # Log error but don't fail the upload
        print(f"Error processing document: {str(e)}")
    
    return document

@router.post("/documents/{document_id}/process")
async def process_admin_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """Manually trigger document processing for any document"""
    from utils.document_processor import DocumentProcessor
    
    document = db.query(Document).filter(Document.id == document_id).first()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    try:
        doc_processor = DocumentProcessor()
        result = doc_processor.process_document(document.file_path, str(document.id))
        
        if result.get("success"):
            text_content = result.get("text_content", {})
            document.total_words = text_content.get("total_words", 0)
            document.total_pages = text_content.get("total_pages", 0)
            document.is_processed = True
            
            db.commit()
            db.refresh(document)
            
            return {
                "message": "Document processed successfully",
                "document_id": document.id,
                "total_words": document.total_words,
                "total_pages": document.total_pages
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Processing failed: {result.get('error', 'Unknown error')}"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing document: {str(e)}"
        )

@router.delete("/documents/{document_id}")
async def delete_admin_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """Delete a document (admin only)"""
    import os
    
    document = db.query(Document).filter(Document.id == document_id).first()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
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

@router.get("/dashboard/stats", response_model=DashboardStats)
async def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """Get dashboard statistics"""
    # User stats
    total_users = db.query(User).count()
    # You can add more complex queries for active users, new users this month, etc.
    
    # Test stats
    total_tests = db.query(Test).count()
    active_tests = db.query(Test).filter(Test.is_active == True).count()
    total_attempts = db.query(Result).count()
    
    # Calculate average score
    results = db.query(Result).all()
    average_score = sum(r.score for r in results) / len(results) if results else 0
    
    # Document stats
    total_documents = db.query(Document).count()
    documents_by_type = {}
    # You can add more complex queries here
    
    return DashboardStats(
        users=UserStats(
            total_users=total_users,
            active_users=total_users,  # Simplified for now
            new_users_this_month=0  # Simplified for now
        ),
        tests=TestStats(
            total_tests=total_tests,
            active_tests=active_tests,
            total_attempts=total_attempts,
            average_score=average_score
        ),
        documents=DocumentStats(
            total_documents=total_documents,
            total_words=0,  # Simplified for now
            documents_by_type=documents_by_type
        )
    )

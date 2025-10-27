"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict, Any
from datetime import datetime

# Authentication schemas
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str = "student"  # "admin" or "student"

class Token(BaseModel):
    access_token: str
    token_type: str
    role: str

class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None  # "admin" or "student"

# User schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str
    role: str = "student"

class UserResponse(UserBase):
    id: int
    role: str
    test_history: List[Dict[str, Any]]
    created_at: datetime
    
    class Config:
        from_attributes = True

# Test schemas
class QuestionCreate(BaseModel):
    question_text: str
    correct_answer: str
    options: Dict[str, str]
    explanation: Optional[str] = None
    difficulty: str = "medium"

class QuestionResponse(BaseModel):
    id: int
    question_text: str
    correct_answer: str
    options: Dict[str, str]
    explanation: Optional[str]
    difficulty: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class TestCreate(BaseModel):
    test_name: str
    topic: str
    description: Optional[str] = None
    time_limit_minutes: int = 60
    questions: List[QuestionCreate]

class TestUpdate(BaseModel):
    test_name: Optional[str] = None
    topic: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    time_limit_minutes: Optional[int] = None

class TestResponse(BaseModel):
    id: int
    admin_id: int
    test_name: str
    topic: str
    description: Optional[str]
    is_active: bool
    time_limit_minutes: int
    created_at: datetime
    questions: List[QuestionResponse]
    
    class Config:
        from_attributes = True

# Document schemas
class DocumentUpload(BaseModel):
    doc_name: str

class DocumentResponse(BaseModel):
    id: int
    user_id: Optional[int] = None
    doc_name: str
    file_path: str
    file_type: str
    file_size: Optional[int] = 0
    total_words: int = 0
    total_pages: int = 0
    is_processed: bool = False
    created_at: datetime
    
    class Config:
        from_attributes = True

# Quiz/Test taking schemas
class QuizAnswer(BaseModel):
    question_id: int
    answer: str

class QuizSubmission(BaseModel):
    test_id: int
    answers: List[QuizAnswer]
    time_taken_minutes: float

class QuizResult(BaseModel):
    id: int
    user_id: int
    test_id: int
    score: float
    total_questions: int
    correct_answers: int
    time_taken_minutes: float
    answers: Dict[str, Any]
    completed_at: datetime
    
    class Config:
        from_attributes = True

# AI Q&A schemas
class QuestionRequest(BaseModel):
    question: str
    document_ids: Optional[List[int]] = None

class AIQuestionResponse(BaseModel):
    answer: str
    source: str  # "document" or "ai"
    confidence: float
    citations: Optional[List[Dict[str, Any]]] = None
    page_numbers: Optional[List[int]] = None

# Analytics schemas
class UserStats(BaseModel):
    total_users: int
    active_users: int
    new_users_this_month: int

class TestStats(BaseModel):
    total_tests: int
    active_tests: int
    total_attempts: int
    average_score: float

class DocumentStats(BaseModel):
    total_documents: int
    total_words: int
    documents_by_type: Dict[str, int]

class DashboardStats(BaseModel):
    users: UserStats
    tests: TestStats
    documents: DocumentStats

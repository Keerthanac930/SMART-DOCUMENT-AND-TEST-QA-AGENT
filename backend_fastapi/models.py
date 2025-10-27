"""
Database models for the QA Agent system
"""
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, JSON, ForeignKey, Float, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import enum

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    STUDENT = "student"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False, default="student")
    test_history = Column(JSON, default=list)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    tests = relationship("Test", back_populates="admin")
    documents = relationship("Document", back_populates="user")
    results = relationship("Result", back_populates="user")

class Test(Base):
    __tablename__ = "tests"
    
    id = Column(Integer, primary_key=True, index=True)
    admin_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    test_name = Column(String(200), nullable=False)
    topic = Column(String(200), nullable=False)
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    time_limit_minutes = Column(Integer, default=60)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    admin = relationship("User", back_populates="tests")
    questions = relationship("Question", back_populates="test", cascade="all, delete-orphan")
    results = relationship("Result", back_populates="test")

class Question(Base):
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, index=True)
    test_id = Column(Integer, ForeignKey("tests.id"), nullable=False)
    question_text = Column(Text, nullable=False)
    correct_answer = Column(String(10), nullable=False)  # A, B, C, D
    options = Column(JSON, nullable=False)  # {"A": "option1", "B": "option2", ...}
    explanation = Column(Text)
    difficulty = Column(String(20), default="medium")  # easy, medium, hard
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    test = relationship("Test", back_populates="questions")

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Nullable for admin uploads
    doc_name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_type = Column(String(20), nullable=False)  # pdf, docx, txt, image
    file_size = Column(Integer, default=0)  # in bytes
    total_words = Column(Integer, default=0)
    total_pages = Column(Integer, default=0)
    is_processed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="documents")

class Result(Base):
    __tablename__ = "results"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    test_id = Column(Integer, ForeignKey("tests.id"), nullable=False)
    score = Column(Float, nullable=False)  # Percentage score
    total_questions = Column(Integer, nullable=False)
    correct_answers = Column(Integer, nullable=False)
    time_taken_minutes = Column(Float, nullable=False)
    answers = Column(JSON, nullable=False)  # User's answers
    proctoring_violations = Column(Integer, default=0)
    is_flagged = Column(Boolean, default=False)
    completed_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="results")
    test = relationship("Test", back_populates="results")
    proctor_logs = relationship("ProctorLog", back_populates="result")

class ProctorLog(Base):
    __tablename__ = "proctor_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    result_id = Column(Integer, ForeignKey("results.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    test_id = Column(Integer, ForeignKey("tests.id"), nullable=False)
    violation_type = Column(String(50), nullable=False)  # no_face, multiple_faces, loud_audio, etc.
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    result = relationship("Result", back_populates="proctor_logs")

class Score(Base):
    __tablename__ = "scores"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    test_id = Column(Integer, ForeignKey("tests.id"), nullable=False)
    score = Column(Float, nullable=False)  # Percentage or points
    duration = Column(Float)  # Time taken in minutes
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())

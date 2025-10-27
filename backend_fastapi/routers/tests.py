"""
Tests router for test-related operations
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Test, Question, Result, User
from schemas import TestResponse, QuestionResponse
from utils.auth import get_current_user

router = APIRouter()

@router.get("/all")
async def get_all_available_tests(
    db: Session = Depends(get_db)
):
    """Get all active tests for students"""
    tests = db.query(Test).filter(Test.is_active == True).all()
    
    # Return simplified response without nested questions
    return [{
        "id": test.id,
        "test_name": test.test_name,
        "topic": test.topic,
        "description": test.description,
        "time_limit_minutes": test.time_limit_minutes,
        "is_active": test.is_active,
        "created_at": test.created_at.isoformat() if test.created_at else None,
        "question_count": len(test.questions) if test.questions else 0
    } for test in tests]

@router.get("/{test_id}")
async def get_test_details(
    test_id: int,
    db: Session = Depends(get_db)
):
    """Get test details"""
    test = db.query(Test).filter(
        Test.id == test_id,
        Test.is_active == True
    ).first()
    
    if not test:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Test not found"
        )
    
    # Return simplified response
    return {
        "id": test.id,
        "test_name": test.test_name,
        "topic": test.topic,
        "description": test.description,
        "time_limit_minutes": test.time_limit_minutes,
        "is_active": test.is_active,
        "created_at": test.created_at.isoformat() if test.created_at else None,
        "question_count": len(test.questions) if test.questions else 0
    }

@router.get("/{test_id}/questions", response_model=List[QuestionResponse])
async def get_test_questions(
    test_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get test questions (requires authentication)"""
    test = db.query(Test).filter(
        Test.id == test_id,
        Test.is_active == True
    ).first()
    
    if not test:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Test not found"
        )
    
    questions = db.query(Question).filter(Question.test_id == test_id).all()
    
    # For regular users, hide correct answers
    if current_user.role != "admin":
        for question in questions:
            question.correct_answer = "***"  # Hide correct answer
    
    return questions

@router.post("/submit")
async def submit_test(
    payload: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Submit test answers and calculate score"""
    from datetime import datetime
    from models import Score
    
    test_id = payload.get("test_id")
    answers = payload.get("answers", {})
    time_taken = payload.get("time_taken_minutes", 0)
    
    if not test_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="test_id is required"
        )
    
    # Get test and questions
    test = db.query(Test).filter(Test.id == test_id).first()
    if not test:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Test not found"
        )
    
    questions = db.query(Question).filter(Question.test_id == test_id).all()
    
    # Calculate score
    correct_count = 0
    total_questions = len(questions)
    
    for question in questions:
        user_answer = answers.get(str(question.id))
        if user_answer and user_answer == question.correct_answer:
            correct_count += 1
    
    score_percentage = (correct_count / total_questions * 100) if total_questions > 0 else 0
    
    # Save to scores table
    new_score = Score(
        user_id=current_user.id,
        test_id=test_id,
        score=score_percentage,
        duration=time_taken
    )
    
    db.add(new_score)
    
    # Also save to results table for compatibility
    new_result = Result(
        user_id=current_user.id,
        test_id=test_id,
        score=score_percentage,
        total_questions=total_questions,
        correct_answers=correct_count,
        time_taken_minutes=time_taken,
        answers=answers,
        proctoring_violations=0,
        is_flagged=False
    )
    
    db.add(new_result)
    db.commit()
    db.refresh(new_score)
    
    return {
        "message": "Test submitted successfully!",
        "score": score_percentage,
        "correct": correct_count,
        "total": total_questions,
        "score_id": new_score.id
    }

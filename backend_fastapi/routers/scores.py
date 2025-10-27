"""
Scores router for managing quiz results and scores
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Result, User, Test, UserRole
from schemas import QuizSubmission, QuizResult
from utils.auth import get_current_user

router = APIRouter()

@router.get("/all", response_model=List[QuizResult])
async def get_all_scores(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all student scores (admin only)"""
    # Handle both string and enum role comparison (case-insensitive)
    user_role = current_user.role.upper() if isinstance(current_user.role, str) else current_user.role.value.upper()
    if user_role != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can view all scores"
        )
    
    results = db.query(Result).order_by(Result.completed_at.desc()).all()
    return results

@router.get("/my-scores", response_model=List[QuizResult])
async def get_my_scores(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get current user's scores"""
    results = db.query(Result).filter(
        Result.user_id == current_user.id
    ).order_by(Result.completed_at.desc()).all()
    return results

@router.get("/my")
async def get_my_scores_simple(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get current user's scores with test details (simplified)"""
    from sqlalchemy import join
    
    results = db.query(Result, Test).join(Test, Result.test_id == Test.id).filter(
        Result.user_id == current_user.id
    ).order_by(Result.completed_at.desc()).all()
    
    scores_list = []
    for result, test in results:
        scores_list.append({
            "id": result.id,
            "test_name": test.test_name,
            "category": test.topic,
            "score": result.score,
            "total_questions": result.total_questions,
            "correct_answers": result.correct_answers,
            "submitted_at": result.completed_at.isoformat() if result.completed_at else None,
            "time_taken": result.time_taken_minutes,
            "duration": test.time_limit_minutes
        })
    
    return scores_list

@router.post("/submit", response_model=QuizResult)
async def submit_score(
    submission: QuizSubmission,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Submit quiz answers and calculate score (student only)"""
    if current_user.role != UserRole.STUDENT:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only students can submit test scores"
        )
    
    # Get test
    test = db.query(Test).filter(Test.id == submission.test_id).first()
    if not test:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Test not found"
        )
    
    # Calculate score
    correct_count = 0
    total_questions = len(submission.answers)
    
    for answer in submission.answers:
        question = next((q for q in test.questions if q.id == answer.question_id), None)
        if question and question.correct_answer == answer.answer:
            correct_count += 1
    
    score_percentage = (correct_count / total_questions * 100) if total_questions > 0 else 0
    
    # Create result
    result = Result(
        user_id=current_user.id,
        test_id=submission.test_id,
        score=score_percentage,
        total_questions=total_questions,
        correct_answers=correct_count,
        time_taken_minutes=submission.time_taken_minutes,
        answers={str(a.question_id): a.answer for a in submission.answers}
    )
    
    db.add(result)
    db.commit()
    db.refresh(result)
    
    return result


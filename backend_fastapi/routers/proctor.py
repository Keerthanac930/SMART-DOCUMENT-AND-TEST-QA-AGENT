"""
Proctoring router for AI-proctored exam monitoring
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import ProctorLog, Result, User, UserRole
from pydantic import BaseModel
from datetime import datetime
from utils.auth import get_current_user

router = APIRouter()

class ProctorLogRequest(BaseModel):
    result_id: int
    test_id: int
    violation_type: str

class ProctorLogResponse(BaseModel):
    id: int
    user_id: int
    test_id: int
    violation_type: str
    timestamp: datetime
    
    class Config:
        from_attributes = True

@router.post("/log", status_code=status.HTTP_201_CREATED)
async def log_proctor_violation(
    log_data: ProctorLogRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Log a proctoring violation (student only)"""
    if current_user.role != UserRole.STUDENT:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only students can log proctoring violations"
        )
    
    # Create proctor log
    proctor_log = ProctorLog(
        result_id=log_data.result_id,
        user_id=current_user.id,
        test_id=log_data.test_id,
        violation_type=log_data.violation_type
    )
    
    db.add(proctor_log)
    
    # Update result violation count
    result = db.query(Result).filter(Result.id == log_data.result_id).first()
    if result:
        result.proctoring_violations = (result.proctoring_violations or 0) + 1
        if result.proctoring_violations >= 10:
            result.is_flagged = True
    
    db.commit()
    
    return {
        "success": True,
        "violation_count": result.proctoring_violations if result else 0,
        "is_flagged": result.is_flagged if result else False
    }

@router.get("/reports/{test_id}", response_model=List[ProctorLogResponse])
async def get_proctor_reports(
    test_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get proctoring reports for a test (admin only)"""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can view proctoring reports"
        )
    
    logs = db.query(ProctorLog).filter(ProctorLog.test_id == test_id).all()
    return logs

@router.get("/violations/{result_id}")
async def get_violation_count(
    result_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get violation count for a specific test attempt"""
    result = db.query(Result).filter(Result.id == result_id).first()
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Result not found"
        )
    
    # Only allow user to see their own violations or admin to see all
    if current_user.role != UserRole.ADMIN and result.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    return {
        "violation_count": result.proctoring_violations or 0,
        "is_flagged": result.is_flagged or False
    }


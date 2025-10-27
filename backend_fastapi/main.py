"""
FastAPI Backend for Smart Document & Test QA Agent Dashboard
Configured for port 8000 with complete CORS and folder management
"""
from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import os
import uvicorn
from datetime import datetime, timedelta
from typing import List, Optional
import jwt
from passlib.context import CryptContext
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import our modules
from database import get_db, engine, Base
from models import *
from schemas import *
from routers import auth, admin, user, tests, ai, proctor, scores, documents
from config import settings
from utils.auth import get_current_user

# Create necessary folders on startup
os.makedirs(settings.upload_dir, exist_ok=True)
os.makedirs(settings.temp_dir, exist_ok=True)
os.makedirs(settings.vector_db_path, exist_ok=True)
os.makedirs("chroma_db", exist_ok=True)

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Smart Document & Test QA Agent API",
    description="Backend API for document processing, AI-powered Q&A, and quiz management with role-based access",
    version="1.0.0"
)

# CORS middleware - Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Primary React dev server
        "http://localhost:3001",  # Alternate React port (CURRENT)
        "http://localhost:5173",  # Vite default port
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "http://127.0.0.1:5173",
        "*"  # Allow all for development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers with proper prefixes
app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])
app.include_router(user.router, prefix="/api/user", tags=["user"])
app.include_router(tests.router, prefix="/api/tests", tags=["tests"])
app.include_router(scores.router, prefix="/api/scores", tags=["scores"])
app.include_router(proctor.router, prefix="/api/proctor", tags=["proctoring"])
app.include_router(ai.router, prefix="/api/ai", tags=["ai"])
app.include_router(documents.router, prefix="/api/documents", tags=["documents"])

@app.on_event("startup")
async def startup_event():
    """Startup event to verify configuration"""
    print("=" * 60)
    print("🚀 Starting Smart Document & Test QA Agent Backend")
    print("=" * 60)
    print(f"📁 Upload Directory: {settings.upload_dir}")
    print(f"📁 Temp Directory: {settings.temp_dir}")
    print(f"📁 Vector DB Path: {settings.vector_db_path}")
    print(f"🔑 Gemini API Key: {'✅ Configured' if settings.get_gemini_key else '❌ Missing'}")
    print(f"🗄️  Database: {settings.mysql_database}")
    print(f"🌐 Port: 8000")
    print(f"🔐 CORS Enabled for: http://localhost:3000")
    print("=" * 60)

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Smart Document & Test QA Agent API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "health": "/api/health"
    }

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "gemini_api_configured": bool(settings.get_gemini_key),
        "database": settings.mysql_database
    }

@app.get("/api/stats")
async def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get dashboard statistics for the logged-in user"""
    from utils.auth import get_current_user
    
    # Get document stats
    documents = db.query(Document).filter(Document.user_id == current_user.id).all()
    total_size = sum(doc.file_size if hasattr(doc, 'file_size') and doc.file_size else 0 for doc in documents)
    pdf_count = sum(1 for doc in documents if doc.file_type == 'pdf')
    other_count = len(documents) - pdf_count
    
    # Format size
    if total_size >= 1024 * 1024:
        size_str = f"{total_size / (1024 * 1024):.1f} MB"
    elif total_size >= 1024:
        size_str = f"{total_size / 1024:.1f} KB"
    else:
        size_str = f"{total_size} B"
    
    # Get test stats
    results = db.query(Result).filter(Result.user_id == current_user.id).all()
    tests_taken = len(results)
    average_score = sum(r.score for r in results) / len(results) if results else 0
    
    return {
        "totalDocuments": len(documents),
        "totalSize": size_str,
        "pdfFiles": pdf_count,
        "otherFiles": other_count,
        "testsTaken": tests_taken,
        "averageScore": round(average_score, 1)
    }

if __name__ == "__main__":
    print("\n🎯 Starting FastAPI server on http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🔄 Press CTRL+C to stop\n")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

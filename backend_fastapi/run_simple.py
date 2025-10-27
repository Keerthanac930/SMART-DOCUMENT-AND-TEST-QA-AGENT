#!/usr/bin/env python3
"""
Simple startup script for QA Agent with SQLite database
"""
import os
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.append(str(Path(__file__).parent))

from database import engine, Base
from main import app
import uvicorn

def create_database():
    """Create database tables"""
    print("Creating database tables...")
    try:
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully!")
    except Exception as e:
        print(f"Error creating database: {e}")
        return False
    return True

def create_sample_data():
    """Create sample data for testing"""
    print("Creating sample data...")
    try:
        from sqlalchemy.orm import Session
        from models import Admin, User, Test, Question
        from utils.auth import get_password_hash
        
        db = Session(bind=engine)
        
        # Check if admin already exists
        existing_admin = db.query(Admin).filter(Admin.username == "admin").first()
        if not existing_admin:
            # Create sample admin
            admin = Admin(
                username="admin",
                email="admin@example.com",
                password_hash=get_password_hash("admin123")
            )
            db.add(admin)
            db.commit()
            print("Sample admin created (username: admin, password: admin123)")
        
        # Check if user already exists
        existing_user = db.query(User).filter(User.username == "user").first()
        if not existing_user:
            # Create sample user
            user = User(
                username="user",
                email="user@example.com",
                password_hash=get_password_hash("user123")
            )
            db.add(user)
            db.commit()
            print("Sample user created (username: user, password: user123)")
        
        # Create sample test
        existing_test = db.query(Test).filter(Test.test_name == "Sample Quiz").first()
        if not existing_test:
            admin = db.query(Admin).first()
            test = Test(
                admin_id=admin.id,
                test_name="Sample Quiz",
                topic="General Knowledge",
                description="A sample quiz for testing the system",
                time_limit_minutes=30
            )
            db.add(test)
            db.flush()  # Get the test ID
            
            # Create sample questions
            questions = [
                {
                    "question_text": "What is the capital of France?",
                    "correct_answer": "A",
                    "options": {"A": "Paris", "B": "London", "C": "Berlin", "D": "Madrid"},
                    "explanation": "Paris is the capital and largest city of France.",
                    "difficulty": "easy"
                },
                {
                    "question_text": "Which planet is known as the Red Planet?",
                    "correct_answer": "B",
                    "options": {"A": "Venus", "B": "Mars", "C": "Jupiter", "D": "Saturn"},
                    "explanation": "Mars is often called the Red Planet due to its reddish appearance.",
                    "difficulty": "medium"
                },
                {
                    "question_text": "What is 2 + 2?",
                    "correct_answer": "C",
                    "options": {"A": "3", "B": "5", "C": "4", "D": "6"},
                    "explanation": "Basic arithmetic: 2 + 2 = 4",
                    "difficulty": "easy"
                }
            ]
            
            for q_data in questions:
                question = Question(
                    test_id=test.id,
                    **q_data
                )
                db.add(question)
            
            db.commit()
            print("Sample test with questions created")
        
        db.close()
        print("Sample data created successfully!")
        
    except Exception as e:
        print(f"Error creating sample data: {e}")

def main():
    """Main function to run the application"""
    print("Starting QA Agent with Simple Database Setup...")
    print("=" * 50)
    
    # Create database
    if not create_database():
        print("Failed to create database. Exiting.")
        return
    
    # Create sample data
    create_sample_data()
    
    print("=" * 50)
    print("Setup complete! Starting server...")
    print("Frontend will be available at: http://localhost:3000")
    print("Backend API will be available at: http://localhost:8000")
    print("API Documentation: http://localhost:8000/docs")
    print("=" * 50)
    print("Test Accounts:")
    print("   Admin: username=admin, password=admin123")
    print("   User:  username=user, password=user123")
    print("=" * 50)
    
    # Start the server
    try:
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\nServer stopped by user")

if __name__ == "__main__":
    main()

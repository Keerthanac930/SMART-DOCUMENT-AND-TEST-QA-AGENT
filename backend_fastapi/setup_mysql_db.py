"""
MySQL Database Setup Script
Creates the database and tables, then adds a default admin user
"""
import mysql.connector
from database import engine, Base, SessionLocal
from models import User
from utils.auth import get_password_hash

def create_database():
    """Create the MySQL database if it doesn't exist"""
    print("Step 1: Creating database...")
    try:
        # Connect to MySQL server (without specifying database)
        conn = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="Keerthu@73380"
        )
        
        cursor = conn.cursor()
        
        # Create database if it doesn't exist
        cursor.execute("CREATE DATABASE IF NOT EXISTS qa_agent_db")
        print("✅ Database 'qa_agent_db' created or already exists")
        
        cursor.close()
        conn.close()
        return True
        
    except mysql.connector.Error as err:
        print(f"❌ Error creating database: {err}")
        return False

def create_tables():
    """Create all tables"""
    print("\nStep 2: Creating tables...")
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ All tables created successfully")
        return True
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False

def create_default_users():
    """Create default admin and student users"""
    print("\nStep 3: Creating default users...")
    try:
        db = SessionLocal()
        
        # Check if admin already exists
        existing_admin = db.query(User).filter(User.username == "admin").first()
        if not existing_admin:
            admin = User(
                username="admin",
                email="admin@example.com",
                password_hash=get_password_hash("admin123"),
                role="admin"
            )
            db.add(admin)
            print("✅ Admin user created:")
            print("   Email: admin@example.com")
            print("   Password: admin123")
        else:
            print("ℹ️  Admin user already exists")
        
        # Check if student already exists
        existing_student = db.query(User).filter(User.username == "user").first()
        if not existing_student:
            student = User(
                username="user",
                email="user@example.com",
                password_hash=get_password_hash("user123"),
                role="student"
            )
            db.add(student)
            print("✅ Student user created:")
            print("   Email: user@example.com")
            print("   Password: user123")
        else:
            print("ℹ️  Student user already exists")
        
        db.commit()
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Error creating users: {e}")
        return False

def main():
    """Main setup function"""
    print("=" * 60)
    print("QA Agent - MySQL Database Setup")
    print("=" * 60)
    
    if not create_database():
        print("\n❌ Setup failed at database creation")
        return
    
    if not create_tables():
        print("\n❌ Setup failed at table creation")
        return
    
    if not create_default_users():
        print("\n❌ Setup failed at user creation")
        return
    
    print("\n" + "=" * 60)
    print("✅ Database setup complete!")
    print("=" * 60)
    print("\nYou can now start the backend server:")
    print("  python run_simple.py")
    print("\nOr:")
    print("  uvicorn main:app --reload")
    print("\nDefault login credentials:")
    print("  Admin  - Email: admin@example.com, Password: admin123")
    print("  Student - Email: user@example.com, Password: user123")
    print("=" * 60)

if __name__ == "__main__":
    main()


"""
Database setup script for Smart QA Agent
Creates the database and initializes tables
"""
import mysql.connector
from sqlalchemy import create_engine
from config import settings
from models import Base, User, UserRole
from utils.auth import get_password_hash

def create_database():
    """Create the database if it doesn't exist"""
    try:
        # Connect to MySQL server without specifying database
        conn = mysql.connector.connect(
            host=settings.mysql_host,
            port=settings.mysql_port,
            user=settings.mysql_user,
            password=settings.mysql_password
        )
        
        cursor = conn.cursor()
        
        # Create database if it doesn't exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {settings.mysql_database}")
        print(f"✅ Database '{settings.mysql_database}' created or already exists")
        
        cursor.close()
        conn.close()
        
    except mysql.connector.Error as err:
        print(f"❌ Error creating database: {err}")
        return False
    
    return True

def create_tables():
    """Create all tables"""
    try:
        engine = create_engine(settings.database_url)
        Base.metadata.create_all(bind=engine)
        print("✅ Tables created successfully")
        return True
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False

def create_admin_user():
    """Create a default admin user"""
    try:
        from database import SessionLocal
        
        db = SessionLocal()
        
        # Check if admin already exists
        existing_admin = db.query(User).filter(User.username == "admin").first()
        if existing_admin:
            print("ℹ️  Admin user already exists")
            db.close()
            return True
        
        # Create admin user
        admin = User(
            username="admin",
            email="admin@example.com",
            password_hash=get_password_hash("admin123"),
            role=UserRole.ADMIN
        )
        
        db.add(admin)
        db.commit()
        db.close()
        
        print("✅ Default admin user created:")
        print("   Username: admin")
        print("   Password: admin123")
        print("   Email: admin@example.com")
        return True
        
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        return False

def main():
    """Main setup function"""
    print("=" * 50)
    print("Smart QA Agent - Database Setup")
    print("=" * 50)
    print()
    
    print("Step 1: Creating database...")
    if not create_database():
        print("Failed to create database. Exiting.")
        return
    
    print("\nStep 2: Creating tables...")
    if not create_tables():
        print("Failed to create tables. Exiting.")
        return
    
    print("\nStep 3: Creating default admin user...")
    create_admin_user()
    
    print("\n" + "=" * 50)
    print("✅ Database setup complete!")
    print("=" * 50)
    print("\nYou can now start the backend server:")
    print("  python main.py")
    print("\nOr create a student account via the frontend at:")
    print("  http://localhost:5173/register")

if __name__ == "__main__":
    main()


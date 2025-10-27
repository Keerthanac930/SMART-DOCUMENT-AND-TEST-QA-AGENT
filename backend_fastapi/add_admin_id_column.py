"""
Add admin_id column to documents table
"""
from database import engine
from sqlalchemy import text

def add_admin_id_column():
    """Add admin_id column to documents table"""
    try:
        with engine.connect() as conn:
            # Check if column exists
            result = conn.execute(text("SHOW COLUMNS FROM documents LIKE 'admin_id'"))
            exists = result.fetchone() is not None
            
            if not exists:
                print("Adding admin_id column to documents table...")
                conn.execute(text("ALTER TABLE documents ADD COLUMN admin_id INTEGER NULL"))
                conn.commit()
                print("[OK] Column added successfully!")
            else:
                print("[INFO] Column already exists")
    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == "__main__":
    add_admin_id_column()


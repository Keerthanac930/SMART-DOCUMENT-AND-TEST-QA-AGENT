"""
Update documents table to allow NULL user_id for admin uploads
"""
import mysql.connector

def update_table():
    """Alter the documents table to allow NULL user_id"""
    try:
        conn = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="Keerthu@73380",
            database="qa_agent_db"
        )
        
        cursor = conn.cursor()
        
        # Alter table to allow NULL for user_id
        cursor.execute("""
            ALTER TABLE documents 
            MODIFY COLUMN user_id INT NULL
        """)
        
        print("✅ Documents table updated successfully!")
        print("   user_id column now allows NULL values for admin uploads")
        
        conn.commit()
        cursor.close()
        conn.close()
        
    except mysql.connector.Error as err:
        print(f"❌ Error updating table: {err}")

if __name__ == "__main__":
    print("Updating documents table...")
    update_table()


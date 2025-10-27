# MySQL Quick Setup Guide

## Step 1: Open MySQL Workbench

1. Open **MySQL Workbench**
2. Connect to your local MySQL server (usually `localhost:3306`)
3. Enter your root password if prompted

## Step 2: Run the Setup Script

1. In MySQL Workbench, click **File** → **Open SQL Script**
2. Navigate to: `E:\QA_Agent\backend_fastapi\setup_mysql.sql`
3. Click **Open**
4. Click the **⚡ Execute** button (or press Ctrl+Shift+Enter)

This will:
- Create the `qa_agent_db` database
- Create all necessary tables (users, tests, questions, documents, results)
- Insert a default admin user

## Step 3: Verify Setup

You should see:
```
Database setup completed successfully!
```

## Step 4: Restart Backend

After running the SQL script, restart your backend server.

---

## Default Admin Account

After setup, you can login with:
- **Email**: `admin@example.com`
- **Password**: `admin123`
- **Role**: Admin

---

## Troubleshooting

### If you get "Access Denied" error:
1. Make sure MySQL server is running
2. Update the password in `backend_fastapi/database.py` line 9:
   ```python
   SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/qa_agent_db"
   ```
   Replace `YOUR_PASSWORD` with your MySQL root password.

### If tables already exist:
The script will drop and recreate them automatically.

---

## Quick Test

Once setup is complete, you can:
1. **Login as Admin**: Use `admin@example.com` / `admin123`
2. **Register New User**: Create a student account
3. **Upload Documents**: Test document upload feature
4. **Create Tests**: Admin can create quizzes
5. **Use AI Assistant**: Ask questions with Gemini API


# MySQL Setup Guide

## Step 1: Create Database in MySQL Workbench

1. Open **MySQL Workbench**
2. Connect to your MySQL server (usually root with your password)
3. Open a new SQL tab
4. Run this command:

```sql
CREATE DATABASE IF NOT EXISTS smartqa_db;
```

5. Click the lightning bolt icon to execute
6. You should see "1 row(s) affected"

## Step 2: Configure Backend

Create a `.env` file in `backend_fastapi/` folder:

```env
# MySQL Configuration
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=YOUR_MYSQL_PASSWORD_HERE
MYSQL_DATABASE=smartqa_db

# JWT Configuration
SECRET_KEY=your-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**Replace `YOUR_MYSQL_PASSWORD_HERE` with your actual MySQL root password**

## Step 3: Start Backend

```bash
cd backend_fastapi
.\venv\Scripts\activate
python main.py
```

The backend will automatically create all tables in your MySQL database!

## Step 4: Verify in MySQL Workbench

After starting the backend, refresh your MySQL Workbench:

1. Right-click on `smartqa_db` database
2. Select "Refresh All"
3. You should see these tables:
   - `users`
   - `tests`
   - `questions`
   - `documents`
   - `results`

## Troubleshooting

### "Access denied for user"
- Check your MySQL password in `.env` file
- Make sure MySQL is running

### "Unknown database 'smartqa_db'"
- Run: `CREATE DATABASE smartqa_db;` in MySQL Workbench

### "Cannot connect to MySQL server"
- Start MySQL server:
  - Windows: Check Services for "MySQL80"
  - Or use MySQL Workbench to start server

## Test Connection

Once backend is running, visit:
- http://localhost:8000/docs
- You should see the API documentation


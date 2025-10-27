# Authentication System Setup Guide

## Overview

This document provides complete setup instructions for the authentication system in the Smart Document & Test QA Agent web application.

## ✅ Features Implemented

- **Unified User Model**: Single User table with role field ('admin' or 'student')
- **MySQL Database**: Full MySQL integration with SQLAlchemy
- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: bcrypt for secure password storage
- **Error Handling**: Proper handling of duplicate users and incorrect passwords
- **Role-Based Access**: Admin and Student dashboards with protected routes
- **React Frontend**: Modern UI with TailwindCSS and proper error handling

## 🔧 Backend Setup

### 1. Install Dependencies

```bash
cd backend_fastapi
pip install -r requirements.txt
```

**Key dependencies:**
- FastAPI
- SQLAlchemy
- PyMySQL (MySQL connector)
- python-jose (JWT)
- passlib[bcrypt] (Password hashing)
- python-dotenv (Environment variables)

### 2. MySQL Database Setup

**Install MySQL** (if not already installed):
- Windows: Download from https://dev.mysql.com/downloads/mysql/
- Linux: `sudo apt-get install mysql-server`
- macOS: `brew install mysql`

**Create Database:**
```sql
CREATE DATABASE smartqa_db;
```

**Create User** (optional):
```sql
CREATE USER 'qa_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON smartqa_db.* TO 'qa_user'@'localhost';
FLUSH PRIVILEGES;
```

### 3. Configure Database Connection

Create or update `.env` file in `backend_fastapi/`:

```env
# MySQL Configuration
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=smartqa_db

# JWT Configuration
SECRET_KEY=your-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 4. Run Backend Server

```bash
cd backend_fastapi
python main.py
```

The server will start at `http://localhost:8000`

**Note**: Tables will be auto-created on first run via `Base.metadata.create_all(bind=engine)`

## 🎨 Frontend Setup

### 1. Install Dependencies

```bash
cd frontend_react
npm install
```

### 2. Configure API Base URL

Create `.env` file in `frontend_react/`:

```env
VITE_API_BASE_URL=http://localhost:8000
```

### 3. Run Frontend Server

```bash
cd frontend_react
npm run dev
```

The frontend will start at `http://localhost:5173`

## 📝 API Endpoints

### Authentication

- **POST** `/api/auth/register` - Register new user
  ```json
  {
    "username": "student1",
    "email": "student@example.com",
    "password": "password123",
    "role": "student"  // or "admin"
  }
  ```

- **POST** `/api/auth/login` - Login
  ```json
  {
    "username": "student1",
    "password": "password123"
  }
  ```

- **GET** `/api/auth/me` - Get current user profile (requires JWT)

### Protected Endpoints

All protected endpoints require JWT token in Authorization header:
```
Authorization: Bearer <token>
```

## 🚀 Usage Examples

### Register as Student

1. Navigate to `http://localhost:5173/register`
2. Select "Student" radio button
3. Fill in username, email, password
4. Click "Create Account"
5. Redirected to `/dashboard`

### Register as Admin

1. Navigate to `http://localhost:5173/register`
2. Select "Admin" radio button
3. Fill in username, email, password
4. Click "Create Account"
5. Redirected to `/admin/dashboard`

### Login

1. Navigate to `http://localhost:5173/login`
2. Enter username and password
3. Click "Sign In"
4. Automatically redirected based on role:
   - Admin → `/admin/dashboard`
   - Student → `/dashboard`

## 🔒 Security Features

1. **Password Hashing**: All passwords are hashed using bcrypt
2. **JWT Tokens**: Short-lived tokens (30 minutes by default)
3. **Role-Based Access**: Middleware checks user roles before accessing protected routes
4. **Error Handling**: 
   - "Username already exists" when registering duplicate username
   - "Email already exists" when registering duplicate email
   - "Incorrect username or password" for invalid login

## 🗄️ Database Schema

### Users Table

```sql
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('admin', 'student') NOT NULL DEFAULT 'student',
    test_history JSON DEFAULT '[]',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

## 🐛 Troubleshooting

### MySQL Connection Issues

**Error**: `Access denied for user`
- **Solution**: Check username and password in `.env` file

**Error**: `Unknown database 'smartqa_db'`
- **Solution**: Create database: `CREATE DATABASE smartqa_db;`

### Frontend API Connection Issues

**Error**: `Network Error` or `CORS Error`
- **Solution**: Ensure backend is running on `http://localhost:8000`
- Check `VITE_API_BASE_URL` in frontend `.env`

### JWT Token Issues

**Error**: `Could not validate credentials`
- **Solution**: Token expired or invalid. Logout and login again.

### Password Verification Issues

**Error**: `Incorrect username or password`
- **Solution**: Ensure password is correctly hashed in database
- Check that you're using the correct username

## 📚 Code Structure

### Backend

```
backend_fastapi/
├── main.py              # FastAPI app entry point
├── database.py          # Database connection and session
├── models.py            # SQLAlchemy models (User, Test, etc.)
├── schemas.py           # Pydantic schemas for validation
├── config.py            # Configuration settings
├── routers/
│   ├── auth.py          # Authentication endpoints
│   ├── admin.py         # Admin endpoints
│   └── user.py          # Student endpoints
└── utils/
    └── auth.py          # Auth utilities (hash, verify, JWT)
```

### Frontend

```
frontend_react/src/
├── pages/
│   ├── LoginPage.jsx    # Login page
│   ├── RegisterPage.jsx # Registration page
│   ├── AdminDashboard.jsx
│   └── UserDashboard.jsx
├── components/
│   └── ProtectedRoute.jsx # Route protection middleware
├── contexts/
│   └── AuthContext.jsx  # Authentication context
└── config/
    └── api.js           # API configuration
```

## 🎯 Next Steps

Once authentication is working, you can extend the system with:

1. **Document Upload**: Add PDF/DOCX processing
2. **AI Q&A**: Integrate Gemini API for document-based questions
3. **Quiz Module**: Allow admins to create tests, students to take them
4. **Analytics**: Track user progress and test performance

## 📞 Support

For issues or questions:
1. Check error messages in browser console (F12)
2. Check backend logs in terminal
3. Verify database connection and credentials
4. Ensure all dependencies are installed

---

**Built with**: FastAPI + MySQL + SQLAlchemy + JWT + React + TailwindCSS


# Quick Start Guide - Authentication System

Get your authentication system up and running in 5 minutes!

## Prerequisites

- Python 3.8+
- Node.js 16+
- MySQL 8.0+

## Step-by-Step Setup

### 1. Backend Setup (2 minutes)

```bash
# Navigate to backend directory
cd backend_fastapi

# Install Python dependencies
pip install -r requirements.txt

# Configure database (edit .env file)
# Set your MySQL credentials:
# MYSQL_HOST=localhost
# MYSQL_PORT=3306
# MYSQL_USER=root
# MYSQL_PASSWORD=your_password
# MYSQL_DATABASE=smartqa_db

# Setup database and create tables
python setup_database.py

# Start backend server
python main.py
```

Backend will be running at: `http://localhost:8000`

### 2. Frontend Setup (2 minutes)

```bash
# Navigate to frontend directory
cd frontend_react

# Install Node dependencies
npm install

# Configure API URL (edit .env file)
# VITE_API_BASE_URL=http://localhost:8000

# Start frontend server
npm run dev
```

Frontend will be running at: `http://localhost:5173`

### 3. Test Authentication (1 minute)

1. **Create Admin Account**:
   - Go to `http://localhost:5173/register`
   - Select "Admin" radio button
   - Enter: username, email, password
   - Click "Create Account"
   - You'll be redirected to `/admin/dashboard`

2. **Create Student Account**:
   - Go to `http://localhost:5173/register`
   - Select "Student" radio button
   - Enter: username, email, password
   - Click "Create Account"
   - You'll be redirected to `/dashboard`

3. **Login**:
   - Go to `http://localhost:5173/login`
   - Enter username and password
   - Click "Sign In"
   - Redirected based on role

## Default Admin Credentials

After running `setup_database.py`, you can login with:

- **Username**: `admin`
- **Password**: `admin123`
- **Email**: `admin@example.com`

**⚠️ Change these credentials in production!**

## Quick Test with cURL

### Register Student
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "student1",
    "email": "student1@example.com",
    "password": "password123",
    "role": "student"
  }'
```

### Login
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "student1",
    "password": "password123"
  }'
```

### Get Current User (with JWT token)
```bash
curl -X GET http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Common Issues

### "Access denied for user"
- Check MySQL username/password in `.env`
- Ensure MySQL server is running: `sudo systemctl start mysql`

### "Database doesn't exist"
- Run: `python setup_database.py`
- Or manually: `CREATE DATABASE smartqa_db;`

### "Module not found"
- Backend: `pip install -r requirements.txt`
- Frontend: `npm install`

### "CORS Error"
- Check backend is running on port 8000
- Check frontend API URL in `.env`

## What's Working

✅ User registration (Admin/Student)  
✅ User login with JWT  
✅ Password hashing with bcrypt  
✅ Duplicate username/email prevention  
✅ Incorrect password handling  
✅ Role-based access control  
✅ Protected routes  
✅ Persistent login (localStorage)  
✅ Automatic role-based redirects  

## Next Steps

1. **Customize JWT expiration**: Edit `ACCESS_TOKEN_EXPIRE_MINUTES` in `.env`
2. **Change secret key**: Update `SECRET_KEY` in `.env`
3. **Add document upload**: Integrate file processing
4. **Add AI features**: Connect Gemini API
5. **Create tests**: Build quiz module

## File Structure

```
Backend:
backend_fastapi/
├── main.py              # Start here
├── models.py            # User model with role
├── routers/auth.py      # Register/login endpoints
├── utils/auth.py       # Password & JWT functions
└── setup_database.py    # Database setup script

Frontend:
frontend_react/src/
├── pages/
│   ├── LoginPage.jsx    # Login UI
│   └── RegisterPage.jsx # Registration UI
├── contexts/AuthContext.jsx  # Auth state management
└── components/ProtectedRoute.jsx  # Route guards
```

## Support

- 📖 Full documentation: `AUTHENTICATION_SETUP.md`
- 🐛 Check browser console (F12) for errors
- 📝 Check backend terminal for logs

---

**Happy Coding! 🚀**


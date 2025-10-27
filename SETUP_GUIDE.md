# 🚀 Smart QA Agent - Complete Setup Guide

This guide will help you set up and run the Smart QA Agent application from scratch.

---

## 📋 Prerequisites

### Required Software
1. **Python 3.9+** - [Download](https://www.python.org/downloads/)
2. **Node.js 16+** and npm - [Download](https://nodejs.org/)
3. **MySQL 8.0+** - [Download](https://dev.mysql.com/downloads/mysql/)
4. **Git** - [Download](https://git-scm.com/downloads/)

### Verify Installations
```powershell
python --version  # Should show Python 3.9 or higher
node --version    # Should show Node 16 or higher
npm --version     # Should show npm 8 or higher
mysql --version   # Should show MySQL 8.0 or higher
```

---

## 🗄️ Step 1: Database Setup

### 1.1 Create MySQL Database

Open MySQL command line or MySQL Workbench and run:

```sql
CREATE DATABASE qa_agent_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 1.2 Create Database User (Optional)

```sql
CREATE USER 'qa_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON qa_agent_db.* TO 'qa_user'@'localhost';
FLUSH PRIVILEGES;
```

### 1.3 Verify Database

```sql
SHOW DATABASES;
USE qa_agent_db;
```

---

## 🔧 Step 2: Backend Setup (FastAPI)

### 2.1 Navigate to Backend Directory

```powershell
cd backend_fastapi
```

### 2.2 Create Virtual Environment

```powershell
python -m venv venv
```

### 2.3 Activate Virtual Environment

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 2.4 Install Dependencies

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

### 2.5 Configure Environment Variables

The application will use the `config.env` file in the root directory, but you can also create a `.env` file in `backend_fastapi/` directory:

**backend_fastapi/.env** (if you want to override root config):
```env
# Database Configuration
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=Keerthu@73380
MYSQL_DATABASE=qa_agent_db

# JWT Configuration
SECRET_KEY=your-secret-key-change-this-in-production-2024
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Gemini API Key (already configured)
GEMINI_API_KEY=AIzaSyClBuvh8RkUgaHIKssBVBwrvF9j4iv6-H0
GOOGLE_AI_API_KEY=AIzaSyClBuvh8RkUgaHIKssBVBwrvF9j4iv6-H0

# File Upload Settings
MAX_FILE_SIZE=209715200
UPLOAD_DIR=uploads
TEMP_DIR=temp

# Vector Database
VECTOR_DB_PATH=vector_db
EMBEDDING_MODEL=all-MiniLM-L6-v2
```

**Note:** Update `MYSQL_PASSWORD` with your MySQL root password or the user password you created.

### 2.6 Create Required Directories

```powershell
mkdir uploads
mkdir temp
mkdir vector_db
mkdir chroma_db
```

### 2.7 Initialize Database Tables

Run the FastAPI server once to auto-create tables:

```powershell
python main.py
```

You should see:
```
🚀 Starting Smart Document & Test QA Agent Backend
📁 Upload Directory: uploads
🗄️  Database: qa_agent_db
🌐 Port: 8000
```

Press `Ctrl+C` to stop once you see tables are created.

### 2.8 Verify Backend is Running

Visit: http://localhost:8000

You should see:
```json
{
  "message": "Smart Document & Test QA Agent API",
  "version": "1.0.0",
  "status": "running",
  "docs": "/docs"
}
```

API Documentation: http://localhost:8000/docs

---

## ⚛️ Step 3: Frontend Setup (React)

### 3.1 Open New Terminal

Keep the backend running and open a new terminal/PowerShell window.

### 3.2 Navigate to Frontend Directory

```powershell
cd frontend_react
```

### 3.3 Install Dependencies

```powershell
npm install
```

This will install all required packages including:
- React
- React Router
- Framer Motion
- face-api.js
- Tailwind CSS
- Axios
- and more...

### 3.4 Download Face Detection Models

The proctoring feature requires face-api.js models. Create a `public/models` directory and download the models:

```powershell
# Create models directory
mkdir public\models

# Download models from: https://github.com/justadudewhohacks/face-api.js-models
# Place these files in public/models/:
# - tiny_face_detector_model-weights_manifest.json
# - tiny_face_detector_model-shard1
# - face_landmark_68_model-weights_manifest.json
# - face_landmark_68_model-shard1
# - face_recognition_model-weights_manifest.json
# - face_recognition_model-shard1
```

**Quick Download Option:**
```powershell
# You can download from the GitHub repository:
# https://github.com/justadudewhohacks/face-api.js-models/tree/master/weights
```

### 3.5 Configure API Base URL

Check `frontend_react/src/config/api.js`:

```javascript
export const API_BASE_URL = 'http://localhost:8000';
```

Ensure it points to your backend server.

### 3.6 Start Development Server

```powershell
npm run dev
```

You should see:
```
VITE v4.5.0  ready in 500 ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
```

---

## 🎯 Step 4: Create Initial Users

### 4.1 Register Admin User

1. Open browser: http://localhost:5173
2. Click "Sign Up"
3. Fill in details:
   - Username: `admin`
   - Email: `admin@example.com`
   - Password: `admin123`
   - Role: **Admin**
4. Click "Sign Up"

### 4.2 Register Student User

1. Click "Sign Up" again
2. Fill in details:
   - Username: `student1`
   - Email: `student@example.com`
   - Password: `student123`
   - Role: **Student**
3. Click "Sign Up"

---

## ✅ Step 5: Test the Application

### 5.1 Test Admin Features

1. Login as Admin (admin@example.com / admin123)
2. Navigate to "Create Test"
3. Generate a test using AI:
   - Test Name: `Data Science Basics`
   - Topic: `Data Science`
   - Number of Questions: `25`
   - Difficulty: `Medium`
4. Click "Generate with AI"
5. View created test

### 5.2 Test Student Features

1. Logout and login as Student (student@example.com / student123)
2. Upload a document:
   - Go to "Upload Document"
   - Upload a PDF/DOCX file
   - View uploaded document
3. Take a test:
   - Go to "Available Tests"
   - Select the test created by admin
   - Start test (Camera will activate for proctoring)
   - Answer questions
   - Submit test

### 5.3 Test Document Q&A

1. As Student, go to "My Documents"
2. Click on an uploaded document
3. Ask a question about the document
4. Gemini AI will provide an answer

---

## 🔍 Troubleshooting

### Backend Issues

**Issue: Database Connection Error**
```
Solution: Check MySQL is running and credentials in .env are correct
```

**Issue: Module Not Found**
```powershell
Solution: Ensure virtual environment is activated and dependencies are installed
pip install -r requirements.txt
```

**Issue: Port 8000 Already in Use**
```powershell
Solution: Change port in main.py or kill process on port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Frontend Issues

**Issue: npm install fails**
```powershell
Solution: Clear npm cache and try again
npm cache clean --force
npm install
```

**Issue: Face-api.js models not loading**
```
Solution: Ensure models are in public/models/ directory
Check browser console for 404 errors
```

**Issue: API calls failing (CORS)**
```
Solution: Ensure backend CORS is configured correctly
Check backend console for CORS errors
```

### MySQL Issues

**Issue: Can't connect to MySQL**
```powershell
Solution: Check MySQL service is running
services.msc → MySQL → Start
```

**Issue: Access Denied**
```
Solution: Check username/password in .env file
Reset MySQL password if needed
```

---

## 📱 Step 6: Test API Endpoints

### Using FastAPI Swagger UI

Visit: http://localhost:8000/docs

This provides an interactive API documentation where you can test all endpoints.

### Using Postman/Thunder Client

**1. Register User**
```http
POST http://localhost:8000/api/auth/register
Content-Type: application/json

{
  "username": "testuser",
  "email": "test@example.com",
  "password": "test123",
  "role": "student"
}
```

**2. Login**
```http
POST http://localhost:8000/api/auth/login
Content-Type: application/json

{
  "email": "test@example.com",
  "password": "test123"
}
```

Response:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "role": "student"
}
```

**3. Get Documents (Authenticated)**
```http
GET http://localhost:8000/api/documents/all
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

---

## 🎨 Optional: Customize the Application

### Change Theme Colors

Edit `frontend_react/tailwind.config.js`:

```javascript
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: '#3B82F6',  // Change primary color
        accent: '#8B5CF6',   // Change accent color
      }
    }
  }
}
```

### Add More Test Topics

Edit `backend_fastapi/utils/gemini_client.py` to add more topics in the test generation prompt.

---

## 🚀 Step 7: Production Deployment

### Backend (FastAPI)

**Option 1: Docker**
```dockerfile
# Use the provided Dockerfile in backend_fastapi/
docker build -t qa-agent-backend .
docker run -p 8000:8000 qa-agent-backend
```

**Option 2: Gunicorn**
```powershell
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

### Frontend (React)

**Build for Production:**
```powershell
cd frontend_react
npm run build
```

This creates a `dist/` folder with optimized production files.

**Deploy to:**
- Netlify
- Vercel
- AWS S3 + CloudFront
- Nginx

---

## 📚 Additional Resources

### Documentation Links
- FastAPI: https://fastapi.tiangolo.com/
- React: https://react.dev/
- face-api.js: https://github.com/justadudewhohacks/face-api.js
- Gemini API: https://ai.google.dev/gemini-api/docs

### Project Structure
```
QA_Agent/
├── backend_fastapi/
│   ├── main.py              # FastAPI application
│   ├── models.py            # Database models
│   ├── schemas.py           # Pydantic schemas
│   ├── database.py          # Database connection
│   ├── config.py            # Configuration
│   ├── routers/             # API routers
│   │   ├── auth.py
│   │   ├── admin.py
│   │   ├── documents.py
│   │   ├── tests.py
│   │   └── proctor.py
│   ├── utils/               # Utility functions
│   │   ├── auth.py
│   │   ├── gemini_client.py
│   │   ├── document_processor.py
│   │   └── text_extractors.py
│   └── requirements.txt
│
├── frontend_react/
│   ├── src/
│   │   ├── components/      # Reusable components
│   │   │   ├── Layout.jsx
│   │   │   └── ProctoringMonitor.jsx
│   │   ├── pages/           # Page components
│   │   │   ├── LoginPage.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── TakeTest.jsx
│   │   │   └── sections/
│   │   │       ├── MyDocumentsSection.jsx
│   │   │       └── AskAISection.jsx
│   │   ├── config/          # Configuration
│   │   │   └── api.js
│   │   └── main.jsx
│   └── package.json
│
├── config.env               # Environment variables
└── REFACTORING_COMPLETE.md  # Features documentation
```

---

## 🎉 You're All Set!

Your Smart QA Agent application is now fully configured and ready to use!

**Access Points:**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

**Default Test Accounts:**
- Admin: admin@example.com / admin123
- Student: student@example.com / student123

---

**Need Help?**
- Check the API documentation at `/docs`
- Review `REFACTORING_COMPLETE.md` for feature details
- Check browser console for frontend errors
- Check backend terminal for API errors

**Happy Testing! 🚀**


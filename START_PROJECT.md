# 🚀 Quick Start Guide - Smart QA Agent

## One-Time Setup (First Time Only)

### Step 1: Database Setup
```sql
-- Open MySQL and run:
CREATE DATABASE qa_agent_db;
```

### Step 2: Backend Setup
```powershell
# In PowerShell (run from project root)
cd backend_fastapi
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Step 3: Frontend Setup
```powershell
# In a NEW PowerShell window
cd frontend_react
npm install
```

### Step 4: Download Face Detection Models (Optional - for Proctoring)
Download models from: https://github.com/justadudewhohacks/face-api.js-models

Place in: `frontend_react/public/models/`

Required files:
- `tiny_face_detector_model-weights_manifest.json`
- `tiny_face_detector_model-shard1`
- `face_landmark_68_model-weights_manifest.json`
- `face_landmark_68_model-shard1`
- `face_recognition_model-weights_manifest.json`
- `face_recognition_model-shard1`

---

## Daily Use (Every Time You Want to Run)

### Terminal 1: Start Backend

```powershell
# From project root
cd backend_fastapi
.\venv\Scripts\Activate.ps1
python main.py
```

**Expected Output:**
```
🚀 Starting Smart Document & Test QA Agent Backend
📁 Upload Directory: uploads
🗄️  Database: qa_agent_db
🌐 Port: 8000
🔑 Gemini API Key: ✅ Configured
```

**Backend URL:** http://localhost:8000  
**API Docs:** http://localhost:8000/docs

---

### Terminal 2: Start Frontend

```powershell
# From project root (NEW terminal)
cd frontend_react
npm run dev
```

**Expected Output:**
```
VITE v4.5.0  ready in 500 ms
➜  Local:   http://localhost:5173/
```

**Frontend URL:** http://localhost:5173

---

## ✅ Verify Setup

### 1. Check Backend
Open: http://localhost:8000

Should see:
```json
{
  "message": "Smart Document & Test QA Agent API",
  "version": "1.0.0",
  "status": "running"
}
```

### 2. Check Frontend
Open: http://localhost:5173

Should see: Login/Signup page

---

## 🎯 Create Test Accounts

### Create Admin Account
1. Go to http://localhost:5173
2. Click "Sign Up"
3. Enter:
   - Username: `admin`
   - Email: `admin@test.com`
   - Password: `admin123`
   - **Role: Admin** ⭐
4. Click "Sign Up"

### Create Student Account
1. Click "Sign Up" again
2. Enter:
   - Username: `student`
   - Email: `student@test.com`
   - Password: `student123`
   - **Role: Student** ⭐
3. Click "Sign Up"

---

## 🧪 Quick Test

### Test Admin Features
1. Login as admin (admin@test.com / admin123)
2. Go to "Create Test"
3. Fill in:
   - Test Name: `Data Science Test`
   - Topic: `Machine Learning`
   - Questions: `25`
   - Difficulty: `Medium`
4. Click "Generate with AI"
5. Wait 5-10 seconds for Gemini to generate questions
6. Test created! ✅

### Test Student Features
1. Logout and login as student (student@test.com / student123)
2. Go to "Available Tests"
3. Click on the test created by admin
4. Click "Start Test"
5. Camera will activate (allow permission)
6. Answer questions
7. Submit test
8. View score ✅

---

## 📂 Test Document Features

### Upload Document
1. Login as student
2. Go to "Upload Document"
3. Upload a PDF, DOCX, or TXT file
4. Wait for processing
5. Document appears in "My Documents"

### Ask AI Questions
1. Go to "My Documents"
2. Select a document
3. Click "Ask AI"
4. Type a question about the document
5. Get AI-powered answer from Gemini ✅

---

## 🛑 Stop the Servers

### Stop Backend
In the backend terminal: Press `Ctrl + C`

### Stop Frontend
In the frontend terminal: Press `Ctrl + C`

---

## 🔧 Troubleshooting

### Backend Issues

**Error: ModuleNotFoundError**
```powershell
# Make sure venv is activated
cd backend_fastapi
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**Error: Database Connection Failed**
```powershell
# Check MySQL is running
services.msc → MySQL → Start

# Verify credentials in config.env
```

**Error: Port 8000 already in use**
```powershell
# Find and kill process
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Frontend Issues

**Error: npm install fails**
```powershell
# Clear cache
npm cache clean --force
rm -rf node_modules
npm install
```

**Error: Port 5173 in use**
```powershell
# Vite will automatically try next port (5174, 5175, etc.)
# Or kill the process on port 5173
netstat -ano | findstr :5173
taskkill /PID <PID> /F
```

**Error: Face detection not working**
- Models not downloaded or in wrong location
- Check `frontend_react/public/models/` has all 6 files
- Check browser console for 404 errors

---

## 📍 Important URLs

| Service | URL | Description |
|---------|-----|-------------|
| Frontend | http://localhost:5173 | Main application |
| Backend API | http://localhost:8000 | REST API |
| API Docs | http://localhost:8000/docs | Interactive API documentation |
| Health Check | http://localhost:8000/api/health | Backend health status |

---

## 📚 Documentation

- **[README_REFACTORED.md](./README_REFACTORED.md)** - Project overview
- **[SETUP_GUIDE.md](./SETUP_GUIDE.md)** - Detailed setup guide
- **[REFACTORING_COMPLETE.md](./REFACTORING_COMPLETE.md)** - All features
- **[IMPLEMENTATION_SUMMARY.md](./IMPLEMENTATION_SUMMARY.md)** - What was built

---

## 🎓 Sample Test Workflow

### As Admin:
1. ✅ Login
2. ✅ Generate test with AI (25 questions on Data Science)
3. ✅ View test questions
4. ✅ Make test active

### As Student:
1. ✅ Login
2. ✅ Upload study materials (PDF/DOCX)
3. ✅ Ask AI questions about materials
4. ✅ Take the test (with AI proctoring)
5. ✅ Submit and view score

---

## 🔒 Default Credentials

**Admin:**
- Email: `admin@test.com`
- Password: `admin123`

**Student:**
- Email: `student@test.com`
- Password: `student123`

---

## ⚙️ Configuration Files

**Backend Config:** `config.env` (root) or `backend_fastapi/.env`
```env
GEMINI_API_KEY=AIzaSyClBuvh8RkUgaHIKssBVBwrvF9j4iv6-H0
MYSQL_PASSWORD=Keerthu@73380
MYSQL_DATABASE=qa_agent_db
```

**Frontend Config:** `frontend_react/src/config/api.js`
```javascript
export const API_BASE_URL = 'http://localhost:8000';
```

---

## 🎉 You're Ready!

Both servers are running:
- ✅ Backend on http://localhost:8000
- ✅ Frontend on http://localhost:5173

**Next Steps:**
1. Create admin and student accounts
2. Generate a test with AI
3. Upload documents
4. Take a test with proctoring
5. Explore all features!

---

**Need help?** Check the detailed guides:
- [SETUP_GUIDE.md](./SETUP_GUIDE.md) - Step-by-step setup
- [REFACTORING_COMPLETE.md](./REFACTORING_COMPLETE.md) - Feature documentation

**Happy Learning! 🚀📚**


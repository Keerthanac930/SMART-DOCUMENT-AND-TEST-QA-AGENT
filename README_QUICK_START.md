# 🚀 QA Agent - Quick Start Guide

## Project Structure (Clean & Simple)

```
QA_Agent/
├── backend_fastapi/      ← Backend (FastAPI, Port 8000)
├── frontend_react/       ← Frontend (React, Port 3000)
├── START_BACKEND.ps1     ← Start backend script
├── START_FRONTEND.ps1    ← Start frontend script
└── Archive/              ← Old files (ignore)
```

## 🎯 Quick Start (3 Steps)

### 1️⃣ Start Backend (Port 8000)

Open PowerShell in project root:

```powershell
.\START_BACKEND.ps1
```

This will:
- ✅ Create `.env` with Gemini API key if missing
- ✅ Activate virtual environment
- ✅ Install dependencies
- ✅ Start FastAPI server on http://localhost:8000

**API Documentation:** http://localhost:8000/docs

### 2️⃣ Start Frontend (Port 3000)

Open **NEW** PowerShell in project root:

```powershell
.\START_FRONTEND.ps1
```

This will:
- ✅ Install npm dependencies
- ✅ Start React dev server on http://localhost:3000

**Frontend URL:** http://localhost:3000

### 3️⃣ Use the Application

1. **Signup:** Create account (select Admin or Student)
2. **Login:** Email + password → Auto-redirect based on role
   - **Admin** → `/admin/dashboard`
   - **Student** → `/dashboard`

---

## 🔑 Key Features

### Backend (`backend_fastapi`)
- ✅ **Port 8000** (FastAPI + Uvicorn)
- ✅ **CORS** configured for `localhost:3000`
- ✅ **Routes:**
  - `/api/auth` → Login, Signup (role-based)
  - `/api/tests` → Create/fetch tests
  - `/api/scores` → Student scores
  - `/api/proctor` → AI proctoring logs
  - `/api/ai` → Gemini-powered Q&A
- ✅ **Auto-creates:** `uploads/`, `temp/`, `vector_db/`
- ✅ **Gemini API:** Auto-configured from `.env`

### Frontend (`frontend_react`)
- ✅ **Port 3000** (Vite)
- ✅ **Tailwind CSS** + Dark mode
- ✅ **Role-based dashboards:**
  - Admin: Create tests, view scores, manage docs
  - Student: Take quizzes, ask AI, upload docs
- ✅ **AI Proctoring:**
  - Camera + microphone monitoring
  - Face detection (10 violation limit)
  - Logs to `/api/proctor/log`

---

## 🔧 Configuration

### Backend `.env` (auto-created)

```env
GEMINI_API_KEY=AIzaSyClBuvh8RkUgaHIKssBVBwrvF9j4iv6-H0
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=
MYSQL_DATABASE=smartqa_db
```

### Frontend API Config

```javascript
// frontend_react/src/config/api.js
const API_BASE_URL = 'http://localhost:8000'
```

---

## 🧠 Authentication Flow

### Signup:
```
POST /api/auth/register
{
  "username": "john",
  "email": "john@example.com",
  "password": "pass123",
  "role": "admin" | "student"
}
```

### Login:
```
POST /api/auth/login
{
  "email": "john@example.com",
  "password": "pass123"
}
Response: { "access_token": "...", "role": "admin" }
```

Frontend redirects:
- `role === 'admin'` → `/admin/dashboard`
- `role === 'student'` → `/dashboard`

---

## 🎓 AI Proctoring

When student starts test:
1. ✅ Webcam & mic activate
2. ✅ Face detection monitors student
3. ✅ Loud noise detection
4. ✅ Violation counter (max 10)
5. ✅ Logs to database via `/api/proctor/log`

---

## 📦 Dependencies

### Backend
- FastAPI
- Uvicorn
- SQLAlchemy
- PyMySQL
- Google Generative AI (Gemini)
- python-dotenv
- ChromaDB

### Frontend
- React 18
- Vite
- Tailwind CSS
- Axios
- React Router
- React Webcam
- Framer Motion

---

## 🚨 Troubleshooting

### Backend won't start:
```powershell
cd backend_fastapi
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8000
```

### Frontend won't start:
```powershell
cd frontend_react
npm install
npm run dev
```

### CORS errors:
- Ensure backend is running on port 8000
- Frontend on port 3000
- Check `backend_fastapi/main.py` CORS settings

### Database errors:
- Install MySQL
- Create database: `smartqa_db`
- Update `.env` with MySQL credentials

---

## 📝 Manual Start (Alternative)

### Backend:
```powershell
cd backend_fastapi
.\venv\Scripts\Activate.ps1
python -m uvicorn main:app --reload --port 8000
```

### Frontend:
```powershell
cd frontend_react
npm run dev
```

---

## ✅ System Verification

1. ✅ Backend: http://localhost:8000/api/health
2. ✅ Frontend: http://localhost:3000
3. ✅ API Docs: http://localhost:8000/docs
4. ✅ Gemini API: Check startup logs

---

## 🎉 You're All Set!

- **Backend:** http://localhost:8000
- **Frontend:** http://localhost:3000
- **Docs:** http://localhost:8000/docs

Happy coding! 🚀


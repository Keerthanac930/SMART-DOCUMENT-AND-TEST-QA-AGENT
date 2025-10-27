# ✅ QA Agent - Deployment Checklist

## Pre-Start Verification

### 1. Directory Structure
- [x] `backend_fastapi/` exists
- [x] `frontend_react/` exists  
- [x] Old folders moved to `Archive/`
- [x] `START_BACKEND.ps1` in root
- [x] `START_FRONTEND.ps1` in root

### 2. Backend Configuration
```powershell
cd backend_fastapi
cat .env
```
**Check for:**
- [x] `GEMINI_API_KEY=AIzaSyClBuvh8RkUgaHIKssBVBwrvF9j4iv6-H0`
- [x] MySQL credentials
- [x] All env vars present

### 3. Frontend Configuration
```powershell
cd frontend_react
cat vite.config.js
```
**Verify:**
- [x] Port: 3000
- [x] Proxy to localhost:8000

---

## Quick Start Commands

### Terminal 1 - Backend
```powershell
.\START_BACKEND.ps1
```
**Expected Output:**
```
🚀 Starting Smart Document & Test QA Agent Backend
📁 Upload Directory: uploads
📁 Temp Directory: temp
📁 Vector DB Path: vector_db
🔑 Gemini API Key: ✅ Configured
🗄️  Database: smartqa_db
🌐 Port: 8000
🔐 CORS Enabled for: http://localhost:3000

INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Terminal 2 - Frontend
```powershell
.\START_FRONTEND.ps1
```
**Expected Output:**
```
🚀 Starting React dev server on http://localhost:3000
🔗 Backend API: http://localhost:8000

VITE v4.5.0  ready in 1234 ms

➜  Local:   http://localhost:3000/
```

---

## System Verification

### 1. Backend Health Check
```powershell
curl http://localhost:8000/api/health
```
**Expected:**
```json
{
  "status": "healthy",
  "timestamp": "2025-10-26T...",
  "gemini_api_configured": true,
  "database": "smartqa_db"
}
```

### 2. Frontend Access
Open browser: http://localhost:3000

**Should See:**
- Login/Signup page
- No console errors
- Dark mode toggle works

### 3. API Documentation
Open: http://localhost:8000/docs

**Should See:**
- All API endpoints
- `/api/auth`, `/api/tests`, `/api/scores`, etc.
- Interactive testing interface

---

## Feature Testing

### Test 1: Admin Signup & Login
1. Go to http://localhost:3000/signup
2. Fill form:
   - Username: `admin1`
   - Email: `admin@test.com`
   - Password: `password123`
   - **Select: Admin**
3. Click "Create Account"
4. Should redirect to `/admin/dashboard`

### Test 2: Student Signup & Login
1. Go to http://localhost:3000/signup
2. Fill form:
   - Username: `student1`
   - Email: `student@test.com`
   - Password: `password123`
   - **Select: Student**
3. Click "Create Account"
4. Should redirect to `/dashboard`

### Test 3: Role-Based Redirect
1. Logout
2. Login with `admin@test.com` → Should go to `/admin/dashboard`
3. Logout
4. Login with `student@test.com` → Should go to `/dashboard`

### Test 4: AI Proctoring
1. Login as student
2. Start a test
3. **Should see:**
   - Camera preview (top right)
   - Mic indicator (green)
   - Violation counter: 0/10

### Test 5: Gemini API
1. As student, go to "Ask AI"
2. Type: "What is machine learning?"
3. **Should get:** AI-generated response
4. **Console:** No API errors

---

## Troubleshooting

### Issue: Backend won't start

**Solution:**
```powershell
cd backend_fastapi
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8000
```

### Issue: Frontend won't start

**Solution:**
```powershell
cd frontend_react
Remove-Item -Recurse -Force node_modules
npm install
npm run dev
```

### Issue: CORS Error

**Check:**
1. Backend running on port 8000
2. Frontend on port 3000
3. `backend_fastapi/main.py` has:
```python
allow_origins=["http://localhost:3000", ...]
```

### Issue: Camera/Mic not working

**Browser Permissions:**
1. Chrome: Click lock icon → Camera/Mic → Allow
2. Must use HTTPS or localhost
3. Check browser console for errors

### Issue: Gemini API not responding

**Verify:**
```powershell
cd backend_fastapi
cat .env | Select-String "GEMINI"
```
Should show: `GEMINI_API_KEY=AIzaSyC...`

**Test directly:**
```python
from config import settings
print(settings.get_gemini_key)
```

---

## Port Conflicts

### If port 8000 is in use:
```powershell
# Find process
netstat -ano | findstr :8000
# Kill process
taskkill /PID <PID> /F
```

### If port 3000 is in use:
```powershell
# Find process
netstat -ano | findstr :3000
# Kill process
taskkill /PID <PID> /F
```

---

## Database Setup (First Time)

### 1. Install MySQL
Download from: https://dev.mysql.com/downloads/mysql/

### 2. Create Database
```sql
CREATE DATABASE smartqa_db;
USE smartqa_db;
```

### 3. Update .env
```env
MYSQL_PASSWORD=your_mysql_password
```

### 4. Run Backend
Tables will be created automatically via SQLAlchemy.

---

## Production Deployment

### Backend
1. Update `.env`:
   ```env
   SECRET_KEY=<generate-strong-key>
   MYSQL_HOST=<production-host>
   MYSQL_PASSWORD=<strong-password>
   ```
2. Set `reload=False` in `main.py`
3. Use gunicorn or similar
4. Enable HTTPS
5. Update CORS origins

### Frontend
1. Build:
   ```bash
   npm run build
   ```
2. Deploy `dist/` folder to hosting
3. Update API_BASE_URL to production backend
4. Enable HTTPS

---

## Final Checklist

Before going live:

- [ ] Backend starts without errors
- [ ] Frontend starts without errors
- [ ] Can signup as Admin
- [ ] Can signup as Student
- [ ] Login redirects correctly
- [ ] Camera/mic permissions work
- [ ] Gemini API responds
- [ ] Database connects
- [ ] API documentation accessible
- [ ] No console errors
- [ ] CORS works
- [ ] All pages load
- [ ] Dark mode works
- [ ] Proctoring tracks violations
- [ ] Tests can be created (Admin)
- [ ] Tests can be taken (Student)

---

## 🎉 All Systems Ready!

If all checks pass, your QA Agent system is fully operational!

**Start with:**
1. `.\START_BACKEND.ps1`
2. `.\START_FRONTEND.ps1` (new terminal)
3. Visit http://localhost:3000

Happy testing! 🚀


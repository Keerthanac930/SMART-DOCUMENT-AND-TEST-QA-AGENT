# Quick Start Guide - Backend

## ⚡ Start Backend in 30 Seconds

### Step 1: Open Terminal
```powershell
cd E:\QA_Agent\backend_fastapi
```

### Step 2: Start Server
```powershell
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Step 3: Verify It's Running
Open: http://localhost:8000/docs

You should see the API documentation page.

---

## ✅ Check Everything Works

Run this command:
```powershell
python check_backend_status.py
```

Expected output:
```
✓ Database connection successful
✓ Processed: 3 documents
✓ AI functionality working
✓ Vector database has 3 embeddings
✓ All systems operational!
```

---

## 🐛 If Something Breaks

### Backend won't start?
```powershell
# Stop all Python processes
Stop-Process -Name python -Force

# Try again
cd E:\QA_Agent\backend_fastapi
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Documents not processing?
```powershell
python process_existing_documents.py
```

### Want to test everything?
```powershell
python test_complete_flow.py
```

---

## 📝 That's It!

Backend is ready. Now start the frontend:
```powershell
cd E:\QA_Agent\frontend_react
npm run dev
```

Then open: http://localhost:3000


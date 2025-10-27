# Starting the Backend Server

## Quick Start

1. **Navigate to backend directory:**
```powershell
cd E:\QA_Agent\backend_fastapi
```

2. **Activate virtual environment (if using one):**
```powershell
.\venv\Scripts\Activate.ps1
```

3. **Install/Update dependencies:**
```powershell
pip install -r requirements.txt
```

4. **Start the backend server:**
```powershell
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Alternative: Run without reload
```powershell
python main.py
```

## Check Backend Status

After starting, visit: http://localhost:8000/docs

Or run the status check:
```powershell
python check_backend_status.py
```

## Process Existing Documents

If you have unprocessed documents:
```powershell
python process_existing_documents.py
```

## Test Complete Flow

To test all functionality:
```powershell
python test_complete_flow.py
```

## Troubleshooting

### If backend won't start:
1. Check if port 8000 is already in use
2. Make sure MySQL is running (if using MySQL)
3. Check that all dependencies are installed
4. Verify .env file has correct configuration

### If documents aren't processing:
1. Run `python process_existing_documents.py`
2. Check ChromaDB directory exists
3. Verify PDF files exist in uploads folder

### If AI isn't working:
1. Check GOOGLE_GEMINI_API_KEY in config.py
2. Run `python test_ai_simple.py` to test models
3. Verify API key is valid and has quota


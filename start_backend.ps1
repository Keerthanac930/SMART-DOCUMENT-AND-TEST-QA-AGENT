# Start Backend FastAPI Server on Port 8000
# Smart Document & Test QA Agent Backend

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Starting QA Agent Backend (Port 8000)" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Navigate to backend directory
Set-Location backend_fastapi

# Check if .env exists
if (-Not (Test-Path ".env")) {
    Write-Host "⚠️  Warning: .env file not found!" -ForegroundColor Yellow
    Write-Host "Creating .env file with default configuration..." -ForegroundColor Yellow
    @"
# Database Configuration
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=
MYSQL_DATABASE=smartqa_db

# JWT Configuration
SECRET_KEY=your-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Gemini API Configuration
GEMINI_API_KEY=AIzaSyClBuvh8RkUgaHIKssBVBwrvF9j4iv6-H0
GOOGLE_GEMINI_API_KEY=AIzaSyClBuvh8RkUgaHIKssBVBwrvF9j4iv6-H0
GOOGLE_AI_API_KEY=AIzaSyClBuvh8RkUgaHIKssBVBwrvF9j4iv6-H0

# File Upload Settings
MAX_FILE_SIZE=209715200
UPLOAD_DIR=uploads
TEMP_DIR=temp
VECTOR_DB_PATH=vector_db

# Embedding Model
EMBEDDING_MODEL=all-MiniLM-L6-v2
"@ | Out-File -FilePath .env -Encoding UTF8
}

# Check if virtual environment exists
if (Test-Path "venv\Scripts\Activate.ps1") {
    Write-Host "✅ Activating virtual environment..." -ForegroundColor Green
    .\venv\Scripts\Activate.ps1
} else {
    Write-Host "⚠️  Virtual environment not found. Creating..." -ForegroundColor Yellow
    python -m venv venv
    .\venv\Scripts\Activate.ps1
    Write-Host "📦 Installing dependencies..." -ForegroundColor Green
    pip install -r requirements.txt
}

Write-Host ""
Write-Host "🚀 Starting FastAPI server on http://localhost:8000" -ForegroundColor Green
Write-Host "📚 API Docs available at http://localhost:8000/docs" -ForegroundColor Green
Write-Host ""
Write-Host "Press CTRL+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Start the server
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

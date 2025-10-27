# 🚀 Getting Started Guide

## Quick Start

### Windows Users

1. **Run the setup script:**
   ```bash
   start_complete.bat
   ```

2. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Linux/Mac Users

1. **Make the script executable:**
   ```bash
   chmod +x start_complete.sh
   ```

2. **Run the setup script:**
   ```bash
   ./start_complete.sh
   ```

3. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## Manual Setup

### Prerequisites

- Python 3.10+
- Node.js 18+
- npm or yarn

### Step 1: Backend Setup

```bash
cd backend_fastapi

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create necessary directories
mkdir uploads vector_db

# Start the server
python main.py
```

The backend will be available at `http://localhost:8000`

### Step 2: Frontend Setup

Open a new terminal:

```bash
cd frontend_react

# Install dependencies
npm install

# Start the development server
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Configuration

### Environment Variables

The backend uses environment variables for configuration. You can:

1. **Use the config.env file** (already present in root):
   - Copy `config.env` to `backend_fastapi/.env`
   - Update with your values

2. **Set environment variables directly**:
   ```bash
   # Windows PowerShell
   $env:GOOGLE_AI_API_KEY='your-api-key'
   
   # Linux/Mac
   export GOOGLE_AI_API_KEY='your-api-key'
   ```

### Required Configuration

- **Google AI API Key**: Get from [Google AI Studio](https://aistudio.google.com/app/apikey)
  - The key from your `config.env` file is: `AIzaSyClBuvh8RkUgaHIKssBVBwrvF9j4iv6-H0`

### Optional Configuration

- **Database**: SQLite is used by default (no setup needed)
- **Tesseract OCR**: For image text extraction (optional)

## First Use

### 1. Register an Admin Account

1. Navigate to http://localhost:3000
2. Click "Register"
3. Select "Admin" account type
4. Fill in your details
5. Click "Register"

### 2. Register Users

1. Logout as admin
2. Register as a regular user
3. Or login as admin and manage users from the admin dashboard

### 3. Upload Documents

1. Login as either admin or user
2. Navigate to "Upload Documents"
3. Upload PDF, DOCX, TXT, or image files
4. Documents will be processed automatically

### 4. Ask Questions

1. Use the "Ask AI" page
2. Type your question
3. Select documents to search (optional)
4. Get AI-powered answers with citations

### 5. Create Tests (Admin Only)

1. Login as admin
2. Navigate to "Admin Dashboard"
3. Click "Create Test"
4. Generate questions from uploaded documents or create manually
5. Set time limits and activate the test

### 6. Take Tests (Users)

1. Login as user
2. Navigate to "Available Tests"
3. Select a test
4. Answer questions within the time limit
5. View results and scores

## Troubleshooting

### Backend Won't Start

1. **Check Python version**: `python --version` (should be 3.10+)
2. **Check dependencies**: `pip install -r requirements.txt`
3. **Check port**: Ensure port 8000 is not in use
4. **Check API key**: Ensure Google AI API key is set

### Frontend Won't Start

1. **Check Node version**: `node --version` (should be 18+)
2. **Clear cache**: `rm -rf node_modules package-lock.json && npm install`
3. **Check port**: Ensure port 3000 is not in use

### Database Issues

- SQLite database is created automatically in `backend_fastapi/qa_agent.db`
- If issues occur, delete the database file and restart the backend

### Document Processing Issues

- Ensure PyMuPDF is installed: `pip install PyMuPDF`
- For OCR: Install Tesseract OCR
- Check file size limits (200MB max)

## API Documentation

FastAPI provides automatic API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Development

### Backend Development

```bash
cd backend_fastapi
source venv/bin/activate  # or venv\Scripts\activate on Windows
python main.py
```

### Frontend Development

```bash
cd frontend_react
npm run dev
```

### Running Tests

```bash
# Backend tests
cd backend_fastapi
pytest

# Frontend tests
cd frontend_react
npm test
```

## Production Deployment

See `SETUP_INSTRUCTIONS.md` for detailed production deployment instructions.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review API documentation
3. Check console logs for errors
4. Ensure all prerequisites are installed

## Next Steps

- Customize the UI with your branding
- Add more AI features
- Integrate with external services
- Deploy to production

---

**Note**: Make sure to change the default secret keys and API keys before deploying to production!


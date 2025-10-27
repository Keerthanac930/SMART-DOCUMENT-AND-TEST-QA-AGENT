# Smart Document & Test QA Agent Dashboard - Setup Instructions

This comprehensive setup guide will help you deploy the Smart Document & Test QA Agent Dashboard with React frontend and FastAPI backend.

## 📋 Prerequisites

### System Requirements
- Python 3.10+
- Node.js 18+
- MySQL 8.0+
- Git

### Required Software
- **Python**: For FastAPI backend
- **Node.js & npm**: For React frontend
- **MySQL**: For database storage
- **Tesseract OCR**: For image text extraction (optional)

## 🗄️ Database Setup

### 1. Install MySQL
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install mysql-server

# Windows
# Download MySQL installer from https://dev.mysql.com/downloads/installer/

# macOS
brew install mysql
```

### 2. Create Database
```sql
-- Connect to MySQL
mysql -u root -p

-- Create database
CREATE DATABASE qa_agent_db;

-- Create user (optional)
CREATE USER 'qa_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON qa_agent_db.* TO 'qa_user'@'localhost';
FLUSH PRIVILEGES;
```

## 🚀 Backend Setup (FastAPI)

### 1. Navigate to Backend Directory
```bash
cd backend_fastapi
```

### 2. Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file in the `backend_fastapi` directory:
```env
# Database Configuration
DATABASE_URL=mysql+pymysql://root:your_password@localhost:3306/qa_agent_db

# JWT Configuration
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Google Gemini API
GOOGLE_GEMINI_API_KEY=your-gemini-api-key-here

# File Upload Settings
MAX_FILE_SIZE=209715200
UPLOAD_DIR=uploads
VECTOR_DB_PATH=vector_db

# OCR Settings (Optional)
TESSERACT_PATH=/usr/bin/tesseract
```

### 5. Initialize Database
```bash
# Run database migrations (if using Alembic)
alembic upgrade head

# Or create tables directly
python -c "from database import engine, Base; Base.metadata.create_all(bind=engine)"
```

### 6. Start Backend Server
```bash
python main.py
```

The backend will be available at `http://localhost:8000`

## 🎨 Frontend Setup (React)

### 1. Navigate to Frontend Directory
```bash
cd frontend_react
```

### 2. Install Dependencies
```bash
npm install
```

### 3. Environment Configuration
Create a `.env` file in the `frontend_react` directory:
```env
VITE_API_URL=http://localhost:8000
```

### 4. Start Development Server
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## 🔧 Additional Configuration

### OCR Setup (Optional)

#### Windows
1. Download Tesseract from [UB-Mannheim](https://github.com/UB-Mannheim/tesseract/wiki)
2. Add to system PATH
3. Update `TESSERACT_PATH` in `.env`

#### Ubuntu/Debian
```bash
sudo apt install tesseract-ocr
```

#### macOS
```bash
brew install tesseract
```

### Google Gemini API Setup
1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create a new API key
3. Add the key to your `.env` file

## 🏗️ Project Structure

```
QA_Agent/
├── backend_fastapi/          # FastAPI Backend
│   ├── main.py              # Main application entry point
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database configuration
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── routers/             # API route handlers
│   │   ├── auth.py          # Authentication routes
│   │   ├── admin.py         # Admin routes
│   │   ├── user.py          # User routes
│   │   ├── tests.py         # Test routes
│   │   └── ai.py            # AI routes
│   ├── utils/               # Utility functions
│   │   ├── auth.py          # Authentication utilities
│   │   ├── gemini_client.py # Gemini AI client
│   │   └── document_processor.py # Document processing
│   └── requirements.txt     # Python dependencies
├── frontend_react/          # React Frontend
│   ├── src/
│   │   ├── components/      # Reusable components
│   │   ├── pages/           # Page components
│   │   ├── contexts/        # React contexts
│   │   └── App.jsx          # Main app component
│   ├── package.json         # Node.js dependencies
│   └── vite.config.js       # Vite configuration
└── SETUP_INSTRUCTIONS.md    # This file
```

## 🚀 Running the Application

### Development Mode

1. **Start Backend**:
   ```bash
   cd backend_fastapi
   python main.py
   ```

2. **Start Frontend**:
   ```bash
   cd frontend_react
   npm run dev
   ```

3. **Access Application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Production Mode

1. **Build Frontend**:
   ```bash
   cd frontend_react
   npm run build
   ```

2. **Serve with Production Server**:
   ```bash
   cd backend_fastapi
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

## 🔐 Initial Setup

### 1. Create Admin Account
1. Navigate to the registration page
2. Select "Admin" account type
3. Register with admin credentials

### 2. Create Test Users
1. Register regular users through the application
2. Or use the admin panel to manage users

### 3. Upload Documents
1. Login as admin or user
2. Navigate to "Upload Documents"
3. Upload PDF, DOCX, TXT, or image files

## 🧪 Testing the Application

### 1. Authentication
- Test user registration and login
- Verify JWT token functionality
- Test role-based access control

### 2. Document Upload
- Upload various file types
- Test file size limits
- Verify document processing

### 3. AI Features
- Test question answering
- Verify document-based responses
- Test AI fallback functionality

### 4. Quiz System
- Create tests as admin
- Take tests as user
- Verify scoring and results

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Error**:
   - Check MySQL service is running
   - Verify database credentials
   - Ensure database exists

2. **Frontend Build Errors**:
   - Clear node_modules and reinstall
   - Check Node.js version compatibility
   - Verify all dependencies are installed

3. **OCR Not Working**:
   - Install Tesseract OCR
   - Update TESSERACT_PATH in .env
   - Check file permissions

4. **API Connection Issues**:
   - Verify backend is running on port 8000
   - Check CORS configuration
   - Ensure API endpoints are accessible

### Debug Mode

Enable debug mode in backend:
```python
# In main.py
uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_level="debug")
```

## 📚 API Documentation

The FastAPI backend provides automatic API documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔒 Security Considerations

1. **Change Default Secrets**:
   - Update JWT secret key
   - Use strong database passwords
   - Secure API keys

2. **Production Deployment**:
   - Use HTTPS
   - Configure proper CORS
   - Set up database backups
   - Use environment variables for secrets

3. **File Upload Security**:
   - Validate file types
   - Scan for malware
   - Limit file sizes

## 📈 Monitoring and Logging

1. **Application Logs**:
   - Backend logs in console
   - Frontend logs in browser console

2. **Database Monitoring**:
   - Monitor query performance
   - Track database size
   - Set up regular backups

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section
2. Review API documentation
3. Check console logs for errors
4. Verify all prerequisites are installed

## 🎯 Next Steps

1. **Customize UI**: Modify TailwindCSS classes for branding
2. **Add Features**: Implement additional AI capabilities
3. **Scale Database**: Set up database clustering if needed
4. **Deploy**: Use Docker or cloud platforms for production deployment

---

**Note**: This is a comprehensive setup guide. Make sure to follow all steps carefully and test each component before proceeding to the next step.

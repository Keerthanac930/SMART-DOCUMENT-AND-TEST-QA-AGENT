# 🎓 Smart QA Agent - Complete Solution

> **AI-Powered Document Management & Testing Platform with Real-Time Proctoring**

A comprehensive full-stack application featuring FastAPI backend, React frontend, Gemini AI integration, and advanced AI proctoring capabilities.

---

## ✨ Key Features

### 📚 Document Management
- **Upload & Store**: PDF, DOCX, TXT file support
- **AI-Powered Q&A**: Ask questions about your documents using Gemini AI
- **View/Download/Delete**: Full CRUD operations
- **Smart Search**: Vector-based semantic search using ChromaDB

### 🧪 Testing Platform
- **AI Test Generation**: Auto-generate 25/50 question MCQ tests on any Data Science topic
- **Timed Tests**: 20-minute countdown with automatic submission
- **Real-Time Proctoring**: Face detection + audio monitoring using face-api.js
- **Violation Tracking**: Automatic test termination after 10 violations
- **Instant Results**: Immediate scoring and feedback

### 🎭 Role-Based Access
- **Admin Dashboard**: Create tests, view scores, manage users
- **Student Portal**: Take tests, upload documents, ask AI questions
- **Secure Authentication**: JWT-based with bcrypt password hashing

### 🤖 AI Integration (Gemini)
- Document Q&A
- Automated test question generation
- Content summarization
- Context-aware responses

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+
- MySQL 8.0+
- Gemini API Key (already configured)

### 1. Database Setup
```sql
CREATE DATABASE qa_agent_db;
```

### 2. Backend Setup
```powershell
cd backend_fastapi
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```
**Backend runs on:** http://localhost:8000

### 3. Frontend Setup
```powershell
cd frontend_react
npm install
npm run dev
```
**Frontend runs on:** http://localhost:5173

### 4. Access the Application
- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

---

## 📖 Documentation

- **[REFACTORING_COMPLETE.md](./REFACTORING_COMPLETE.md)** - Complete feature list and implementation details
- **[SETUP_GUIDE.md](./SETUP_GUIDE.md)** - Detailed setup instructions with troubleshooting

---

## 🏗️ Tech Stack

### Backend
- **Framework:** FastAPI
- **Database:** MySQL with SQLAlchemy ORM
- **Authentication:** JWT with python-jose
- **AI:** Google Gemini 2.0 Flash
- **Document Processing:** PyMuPDF, PyPDF2, python-docx
- **Vector DB:** ChromaDB with sentence-transformers

### Frontend
- **Framework:** React 18.2
- **Routing:** React Router DOM
- **Styling:** TailwindCSS
- **Animations:** Framer Motion
- **Face Detection:** face-api.js
- **HTTP Client:** Axios
- **Icons:** Lucide React

---

## 📁 Project Structure

```
QA_Agent/
├── backend_fastapi/          # FastAPI Backend
│   ├── main.py              # Main application
│   ├── models.py            # Database models
│   ├── schemas.py           # Pydantic schemas
│   ├── routers/             # API endpoints
│   │   ├── auth.py         # Authentication
│   │   ├── admin.py        # Admin functions
│   │   ├── documents.py    # Document management
│   │   ├── tests.py        # Test management
│   │   ├── proctor.py      # Proctoring logs
│   │   └── scores.py       # Score management
│   └── utils/              # Utilities
│       ├── gemini_client.py
│       ├── document_processor.py
│       └── text_extractors.py
│
├── frontend_react/          # React Frontend
│   ├── src/
│   │   ├── components/     # Reusable components
│   │   │   ├── Layout.jsx
│   │   │   └── ProctoringMonitor.jsx
│   │   ├── pages/          # Page components
│   │   │   ├── Dashboard.jsx
│   │   │   ├── TakeTest.jsx
│   │   │   └── sections/
│   │   └── config/
│   └── public/
│       └── models/         # face-api.js models
│
├── uploads/                # Uploaded documents
├── config.env             # Environment configuration
├── REFACTORING_COMPLETE.md
└── SETUP_GUIDE.md
```

---

## 🔐 Environment Variables

**Root: config.env**
```env
GEMINI_API_KEY=AIzaSyClBuvh8RkUgaHIKssBVBwrvF9j4iv6-H0
MYSQL_PASSWORD=Keerthu@73380
```

**Backend: backend_fastapi/.env** (optional override)
```env
MYSQL_HOST=localhost
MYSQL_DATABASE=qa_agent_db
SECRET_KEY=your-secret-key
```

---

## 📋 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login

### Documents
- `GET /api/documents/all` - Get all user documents
- `POST /api/documents/upload` - Upload document
- `GET /api/documents/:id/content` - Get document text
- `POST /api/documents/ask` - Ask AI about document
- `GET /api/documents/:id/download` - Download document
- `DELETE /api/documents/:id` - Delete document

### Tests
- `GET /api/tests/all` - Get available tests (Student)
- `POST /api/tests/submit` - Submit test answers
- `POST /api/admin/tests/generate` - Generate test with AI (Admin)
- `GET /api/admin/scores/all` - View all scores (Admin)

### Stats & Monitoring
- `GET /api/stats` - Dashboard statistics
- `POST /api/proctor/log` - Log proctoring violation

Full API documentation: http://localhost:8000/docs

---

## 🎯 User Flows

### Student Journey
1. **Register** → Choose "Student" role
2. **Login** → Access student dashboard
3. **Upload Documents** → PDF/DOCX/TXT files
4. **Ask AI** → Get instant answers from your documents
5. **Take Test** → AI proctoring monitors your session
6. **Submit** → Get immediate results

### Admin Journey
1. **Register** → Choose "Admin" role
2. **Login** → Access admin dashboard
3. **Generate Test** → Use AI to create 25/50 MCQs on any topic
4. **Monitor** → View student scores and performance
5. **Manage** → View all documents and users

---

## 🛡️ Security Features

- ✅ JWT-based authentication
- ✅ Bcrypt password hashing
- ✅ Role-based access control (RBAC)
- ✅ CORS protection
- ✅ SQL injection prevention (SQLAlchemy ORM)
- ✅ File upload validation
- ✅ Secure token storage

---

## 🎥 AI Proctoring System

### How It Works
1. **Camera Activation**: Automatically starts when test begins
2. **Face Detection**: Monitors for student presence using face-api.js
3. **Audio Monitoring**: Detects loud noises using Web Audio API
4. **Violation Logging**: Records all violations to database
5. **Automatic Termination**: Blocks test after 10 violations

### Violation Types
- ❌ No face detected
- ❌ Multiple faces detected
- ❌ Loud audio/background noise

### Visual Feedback
- 🟢 **Green** (0-4 violations): Safe zone
- 🟡 **Yellow** (5-7 violations): Warning
- 🔴 **Red** (8-10 violations): Critical - Test will terminate

---

## 🧪 Testing the Application

### Create Test Data

**1. Register Admin**
```
Email: admin@test.com
Password: admin123
Role: Admin
```

**2. Generate a Test (as Admin)**
```
Name: Data Science Fundamentals
Topic: Machine Learning
Questions: 25
Difficulty: Medium
Time: 20 minutes
```

**3. Register Student**
```
Email: student@test.com
Password: student123
Role: Student
```

**4. Take Test (as Student)**
- Camera will activate
- Answer 25 questions
- Watch proctoring monitor
- Submit before time runs out

---

## 📊 Database Schema

### Core Tables
- **users** - User accounts and authentication
- **tests** - Test definitions
- **questions** - Test questions with options
- **documents** - Uploaded documents metadata
- **results** - Test submission results
- **scores** - Simple score tracking
- **proctor_logs** - AI proctoring violation logs

Full schema details in [REFACTORING_COMPLETE.md](./REFACTORING_COMPLETE.md)

---

## 🐛 Common Issues & Solutions

### Backend Won't Start
```powershell
# Ensure MySQL is running
services.msc → MySQL → Start

# Check database credentials in config.env

# Reinstall dependencies
pip install -r requirements.txt
```

### Frontend Build Errors
```powershell
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Face Detection Not Working
```powershell
# Ensure models are in public/models/
# Download from: https://github.com/justadudewhohacks/face-api.js-models
```

### CORS Errors
```
# Backend CORS is configured for:
- http://localhost:3000
- http://localhost:5173
- http://localhost:3001
```

---

## 📈 Performance Optimizations

- ✅ Lazy loading for components
- ✅ Database indexing on frequently queried fields
- ✅ Vector search for fast document retrieval
- ✅ Optimized image compression
- ✅ Chunked file uploads
- ✅ Connection pooling for MySQL

---

## 🔮 Future Enhancements

- [ ] Email notifications
- [ ] Advanced analytics dashboard
- [ ] Bulk import/export
- [ ] Video recording during tests
- [ ] Multi-language support
- [ ] Mobile app version
- [ ] Real-time collaboration
- [ ] Integration with LMS platforms

---

## 📝 License

This project is for educational purposes.

---

## 👥 Support

For issues or questions:
1. Check [SETUP_GUIDE.md](./SETUP_GUIDE.md)
2. Review API docs at http://localhost:8000/docs
3. Check browser console for frontend errors
4. Check terminal for backend errors

---

## 🎉 Acknowledgments

- **Gemini AI** by Google for AI capabilities
- **FastAPI** for the excellent web framework
- **face-api.js** for face detection
- **React** for the frontend framework
- **TailwindCSS** for beautiful styling

---

**🚀 Ready to get started? Follow the [SETUP_GUIDE.md](./SETUP_GUIDE.md)**

**Status:** ✅ Production Ready  
**Version:** 1.0.0  
**Last Updated:** October 26, 2025

---

**Made with ❤️ for smart learning and secure testing**


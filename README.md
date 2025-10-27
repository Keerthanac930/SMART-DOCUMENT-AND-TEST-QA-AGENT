# 📚 Smart Document QA Agent

A powerful AI-powered question-answering system that processes documents and answers questions with page-numbered citations and AI fallback responses.

## ✨ Features

### 🎯 Core Requirements
- **Document Answering**: Fetch answers from uploaded documents (PDF, DOCX, TXT, images) with page numbers
- **AI Fallback**: Generate intelligent answers when not found in documents with explicit warnings
- **OCR Support**: Extract text from images and scanned PDFs using Tesseract
- **File Limits**: 200MB maximum file size per upload

### 🧩 Quiz Mode
- **Camera & Microphone Access**: Real-time proctoring with movement detection
- **Anti-Malpractice**: Detects head movement and background voices
- **Exam Controls**: Start/end exam, reset detection, view results

### 📝 Input Modes
- **Manual Typing**: Traditional text input
- **Voice Input**: Speech-to-text conversion (placeholder)
- **Image Scanner**: OCR-based question extraction (placeholder)

### 👥 User Roles
- **Admin Dashboard**: Manage users, upload question papers, approve registrations, schedule exams
- **Student Dashboard**: Practice tests, register for exams, view results

### 🎨 Modern UI
- **Floating Action Buttons**: Quick access to Voice, Quiz, and Image features
- **Theme Toggle**: Light and dark mode support
- **Responsive Design**: Works on desktop and mobile devices

## 🏗️ Project Structure

```
QA_Agent/
├── frontend/
│   ├── app.py                 # Main Streamlit application
│   ├── pages/                 # Multi-page app structure
│   │   ├── quiz_page.py       # Quiz Mode with proctoring
│   │   ├── admin.py           # Admin dashboard
│   │   └── student.py         # Student dashboard
│   ├── components/            # Reusable UI components
│   │   ├── header.py          # Header with Quiz Mode button
│   │   ├── floating_buttons.py # FAB for Voice/Quiz/Image
│   │   └── input_modes.py     # Input mode selection
│   ├── assets/                # Static assets
│   │   └── styles.css         # Shared CSS styles
│   └── requirements.txt       # Frontend dependencies
├── backend/
│   ├── api.py                 # Flask API server
│   ├── qa_engine.py           # Core QA engine with AI integration
│   ├── document_processor.py  # Document processing with OCR
│   ├── embedding_manager.py   # Text embedding and similarity search
│   ├── vector_database.py     # Vector database for document storage
│   ├── config.py              # Configuration settings
│   ├── services/              # Business logic services
│   ├── models/                # Data models
│   ├── utils/                 # Utility functions
│   └── requirements.txt       # Backend dependencies
├── Archive/                   # Archived duplicate/non-working files
├── requirements.txt           # Main dependencies
└── README.md                  # This file
```

## 🚀 Quick Start

### One-Command Setup (Recommended)

**Windows:**
```bash
start_complete.bat
```

**Linux/Mac:**
```bash
chmod +x start_complete.sh
./start_complete.sh
```

This will automatically:
- Set up backend (FastAPI) with virtual environment
- Set up frontend (React) with dependencies
- Start both servers
- Open the application in your browser

### Manual Setup

See [GETTING_STARTED.md](GETTING_STARTED.md) for detailed instructions.

### Prerequisites
- Python 3.10+
- Node.js 18+
- Google AI API key (configured in config.env)

### Access Points
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 🔧 Configuration

### OCR Setup (Windows)
1. **Tesseract**: Download from [UB-Mannheim](https://github.com/UB-Mannheim/tesseract/wiki)
2. **Poppler**: Download from [oschwartz10612](https://github.com/oschwartz10612/poppler-windows/releases/)
3. Add both to your system PATH

### API Key Setup
Get your Google AI API key from [Google AI Studio](https://aistudio.google.com/app/apikey)

## 📖 Usage

### Document Upload
1. Use the sidebar to upload PDF, TXT, DOCX, or image files
2. Maximum file size: 200MB
3. Images and scanned PDFs will be processed with OCR

### Asking Questions
1. Choose input method: Manual, Voice, or Image
2. Type, speak, or upload your question
3. Get answers with page number citations
4. See AI fallback warnings when answers aren't found in documents

### Quiz Mode
1. Click "🧩 Quiz Mode" button
2. Grant camera and microphone permissions
3. Start exam for proctored testing
4. System monitors for suspicious activity

### Admin/Student Dashboards
1. Select role in sidebar
2. Navigate to respective dashboard
3. Manage users, exams, or view results

## 🛠️ Technical Details

### Dependencies
- **Streamlit**: Web interface framework
- **Google Generative AI**: AI model for answer generation
- **Sentence Transformers**: Text embedding generation
- **PyPDF2**: PDF text extraction
- **python-docx**: DOCX text extraction
- **Pillow**: Image processing
- **pytesseract**: OCR text extraction
- **pdf2image**: PDF to image conversion
- **OpenCV**: Computer vision processing

### Key Components
- **DocumentProcessor**: Handles file parsing and OCR
- **EmbeddingManager**: Manages text embeddings and similarity search
- **VectorDatabase**: Stores and retrieves document embeddings with page numbers
- **QAEngine**: Orchestrates question-answering with AI fallback
- **Streamlit App**: Provides the user interface with role-based dashboards

## 🔒 Privacy & Security

- All processing happens locally on your machine
- Documents are stored locally in the `vector_db` directory
- Only the Google AI API is called for answer generation
- No document content is sent to external services except for answer generation
- Camera/microphone access is only used during Quiz Mode

## 🐛 Troubleshooting

### Common Issues
1. **API Key Error**: Set your Google AI API key correctly
2. **Import Errors**: Install all dependencies with `pip install -r requirements.txt`
3. **OCR Issues**: Ensure Tesseract and Poppler are installed and in PATH
4. **File Upload Issues**: Check file size limits and supported formats
5. **Memory Issues**: Large documents may require more RAM

### Getting Help
- Check the console output for detailed error messages
- Ensure all dependencies are installed correctly
- Verify OCR tools are properly configured

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📞 Support

For support, please open an issue in the repository or contact the development team.
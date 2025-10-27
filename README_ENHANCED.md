# 🤖 Enhanced Smart Document QA Agent

A powerful AI-powered question-answering system with support for **images**, **voice chat**, **Google Drive integration**, and **mobile devices**. Built with Streamlit, Google Generative AI, and advanced NLP techniques.

## ✨ Enhanced Features

### 🖼️ Image Processing
- **OCR Support**: Extract text from images using Tesseract and EasyOCR
- **Multiple Formats**: JPG, PNG, GIF, BMP, TIFF, WebP
- **Image Preprocessing**: Automatic enhancement for better OCR results
- **Multi-language OCR**: Support for 10+ languages

### 🎤 Voice Chat
- **Speech-to-Text**: Convert voice questions to text
- **Text-to-Speech**: Get voice responses to your questions
- **Voice Notes**: Add voice recordings to your knowledge base
- **Multiple Audio Formats**: MP3, WAV, M4A, AAC, OGG, FLAC

### ☁️ Google Drive Integration
- **Direct Access**: Browse and import files from Google Drive
- **Folder Sync**: Synchronize entire folders locally
- **Search**: Find files across your Google Drive
- **Authentication**: Secure OAuth2 integration

### 📱 Mobile Support
- **Responsive Design**: Works perfectly on mobile devices
- **Touch-Friendly**: Optimized for touch interactions
- **Voice Recording**: Use your phone's microphone for voice notes
- **Camera Upload**: Take photos and extract text instantly

### 📄 Extended Document Support
- **Documents**: PDF, TXT, DOCX, DOC, RTF, ODT
- **Spreadsheets**: XLSX, XLS, CSV, ODS
- **Presentations**: PPTX, PPT, ODP
- **Images**: JPG, PNG, GIF, BMP, TIFF, WebP
- **Audio**: MP3, WAV, M4A, AAC, OGG, FLAC

## 🚀 Quick Start

### 1. Installation

```bash
# Clone or download the project
git clone <repository-url>
cd QA_Agent

# Run the enhanced setup
python setup_enhanced.py
```

### 2. Configuration

Edit the `.env` file with your API keys:

```env
# Google AI API Key (required)
GOOGLE_AI_API_KEY=your_api_key_here

# Google Drive API (optional)
GOOGLE_DRIVE_API_KEY=your_drive_api_key
GOOGLE_DRIVE_CLIENT_ID=your_client_id
GOOGLE_DRIVE_CLIENT_SECRET=your_client_secret
GOOGLE_DRIVE_FOLDER_ID=your_folder_id
```

### 3. Google Drive Setup (Optional)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Google Drive API
4. Create OAuth2 credentials
5. Download `credentials.json` and place in `backend/` folder

### 4. Run the Application

```bash
# Start the enhanced version
python run_enhanced.py
```

The application will open at `http://localhost:8501`

## 📖 How to Use

### Upload Documents
1. **File Upload**: Drag and drop files or use the file picker
2. **Google Drive**: Connect your Google Drive and browse files
3. **Voice Notes**: Record voice messages and add them as documents
4. **Mobile Camera**: Take photos of documents for instant OCR

### Ask Questions
1. **Text Questions**: Type your questions in the chat interface
2. **Voice Questions**: Click the microphone icon to ask questions verbally
3. **Voice Responses**: Enable voice responses to hear answers aloud
4. **Source Attribution**: See which documents were used for answers

### Manage Knowledge Base
- View all uploaded documents with metadata
- Remove documents you no longer need
- Monitor database statistics and system information
- Export conversation history

## 🏗️ Enhanced Architecture

```
Enhanced QA Agent/
├── backend/
│   ├── enhanced_api.py           # Enhanced Flask API
│   ├── enhanced_qa_engine.py     # Enhanced QA engine
│   ├── enhanced_document_processor.py # Multi-format processor
│   ├── voice_processor.py        # Voice processing
│   ├── google_drive_manager.py   # Google Drive integration
│   ├── embedding_manager.py      # Text embeddings
│   ├── vector_database.py        # Vector storage
│   └── config.py                 # Enhanced configuration
├── frontend/
│   ├── enhanced_app.py           # Enhanced Streamlit app
│   └── requirements.txt          # Frontend dependencies
├── run_enhanced.py               # Enhanced runner
├── setup_enhanced.py             # Enhanced setup
└── README_ENHANCED.md           # This file
```

## 🔧 Configuration Options

### Image Processing
```python
IMAGE_MAX_SIZE_MB = 10
IMAGE_OCR_LANGUAGES = ["eng", "spa", "fra", "deu", "ita", "por", "rus", "ara", "chi_sim", "chi_tra"]
IMAGE_PREPROCESSING = True
```

### Voice Processing
```python
VOICE_CHAT_ENABLED = True
SPEECH_RECOGNITION_TIMEOUT = 5
TEXT_TO_SPEECH_ENABLED = True
AUDIO_MAX_DURATION_SECONDS = 300
```

### Google Drive
```python
GOOGLE_DRIVE_SCOPES = [
    'https://www.googleapis.com/auth/drive.readonly',
    'https://www.googleapis.com/auth/drive.metadata.readonly'
]
```

### Mobile Support
```python
MOBILE_OPTIMIZED = True
RESPONSIVE_DESIGN = True
TOUCH_FRIENDLY = True
```

## 📱 Mobile Usage

### Voice Features
- Use your phone's microphone for voice questions
- Record voice notes while on the go
- Get voice responses for hands-free interaction

### Camera Integration
- Take photos of documents for instant text extraction
- Capture whiteboards, signs, and printed materials
- OCR works on mobile-optimized interface

### Touch Interface
- Swipe through documents
- Tap to expand sources and details
- Touch-friendly buttons and controls

## 🔒 Privacy & Security

- **Local Processing**: All OCR and speech processing happens locally
- **Secure Authentication**: Google Drive uses OAuth2
- **No Data Storage**: Documents processed in memory
- **API Security**: Secure API key management

## 🛠️ Technical Stack

### Backend
- **Flask**: Web API framework
- **Google AI**: Answer generation
- **EasyOCR/Tesseract**: Image text extraction
- **SpeechRecognition**: Voice processing
- **Google Drive API**: Cloud integration

### Frontend
- **Streamlit**: Web interface
- **Responsive CSS**: Mobile optimization
- **Web Audio API**: Voice recording
- **File API**: Drag-and-drop uploads

### Processing
- **Sentence Transformers**: Text embeddings
- **FAISS**: Vector similarity search
- **PyPDF2**: PDF processing
- **Pillow**: Image processing
- **Pydub**: Audio processing

## 🐛 Troubleshooting

### Common Issues

1. **OCR Not Working**
   - Install Tesseract: `brew install tesseract` (Mac) or `apt-get install tesseract-ocr` (Linux)
   - Check image quality and format

2. **Voice Recognition Issues**
   - Check microphone permissions
   - Ensure audio file format is supported
   - Try different speech recognition engines

3. **Google Drive Authentication**
   - Verify credentials.json file
   - Check OAuth2 configuration
   - Ensure Drive API is enabled

4. **Mobile Performance**
   - Use Chrome or Safari for best experience
   - Ensure stable internet connection
   - Clear browser cache if needed

### Getting Help

- Check console logs for detailed error messages
- Verify all dependencies are installed correctly
- Ensure API keys have necessary permissions
- Test individual components using the API endpoints

## 🚀 API Endpoints

### Documents
- `GET /api/documents` - List documents
- `POST /api/documents` - Upload document
- `DELETE /api/documents/{id}` - Remove document

### Questions
- `POST /api/ask` - Ask text question
- `POST /api/ask/voice` - Ask voice question

### Voice
- `POST /api/voice/process` - Speech-to-text
- `POST /api/voice/text-to-speech` - Text-to-speech
- `POST /api/voice/add-note` - Add voice note

### Google Drive
- `POST /api/google-drive/authenticate` - Authenticate
- `GET /api/google-drive/files` - List files
- `GET /api/google-drive/download/{id}` - Download file
- `POST /api/google-drive/sync` - Sync folder

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

---

**Enhanced QA Agent - Now with Images, Voice, Google Drive, and Mobile Support! 🤖📱🎤☁️**

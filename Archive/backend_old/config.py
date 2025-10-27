"""
Configuration settings for the Smart Document QA Agent
Enhanced with image, voice, and Google Drive support
"""
import os
from typing import Dict, Any, List

# API Configuration
GOOGLE_AI_API_KEY = os.getenv("GOOGLE_AI_API_KEY", "")
GOOGLE_DRIVE_API_KEY = os.getenv("GOOGLE_DRIVE_API_KEY", "")
GOOGLE_DRIVE_CLIENT_ID = os.getenv("GOOGLE_DRIVE_CLIENT_ID", "")
GOOGLE_DRIVE_CLIENT_SECRET = os.getenv("GOOGLE_DRIVE_CLIENT_SECRET", "")
MODEL_NAME = "gemini-pro"

# Document Processing Settings
MAX_CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
SUPPORTED_FILE_TYPES = [
    # Documents
    ".pdf", ".txt", ".docx", ".doc", ".rtf", ".odt",
    # Spreadsheets
    ".xlsx", ".xls", ".csv", ".ods",
    # Presentations
    ".pptx", ".ppt", ".odp",
    # Images
    ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp",
    # Audio
    ".mp3", ".wav", ".m4a", ".aac", ".ogg", ".flac", ".wma"
]

# Image Processing Settings
IMAGE_MAX_SIZE_MB = 10
IMAGE_OCR_LANGUAGES = ["eng", "spa", "fra", "deu", "ita", "por", "rus", "ara", "chi_sim", "chi_tra"]
IMAGE_PREPROCESSING = True
IMAGE_DPI = 300

# Audio Processing Settings
AUDIO_MAX_DURATION_SECONDS = 300  # 5 minutes
AUDIO_SAMPLE_RATE = 16000
AUDIO_CHUNK_SIZE = 1024
SUPPORTED_AUDIO_FORMATS = [".mp3", ".wav", ".m4a", ".aac", ".ogg", ".flac"]

# Google Drive Settings
GOOGLE_DRIVE_SCOPES = [
    'https://www.googleapis.com/auth/drive.readonly',
    'https://www.googleapis.com/auth/drive.metadata.readonly'
]
GOOGLE_DRIVE_FOLDER_ID = os.getenv("GOOGLE_DRIVE_FOLDER_ID", "")

# Voice Chat Settings
VOICE_CHAT_ENABLED = True
SPEECH_RECOGNITION_TIMEOUT = 5
SPEECH_RECOGNITION_PHRASE_TIMEOUT = 1
TEXT_TO_SPEECH_ENABLED = True
TEXT_TO_SPEECH_VOICE = "en-US-Standard-C"

# Vector Database Settings
VECTOR_DB_PATH = "./vector_db"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # Lightweight sentence transformer
TOP_K_RESULTS = 5

# UI Settings
PAGE_TITLE = "Smart Document QA Agent - Enhanced"
PAGE_ICON = "🤖"
LAYOUT = "wide"

# File Upload Settings
MAX_FILE_SIZE_MB = 100  # Increased for images and audio
UPLOAD_FOLDER = "./uploads"
TEMP_FOLDER = "./temp"

# Mobile Support Settings
MOBILE_OPTIMIZED = True
RESPONSIVE_DESIGN = True
TOUCH_FRIENDLY = True

# Conversation Settings
MAX_CONVERSATION_HISTORY = 10
SESSION_TIMEOUT_MINUTES = 30

# Performance Settings
MAX_CONCURRENT_UPLOADS = 3
PROCESSING_TIMEOUT_SECONDS = 300
CACHE_ENABLED = True
CACHE_TTL_SECONDS = 3600

# Security Settings
ALLOWED_ORIGINS = ["*"]  # Configure for production
CSRF_ENABLED = True
FILE_VALIDATION_ENABLED = True

# Create necessary directories
os.makedirs(VECTOR_DB_PATH, exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(TEMP_FOLDER, exist_ok=True)

# Application Configuration
APP_CONFIG = {
    "title": PAGE_TITLE,
    "icon": PAGE_ICON,
    "layout": LAYOUT,
    "initial_sidebar_state": "expanded"
}

# Feature Flags
FEATURES = {
    "image_processing": True,
    "voice_chat": True,
    "google_drive": True,
    "mobile_support": True,
    "advanced_ocr": True,
    "multi_language": True,
    "audio_processing": True
}


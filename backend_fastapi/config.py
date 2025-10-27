"""
Configuration settings for the FastAPI backend
"""
from pydantic_settings import BaseSettings
from typing import Optional
from urllib.parse import quote_plus
import os

class Settings(BaseSettings):
    # Database - MySQL configuration
    # Format: mysql+pymysql://username:password@host:port/database_name
    mysql_host: str = "localhost"
    mysql_port: int = 3306
    mysql_user: str = "root"
    mysql_password: str = ""  # Update this in .env file
    mysql_database: str = "smartqa_db"
    
    @property
    def database_url(self) -> str:
        """Build MySQL connection string with URL-encoded password"""
        encoded_password = quote_plus(self.mysql_password)
        return f"mysql+pymysql://{self.mysql_user}:{encoded_password}@{self.mysql_host}:{self.mysql_port}/{self.mysql_database}"
    
    # JWT
    secret_key: str = "your-secret-key-change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Google Gemini API (support multiple env var names)
    gemini_api_key: Optional[str] = None
    google_gemini_api_key: Optional[str] = None
    google_ai_api_key: Optional[str] = None
    
    @property
    def get_gemini_key(self) -> str:
        """Get Gemini API key from any of the supported environment variables"""
        return self.gemini_api_key or self.google_gemini_api_key or self.google_ai_api_key or ""
    
    # File upload settings
    max_file_size: int = 200 * 1024 * 1024  # 200MB
    upload_dir: str = "uploads"
    temp_dir: str = "temp"
    
    # Vector database
    vector_db_path: str = "vector_db"
    embedding_model: str = "all-MiniLM-L6-v2"
    
    # OCR settings
    tesseract_path: Optional[str] = None
    
    # Google Drive (optional)
    google_drive_api_key: Optional[str] = None
    google_drive_client_id: Optional[str] = None
    google_drive_client_secret: Optional[str] = None
    google_drive_folder_id: Optional[str] = None
    
    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()

# Create necessary directories on startup
os.makedirs(settings.upload_dir, exist_ok=True)
os.makedirs(settings.temp_dir, exist_ok=True)
os.makedirs(settings.vector_db_path, exist_ok=True)

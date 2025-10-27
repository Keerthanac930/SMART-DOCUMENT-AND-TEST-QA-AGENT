"""
Google Drive integration module for document access and synchronization
"""
import os
import io
import json
import logging
from typing import List, Dict, Any, Optional, Union
from datetime import datetime
import tempfile

# Google Drive API
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
from googleapiclient.errors import HttpError

# Configuration
from config import (
    GOOGLE_DRIVE_SCOPES, GOOGLE_DRIVE_FOLDER_ID, GOOGLE_DRIVE_CLIENT_ID,
    GOOGLE_DRIVE_CLIENT_SECRET, FEATURES, SUPPORTED_FILE_TYPES
)

logger = logging.getLogger(__name__)

class GoogleDriveManager:
    """
    Manages Google Drive integration for document access and synchronization
    """
    
    def __init__(self):
        self.service = None
        self.credentials = None
        self.token_path = 'token.json'
        self.credentials_path = 'credentials.json'
        
        if FEATURES.get('google_drive', False):
            self._initialize_service()
    
    def _initialize_service(self):
        """Initialize Google Drive service"""
        try:
            # Load existing credentials
            if os.path.exists(self.token_path):
                self.credentials = Credentials.from_authorized_user_file(
                    self.token_path, GOOGLE_DRIVE_SCOPES
                )
            
            # If no valid credentials, get new ones
            if not self.credentials or not self.credentials.valid:
                if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                    self.credentials.refresh(Request())
                elif os.path.exists(self.credentials_path):
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.credentials_path, GOOGLE_DRIVE_SCOPES
                    )
                    self.credentials = flow.run_local_server(port=0)
                elif GOOGLE_DRIVE_CLIENT_ID and GOOGLE_DRIVE_CLIENT_SECRET:
                    # Create credentials from environment variables
                    self.credentials = self._create_credentials_from_env()
                
                # Save credentials for next run
                if self.credentials:
                    with open(self.token_path, 'w') as token:
                        token.write(self.credentials.to_json())
            
            if self.credentials:
                self.service = build('drive', 'v3', credentials=self.credentials)
                logger.info("Google Drive service initialized successfully")
            else:
                logger.warning("Google Drive service initialization failed - no credentials")
                
        except Exception as e:
            logger.error(f"Error initializing Google Drive service: {e}")
            self.service = None
    
    def _create_credentials_from_env(self) -> Optional[Credentials]:
        """Create credentials from environment variables"""
        try:
            if not GOOGLE_DRIVE_CLIENT_ID or not GOOGLE_DRIVE_CLIENT_SECRET:
                return None
            
            # Create a temporary credentials file
            creds_data = {
                "installed": {
                    "client_id": GOOGLE_DRIVE_CLIENT_ID,
                    "client_secret": GOOGLE_DRIVE_CLIENT_SECRET,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                    "redirect_uris": ["http://localhost"]
                }
            }
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp_file:
                json.dump(creds_data, tmp_file)
                tmp_creds_path = tmp_file.name
            
            try:
                flow = InstalledAppFlow.from_client_secrets_file(
                    tmp_creds_path, GOOGLE_DRIVE_SCOPES
                )
                credentials = flow.run_local_server(port=0)
                return credentials
            finally:
                os.unlink(tmp_creds_path)
                
        except Exception as e:
            logger.error(f"Error creating credentials from environment: {e}")
            return None
    
    def is_authenticated(self) -> bool:
        """Check if Google Drive is authenticated"""
        return self.service is not None
    
    def authenticate(self) -> Dict[str, Any]:
        """Manually trigger authentication process"""
        try:
            if os.path.exists(self.credentials_path):
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, GOOGLE_DRIVE_SCOPES
                )
                self.credentials = flow.run_local_server(port=0)
                
                # Save credentials
                with open(self.token_path, 'w') as token:
                    token.write(self.credentials.to_json())
                
                # Reinitialize service
                self.service = build('drive', 'v3', credentials=self.credentials)
                
                return {
                    'success': True,
                    'message': 'Authentication successful'
                }
            else:
                return {
                    'success': False,
                    'error': 'Credentials file not found',
                    'message': 'Please add credentials.json file to the backend directory'
                }
                
        except Exception as e:
            logger.error(f"Authentication error: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': 'Authentication failed'
            }
    
    def list_files(self, folder_id: Optional[str] = None, 
                   file_types: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        List files from Google Drive
        
        Args:
            folder_id: Specific folder ID to list files from
            file_types: List of file extensions to filter by
            
        Returns:
            List of file information dictionaries
        """
        if not self.service:
            raise ValueError("Google Drive service not initialized")
        
        try:
            folder_id = folder_id or GOOGLE_DRIVE_FOLDER_ID
            file_types = file_types or SUPPORTED_FILE_TYPES
            
            # Build query
            if folder_id:
                query = f"'{folder_id}' in parents and trashed=false"
            else:
                query = "trashed=false"
            
            # Add file type filter if specified
            if file_types:
                type_conditions = []
                for file_type in file_types:
                    type_conditions.append(f"name contains '{file_type}'")
                query += f" and ({' or '.join(type_conditions)})"
            
            # Execute query
            results = self.service.files().list(
                q=query,
                fields="files(id,name,mimeType,size,createdTime,modifiedTime,webViewLink,parents)",
                pageSize=100,
                orderBy='modifiedTime desc'
            ).execute()
            
            files = []
            for file_info in results.get('files', []):
                # Check if file type is supported
                file_name = file_info['name']
                file_ext = os.path.splitext(file_name)[1].lower()
                
                if file_ext in file_types:
                    files.append({
                        'id': file_info['id'],
                        'name': file_name,
                        'mime_type': file_info.get('mimeType', ''),
                        'size': int(file_info.get('size', 0)),
                        'created_time': file_info.get('createdTime', ''),
                        'modified_time': file_info.get('modifiedTime', ''),
                        'web_view_link': file_info.get('webViewLink', ''),
                        'parents': file_info.get('parents', []),
                        'drive_url': f"drive://{file_info['id']}",
                        'file_extension': file_ext
                    })
            
            return files
            
        except HttpError as e:
            logger.error(f"Google Drive API error: {e}")
            raise
        except Exception as e:
            logger.error(f"Error listing Google Drive files: {e}")
            raise
    
    def download_file(self, file_id: str, output_path: Optional[str] = None) -> Union[bytes, str]:
        """
        Download a file from Google Drive
        
        Args:
            file_id: Google Drive file ID
            output_path: Optional path to save the file
            
        Returns:
            File content as bytes or file path if output_path specified
        """
        if not self.service:
            raise ValueError("Google Drive service not initialized")
        
        try:
            # Get file metadata
            file_metadata = self.service.files().get(fileId=file_id).execute()
            file_name = file_metadata['name']
            
            # Download file content
            request = self.service.files().get_media(fileId=file_id)
            file_content = io.BytesIO()
            downloader = MediaIoBaseDownload(file_content, request)
            
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                if status:
                    logger.info(f"Download progress: {int(status.progress() * 100)}%")
            
            file_content.seek(0)
            content_bytes = file_content.getvalue()
            
            # Save to file if output path specified
            if output_path:
                with open(output_path, 'wb') as f:
                    f.write(content_bytes)
                logger.info(f"File downloaded to {output_path}")
                return output_path
            else:
                logger.info(f"File downloaded in memory: {file_name}")
                return content_bytes
                
        except HttpError as e:
            logger.error(f"Google Drive API error downloading file {file_id}: {e}")
            raise
        except Exception as e:
            logger.error(f"Error downloading file {file_id}: {e}")
            raise
    
    def upload_file(self, file_path: str, folder_id: Optional[str] = None,
                   file_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Upload a file to Google Drive
        
        Args:
            file_path: Path to the file to upload
            folder_id: Optional folder ID to upload to
            file_name: Optional name for the uploaded file
            
        Returns:
            Upload result information
        """
        if not self.service:
            raise ValueError("Google Drive service not initialized")
        
        try:
            file_name = file_name or os.path.basename(file_path)
            folder_id = folder_id or GOOGLE_DRIVE_FOLDER_ID
            
            # Prepare file metadata
            file_metadata = {
                'name': file_name
            }
            
            if folder_id:
                file_metadata['parents'] = [folder_id]
            
            # Upload file
            media = MediaFileUpload(file_path, resumable=True)
            
            request = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id,name,size,webViewLink'
            )
            
            response = None
            while response is None:
                status, response = request.next_chunk()
                if status:
                    logger.info(f"Upload progress: {int(status.progress() * 100)}%")
            
            return {
                'success': True,
                'file_id': response.get('id'),
                'file_name': response.get('name'),
                'file_size': response.get('size'),
                'web_view_link': response.get('webViewLink'),
                'message': f"File '{file_name}' uploaded successfully"
            }
            
        except HttpError as e:
            logger.error(f"Google Drive API error uploading file {file_path}: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': f"Failed to upload file '{file_name}'"
            }
        except Exception as e:
            logger.error(f"Error uploading file {file_path}: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': f"Failed to upload file '{file_name}'"
            }
    
    def search_files(self, query: str, folder_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Search for files in Google Drive
        
        Args:
            query: Search query
            folder_id: Optional folder ID to search in
            
        Returns:
            List of matching files
        """
        if not self.service:
            raise ValueError("Google Drive service not initialized")
        
        try:
            # Build search query
            search_query = f"name contains '{query}' and trashed=false"
            
            if folder_id:
                search_query += f" and '{folder_id}' in parents"
            
            # Execute search
            results = self.service.files().list(
                q=search_query,
                fields="files(id,name,mimeType,size,createdTime,modifiedTime,webViewLink)",
                pageSize=50,
                orderBy='modifiedTime desc'
            ).execute()
            
            files = []
            for file_info in results.get('files', []):
                file_name = file_info['name']
                file_ext = os.path.splitext(file_name)[1].lower()
                
                # Only include supported file types
                if file_ext in SUPPORTED_FILE_TYPES:
                    files.append({
                        'id': file_info['id'],
                        'name': file_name,
                        'mime_type': file_info.get('mimeType', ''),
                        'size': int(file_info.get('size', 0)),
                        'created_time': file_info.get('createdTime', ''),
                        'modified_time': file_info.get('modifiedTime', ''),
                        'web_view_link': file_info.get('webViewLink', ''),
                        'drive_url': f"drive://{file_info['id']}",
                        'file_extension': file_ext
                    })
            
            return files
            
        except HttpError as e:
            logger.error(f"Google Drive API error searching files: {e}")
            raise
        except Exception as e:
            logger.error(f"Error searching Google Drive files: {e}")
            raise
    
    def create_folder(self, folder_name: str, parent_folder_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a new folder in Google Drive
        
        Args:
            folder_name: Name of the folder to create
            parent_folder_id: Optional parent folder ID
            
        Returns:
            Creation result information
        """
        if not self.service:
            raise ValueError("Google Drive service not initialized")
        
        try:
            folder_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            
            if parent_folder_id:
                folder_metadata['parents'] = [parent_folder_id]
            
            folder = self.service.files().create(
                body=folder_metadata,
                fields='id,name,webViewLink'
            ).execute()
            
            return {
                'success': True,
                'folder_id': folder.get('id'),
                'folder_name': folder.get('name'),
                'web_view_link': folder.get('webViewLink'),
                'message': f"Folder '{folder_name}' created successfully"
            }
            
        except HttpError as e:
            logger.error(f"Google Drive API error creating folder: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': f"Failed to create folder '{folder_name}'"
            }
        except Exception as e:
            logger.error(f"Error creating folder {folder_name}: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': f"Failed to create folder '{folder_name}'"
            }
    
    def get_folder_info(self, folder_id: str) -> Dict[str, Any]:
        """
        Get information about a Google Drive folder
        
        Args:
            folder_id: Google Drive folder ID
            
        Returns:
            Folder information
        """
        if not self.service:
            raise ValueError("Google Drive service not initialized")
        
        try:
            folder_info = self.service.files().get(
                fileId=folder_id,
                fields='id,name,mimeType,createdTime,modifiedTime,webViewLink,parents'
            ).execute()
            
            return {
                'id': folder_info['id'],
                'name': folder_info['name'],
                'mime_type': folder_info.get('mimeType', ''),
                'created_time': folder_info.get('createdTime', ''),
                'modified_time': folder_info.get('modifiedTime', ''),
                'web_view_link': folder_info.get('webViewLink', ''),
                'parents': folder_info.get('parents', [])
            }
            
        except HttpError as e:
            logger.error(f"Google Drive API error getting folder info: {e}")
            raise
        except Exception as e:
            logger.error(f"Error getting folder info for {folder_id}: {e}")
            raise
    
    def sync_folder(self, folder_id: str, local_path: str) -> Dict[str, Any]:
        """
        Sync a Google Drive folder to local directory
        
        Args:
            folder_id: Google Drive folder ID
            local_path: Local directory path to sync to
            
        Returns:
            Sync result information
        """
        if not self.service:
            raise ValueError("Google Drive service not initialized")
        
        try:
            # Create local directory if it doesn't exist
            os.makedirs(local_path, exist_ok=True)
            
            # Get folder files
            files = self.list_files(folder_id=folder_id)
            
            synced_files = []
            errors = []
            
            for file_info in files:
                try:
                    # Download file
                    file_path = os.path.join(local_path, file_info['name'])
                    self.download_file(file_info['id'], file_path)
                    synced_files.append(file_info['name'])
                    
                except Exception as e:
                    error_msg = f"Failed to sync {file_info['name']}: {str(e)}"
                    logger.error(error_msg)
                    errors.append(error_msg)
            
            return {
                'success': len(errors) == 0,
                'synced_files': synced_files,
                'errors': errors,
                'total_files': len(files),
                'successful_syncs': len(synced_files),
                'failed_syncs': len(errors),
                'message': f"Sync completed: {len(synced_files)}/{len(files)} files synced"
            }
            
        except Exception as e:
            logger.error(f"Error syncing folder {folder_id}: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': f"Failed to sync folder"
            }
    
    def get_drive_info(self) -> Dict[str, Any]:
        """Get Google Drive account and quota information"""
        if not self.service:
            return {
                'authenticated': False,
                'message': 'Google Drive service not initialized'
            }
        
        try:
            # Get about information (includes quota and user info)
            about = self.service.about().get(fields='user,storageQuota').execute()
            
            user_info = about.get('user', {})
            quota_info = about.get('storageQuota', {})
            
            return {
                'authenticated': True,
                'user': {
                    'display_name': user_info.get('displayName', ''),
                    'email': user_info.get('emailAddress', ''),
                    'photo_link': user_info.get('photoLink', '')
                },
                'quota': {
                    'limit': int(quota_info.get('limit', 0)) if quota_info.get('limit') else None,
                    'usage': int(quota_info.get('usage', 0)) if quota_info.get('usage') else None,
                    'usage_in_drive': int(quota_info.get('usageInDrive', 0)) if quota_info.get('usageInDrive') else None,
                    'usage_in_drive_trash': int(quota_info.get('usageInDriveTrash', 0)) if quota_info.get('usageInDriveTrash') else None
                },
                'message': 'Google Drive information retrieved successfully'
            }
            
        except HttpError as e:
            logger.error(f"Google Drive API error getting drive info: {e}")
            return {
                'authenticated': True,
                'error': str(e),
                'message': 'Failed to retrieve drive information'
            }
        except Exception as e:
            logger.error(f"Error getting drive info: {e}")
            return {
                'authenticated': True,
                'error': str(e),
                'message': 'Failed to retrieve drive information'
            }

"""
Enhanced Backend API for Smart Document QA Agent
Supports images, voice, Google Drive, and mobile file handling
"""
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import tempfile
import io
import logging
from typing import Dict, Any
import json

# Import enhanced modules
from enhanced_qa_engine import EnhancedQAEngine
from voice_processor import VoiceProcessor
from google_drive_manager import GoogleDriveManager
from config import GOOGLE_AI_API_KEY, MAX_FILE_SIZE_MB, SUPPORTED_FILE_TYPES

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Initialize Enhanced QA Engine
qa_engine = EnhancedQAEngine(api_key=GOOGLE_AI_API_KEY)
voice_processor = VoiceProcessor()
google_drive_manager = GoogleDriveManager()

# Configure Flask
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE_MB * 1024 * 1024  # Convert MB to bytes
app.config['UPLOAD_FOLDER'] = './uploads'

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    capabilities = qa_engine.get_capabilities()
    return jsonify({
        'status': 'healthy',
        'message': 'Enhanced QA Agent Backend is running',
        'capabilities': capabilities
    })

@app.route('/api/documents', methods=['GET'])
def list_documents():
    """List all documents"""
    try:
        documents = qa_engine.list_documents()
        return jsonify({'success': True, 'documents': documents})
    except Exception as e:
        logger.error(f"Error listing documents: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/documents', methods=['POST'])
def add_document():
    """Add a document (supports multiple file types)"""
    try:
        # Check if file is provided
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        # Get file info
        file_name = file.filename
        file_ext = os.path.splitext(file_name)[1].lower()
        
        # Check if file type is supported
        if file_ext not in SUPPORTED_FILE_TYPES:
            return jsonify({
                'success': False,
                'error': f'Unsupported file type: {file_ext}',
                'supported_types': SUPPORTED_FILE_TYPES
            }), 400
        
        # Get source type from request
        source = request.form.get('source', 'upload')
        
        # Save file content
        file_content = file.read()
        file.seek(0)  # Reset file pointer
        
        # Add document to knowledge base
        result = qa_engine.add_document(
            file_path=file_name,
            file_content=file_content,
            file_name=file_name,
            source=source
        )
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error adding document: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/documents/<document_id>', methods=['DELETE'])
def remove_document(document_id):
    """Remove a document"""
    try:
        result = qa_engine.remove_document(document_id)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error removing document: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/ask', methods=['POST'])
def ask_question():
    """Ask a question"""
    try:
        data = request.get_json()
        question = data.get('question', '')
        include_voice_response = data.get('include_voice_response', False)
        
        if not question:
            return jsonify({'success': False, 'error': 'No question provided'}), 400
        
        result = qa_engine.ask_question(
            question=question,
            include_voice_response=include_voice_response
        )
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error asking question: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/ask/voice', methods=['POST'])
def ask_voice_question():
    """Ask a question using voice input"""
    try:
        # Check if audio file is provided
        if 'audio' not in request.files:
            return jsonify({'success': False, 'error': 'No audio file provided'}), 400
        
        audio_file = request.files['audio']
        if audio_file.filename == '':
            return jsonify({'success': False, 'error': 'No audio file selected'}), 400
        
        # Get audio format from filename
        audio_format = os.path.splitext(audio_file.filename)[1][1:]  # Remove the dot
        
        # Get audio data
        audio_data = audio_file.read()
        
        # Get options from request
        data = request.form.to_dict()
        include_voice_response = data.get('include_voice_response', 'false').lower() == 'true'
        
        # Process voice question
        result = qa_engine.ask_voice_question(
            audio_data=audio_data,
            audio_format=audio_format,
            include_voice_response=include_voice_response
        )
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error processing voice question: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/voice/process', methods=['POST'])
def process_voice_input():
    """Process voice input to text"""
    try:
        if 'audio' not in request.files:
            return jsonify({'success': False, 'error': 'No audio file provided'}), 400
        
        audio_file = request.files['audio']
        if audio_file.filename == '':
            return jsonify({'success': False, 'error': 'No audio file selected'}), 400
        
        # Get audio format
        audio_format = os.path.splitext(audio_file.filename)[1][1:]
        
        # Get audio data
        audio_data = audio_file.read()
        
        # Process voice input
        result = voice_processor.process_voice_input(audio_data, audio_format)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error processing voice input: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/voice/text-to-speech', methods=['POST'])
def text_to_speech():
    """Convert text to speech"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        output_format = data.get('format', 'wav')
        
        if not text:
            return jsonify({'success': False, 'error': 'No text provided'}), 400
        
        # Generate speech
        audio_data = voice_processor.text_to_speech(text, output_format)
        
        if audio_data:
            # Return audio file
            return send_file(
                io.BytesIO(audio_data),
                mimetype=f'audio/{output_format}',
                as_attachment=True,
                download_name=f'speech.{output_format}'
            )
        else:
            return jsonify({'success': False, 'error': 'Failed to generate speech'}), 500
        
    except Exception as e:
        logger.error(f"Error in text-to-speech: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/voice/add-note', methods=['POST'])
def add_voice_note():
    """Add a voice note to the knowledge base"""
    try:
        if 'audio' not in request.files:
            return jsonify({'success': False, 'error': 'No audio file provided'}), 400
        
        audio_file = request.files['audio']
        if audio_file.filename == '':
            return jsonify({'success': False, 'error': 'No audio file selected'}), 400
        
        # Get audio format
        audio_format = os.path.splitext(audio_file.filename)[1][1:]
        
        # Get audio data
        audio_data = audio_file.read()
        
        # Add voice note
        result = qa_engine.add_voice_note(audio_data, audio_format)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error adding voice note: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/google-drive/authenticate', methods=['POST'])
def authenticate_google_drive():
    """Authenticate with Google Drive"""
    try:
        result = google_drive_manager.authenticate()
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error authenticating Google Drive: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/google-drive/files', methods=['GET'])
def list_google_drive_files():
    """List files from Google Drive"""
    try:
        folder_id = request.args.get('folder_id')
        result = qa_engine.list_google_drive_files(folder_id)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error listing Google Drive files: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/google-drive/download/<file_id>', methods=['GET'])
def download_google_drive_file(file_id):
    """Download a file from Google Drive and add to knowledge base"""
    try:
        result = qa_engine.add_google_drive_document(file_id)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error downloading Google Drive file: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/google-drive/sync', methods=['POST'])
def sync_google_drive_folder():
    """Sync a Google Drive folder"""
    try:
        data = request.get_json()
        folder_id = data.get('folder_id')
        local_path = data.get('local_path', './google_drive_sync')
        
        if not folder_id:
            return jsonify({'success': False, 'error': 'Folder ID required'}), 400
        
        result = qa_engine.sync_google_drive_folder(folder_id, local_path)
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error syncing Google Drive folder: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/google-drive/search', methods=['POST'])
def search_google_drive_files():
    """Search files in Google Drive"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        folder_id = data.get('folder_id')
        
        if not query:
            return jsonify({'success': False, 'error': 'Search query required'}), 400
        
        files = google_drive_manager.search_files(query, folder_id)
        
        return jsonify({
            'success': True,
            'files': files,
            'count': len(files),
            'message': f"Found {len(files)} files matching '{query}'"
        })
        
    except Exception as e:
        logger.error(f"Error searching Google Drive files: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/google-drive/info', methods=['GET'])
def get_google_drive_info():
    """Get Google Drive account information"""
    try:
        info = google_drive_manager.get_drive_info()
        return jsonify(info)
    except Exception as e:
        logger.error(f"Error getting Google Drive info: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get database statistics"""
    try:
        stats = qa_engine.get_database_stats()
        return jsonify({'success': True, 'stats': stats})
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/capabilities', methods=['GET'])
def get_capabilities():
    """Get system capabilities"""
    try:
        capabilities = qa_engine.get_capabilities()
        return jsonify({'success': True, 'capabilities': capabilities})
    except Exception as e:
        logger.error(f"Error getting capabilities: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/search', methods=['POST'])
def search_documents():
    """Search for relevant document chunks"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        top_k = data.get('top_k', 5)
        
        if not query:
            return jsonify({'success': False, 'error': 'Search query required'}), 400
        
        results = qa_engine.search_documents(query, top_k)
        
        return jsonify({
            'success': True,
            'results': results,
            'count': len(results),
            'query': query
        })
        
    except Exception as e:
        logger.error(f"Error searching documents: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/conversation/history', methods=['GET'])
def get_conversation_history():
    """Get conversation history"""
    try:
        history = qa_engine.get_conversation_history()
        return jsonify({'success': True, 'history': history})
    except Exception as e:
        logger.error(f"Error getting conversation history: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/conversation/clear', methods=['POST'])
def clear_conversation_history():
    """Clear conversation history"""
    try:
        qa_engine.clear_conversation_history()
        return jsonify({'success': True, 'message': 'Conversation history cleared'})
    except Exception as e:
        logger.error(f"Error clearing conversation history: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/conversation/export', methods=['GET'])
def export_conversation_history():
    """Export conversation history"""
    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp_file:
            tmp_file_path = tmp_file.name
        
        # Export history
        qa_engine.export_conversation_history(tmp_file_path)
        
        # Return file
        return send_file(
            tmp_file_path,
            as_attachment=True,
            download_name='conversation_history.json',
            mimetype='application/json'
        )
        
    except Exception as e:
        logger.error(f"Error exporting conversation history: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/system/info', methods=['GET'])
def get_system_info():
    """Get system information"""
    try:
        info = qa_engine.get_system_info()
        return jsonify({'success': True, 'info': info})
    except Exception as e:
        logger.error(f"Error getting system info: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/voice/test-microphone', methods=['GET'])
def test_microphone():
    """Test microphone availability"""
    try:
        result = voice_processor.test_microphone()
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error testing microphone: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/voice/voices', methods=['GET'])
def get_available_voices():
    """Get available text-to-speech voices"""
    try:
        voices = voice_processor.get_available_voices()
        return jsonify({'success': True, 'voices': voices})
    except Exception as e:
        logger.error(f"Error getting available voices: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/voice/settings', methods=['POST'])
def update_voice_settings():
    """Update voice settings"""
    try:
        data = request.get_json()
        voice_id = data.get('voice_id')
        rate = data.get('rate')
        volume = data.get('volume')
        
        results = {}
        
        if voice_id is not None:
            results['voice'] = voice_processor.set_voice(voice_id)
        
        if rate is not None:
            results['rate'] = voice_processor.set_speech_rate(rate)
        
        if volume is not None:
            results['volume'] = voice_processor.set_volume(volume)
        
        return jsonify({'success': True, 'results': results})
        
    except Exception as e:
        logger.error(f"Error updating voice settings: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# Error handlers
@app.errorhandler(413)
def too_large(e):
    return jsonify({
        'success': False,
        'error': 'File too large',
        'message': f'File size exceeds maximum limit of {MAX_FILE_SIZE_MB}MB'
    }), 413

@app.errorhandler(400)
def bad_request(e):
    return jsonify({
        'success': False,
        'error': 'Bad request',
        'message': 'Invalid request data'
    }), 400

@app.errorhandler(500)
def internal_error(e):
    return jsonify({
        'success': False,
        'error': 'Internal server error',
        'message': 'An unexpected error occurred'
    }), 500

if __name__ == '__main__':
    logger.info("Starting Enhanced QA Agent Backend API...")
    logger.info(f"Supported file types: {SUPPORTED_FILE_TYPES}")
    logger.info(f"Max file size: {MAX_FILE_SIZE_MB}MB")
    logger.info(f"Google AI enabled: {qa_engine.genai_client is not None}")
    logger.info(f"Google Drive enabled: {google_drive_manager.is_authenticated()}")
    logger.info("🌐 Server will be available at: http://localhost:5000")
    logger.info("📖 Health check: http://localhost:5000/api/health")
    
    try:
        app.run(debug=False, host='0.0.0.0', port=5000, threaded=True)
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        print(f"❌ Failed to start server: {e}")
        sys.exit(1)

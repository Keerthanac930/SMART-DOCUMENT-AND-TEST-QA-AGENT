#!/usr/bin/env python3
"""
Backend API for Smart Document QA Agent
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import tempfile
from qa_engine import QAEngine
from config import GOOGLE_AI_API_KEY

app = Flask(__name__)
CORS(app)

# Initialize QA Engine
qa_engine = QAEngine(api_key=GOOGLE_AI_API_KEY)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'QA Agent Backend is running'})

@app.route('/api/documents', methods=['GET'])
def list_documents():
    """List all documents"""
    try:
        documents = qa_engine.list_documents()
        return jsonify({'success': True, 'documents': documents})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

MAX_FILE_BYTES = 200 * 1024 * 1024  # 200 MB limit

@app.route('/api/documents', methods=['POST'])
def add_document():
    """Add a document"""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        file.seek(0, os.SEEK_END)
        size = file.tell()
        file.seek(0)
        if size > MAX_FILE_BYTES:
            return jsonify({'success': False, 'error': 'File exceeds 200MB limit'}), 413
        
        # Save temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp_file:
            file.save(tmp_file.name)
            result = qa_engine.add_document(tmp_file.name)
            os.unlink(tmp_file.name)
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/documents/<document_id>', methods=['DELETE'])
def remove_document(document_id):
    """Remove a document"""
    try:
        result = qa_engine.remove_document(document_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/ask', methods=['POST'])
def ask_question():
    """Ask a question"""
    try:
        data = request.get_json()
        question = data.get('question', '')
        
        if not question:
            return jsonify({'success': False, 'error': 'No question provided'}), 400
        
        result = qa_engine.ask_question(question)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get database statistics"""
    try:
        stats = qa_engine.get_database_stats()
        return jsonify({'success': True, 'stats': stats})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

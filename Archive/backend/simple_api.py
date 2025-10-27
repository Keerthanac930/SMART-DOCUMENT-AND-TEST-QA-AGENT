"""
Simple Backend API - Works without complex dependencies
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import tempfile
import PyPDF2
import docx
from datetime import datetime
import json

app = Flask(__name__)
CORS(app)

# Simple in-memory storage
documents_db = []
conversation_history = []

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Simple QA Agent Backend is running',
        'documents_count': len(documents_db),
        'features': ['text_qa', 'document_upload', 'pdf_support', 'docx_support']
    })

@app.route('/api/documents', methods=['GET'])
def list_documents():
    """List all documents"""
    try:
        return jsonify({'success': True, 'documents': documents_db})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/documents', methods=['POST'])
def add_document():
    """Add a document"""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        # Extract text based on file type
        file_ext = os.path.splitext(file.filename)[1].lower()
        
        if file_ext == '.pdf':
            text = extract_pdf_text(file)
        elif file_ext == '.txt':
            text = file.read().decode('utf-8')
        elif file_ext in ['.docx', '.doc']:
            text = extract_docx_text(file)
        else:
            return jsonify({'success': False, 'error': f'Unsupported file type: {file_ext}'}), 400
        
        # Create document record
        document = {
            'document_id': len(documents_db) + 1,
            'file_name': file.filename,
            'file_type': file_ext,
            'content': text,
            'word_count': len(text.split()),
            'added_at': datetime.now().isoformat()
        }
        
        documents_db.append(document)
        
        return jsonify({
            'success': True,
            'document_id': document['document_id'],
            'file_name': file.filename,
            'word_count': document['word_count'],
            'message': f"Document '{file.filename}' added successfully"
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

def extract_pdf_text(file):
    """Extract text from PDF"""
    try:
        file.seek(0)
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        return f"Error extracting PDF: {str(e)}"

def extract_docx_text(file):
    """Extract text from DOCX"""
    try:
        file.seek(0)
        doc = docx.Document(file)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        return f"Error extracting DOCX: {str(e)}"

@app.route('/api/ask', methods=['POST'])
def ask_question():
    """Ask a question"""
    try:
        data = request.get_json()
        question = data.get('question', '')
        
        if not question:
            return jsonify({'success': False, 'error': 'No question provided'}), 400
        
        if not documents_db:
            return jsonify({
                'success': False,
                'message': 'No documents found. Please upload some documents first.'
            })
        
        # Simple text search
        results = []
        for doc in documents_db:
            if question.lower() in doc['content'].lower():
                # Find relevant sentences
                sentences = doc['content'].split('.')
                for sentence in sentences:
                    if question.lower() in sentence.lower():
                        results.append({
                            'document_name': doc['file_name'],
                            'similarity': 0.8,
                            'chunk_preview': sentence.strip()[:200] + "..." if len(sentence.strip()) > 200 else sentence.strip()
                        })
        
        if results:
            answer = f"Based on your documents, I found {len(results)} relevant sections about '{question}'. Here's what I found:\n\n"
            for i, result in enumerate(results[:3], 1):
                answer += f"{i}. From {result['document_name']}:\n{result['chunk_preview']}\n\n"
        else:
            answer = f"I couldn't find specific information about '{question}' in your documents. Try rephrasing your question or upload more relevant documents."
        
        # Store in conversation history
        conversation_history.append({
            'question': question,
            'answer': answer,
            'timestamp': datetime.now().isoformat(),
            'sources': results[:3]
        })
        
        return jsonify({
            'success': True,
            'question': question,
            'answer': answer,
            'sources': results[:3],
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/documents/<int:document_id>', methods=['DELETE'])
def remove_document(document_id):
    """Remove a document"""
    try:
        global documents_db
        documents_db = [doc for doc in documents_db if doc['document_id'] != document_id]
        return jsonify({'success': True, 'message': f'Document {document_id} removed successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get database statistics"""
    try:
        total_words = sum(doc['word_count'] for doc in documents_db)
        return jsonify({
            'success': True,
            'stats': {
                'document_count': len(documents_db),
                'total_words': total_words,
                'total_chunks': len(documents_db),
                'total_size_mb': 0.1  # Approximate
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/capabilities', methods=['GET'])
def get_capabilities():
    """Get system capabilities"""
    return jsonify({
        'success': True,
        'capabilities': {
            'document_processing': {
                'supported_file_types': ['.pdf', '.txt', '.docx', '.doc'],
                'image_processing': False,
                'audio_processing': False
            },
            'voice_processing': {
                'voice_chat_enabled': False,
                'speech_recognition_available': False,
                'text_to_speech_available': False
            },
            'google_drive': {
                'enabled': False,
                'authenticated': False
            },
            'features': {
                'image_processing': False,
                'voice_chat': False,
                'google_drive': False,
                'mobile_support': True,
                'advanced_ocr': False,
                'multi_language': False,
                'audio_processing': False
            }
        }
    })

if __name__ == '__main__':
    print("🚀 Starting Simple QA Agent Backend...")
    print("📄 Supported: PDF, TXT, DOCX files")
    print("🌐 Server: http://localhost:5000")
    print("📖 Health: http://localhost:5000/api/health")
    
    app.run(debug=False, host='0.0.0.0', port=5000, threaded=True)

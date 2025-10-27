"""
Enhanced Question Answering Engine with image, voice, and Google Drive support
"""
import os
import io
import tempfile
import logging
from typing import List, Dict, Any, Optional, Union
from datetime import datetime
import json

# Import Google AI
import google.generativeai as genai

# Import our enhanced modules
from enhanced_document_processor import EnhancedDocumentProcessor
from voice_processor import VoiceProcessor
from google_drive_manager import GoogleDriveManager
from embedding_manager import EmbeddingManager
from vector_database import VectorDatabase

# Import configuration
from config import (
    TOP_K_RESULTS, GOOGLE_AI_API_KEY, MODEL_NAME, FEATURES,
    SUPPORTED_FILE_TYPES, MAX_FILE_SIZE_MB
)

logger = logging.getLogger(__name__)

class EnhancedQAEngine:
    """
    Enhanced QA Engine with support for images, voice, and Google Drive
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Enhanced QA Engine
        
        Args:
            api_key (str, optional): Google AI API key
        """
        # Initialize components
        self.document_processor = EnhancedDocumentProcessor()
        self.voice_processor = VoiceProcessor()
        self.google_drive_manager = GoogleDriveManager()
        self.embedding_manager = EmbeddingManager()
        self.vector_db = VectorDatabase()
        
        # Initialize Google AI
        self.api_key = api_key or GOOGLE_AI_API_KEY
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.genai_client = genai
            logger.info("Enhanced QA Engine initialized with Google AI")
        else:
            self.genai_client = None
            logger.warning("Enhanced QA Engine initialized without API key - limited functionality")
        
        # Conversation history
        self.conversation_history = []
    
    def add_document(self, file_path: str, file_content: Optional[bytes] = None,
                    file_name: Optional[str] = None, source: str = 'file') -> Dict[str, Any]:
        """
        Add a document to the knowledge base
        
        Args:
            file_path (str): Path to the document file or drive:// URL
            file_content (bytes, optional): File content if processing from memory
            file_name (str, optional): File name if different from path
            source (str): Source type ('file', 'drive', 'upload', 'mobile')
            
        Returns:
            Dict[str, Any]: Processing result
        """
        try:
            # Process document
            logger.info(f"Processing document: {file_path}")
            document_data = self.document_processor.process_document(
                file_path, file_content, file_name
            )
            
            # Add source information
            document_data['source'] = source
            document_data['added_at'] = datetime.now().isoformat()
            
            # Chunk the document
            chunks = self.document_processor.chunk_text(document_data['content'])
            
            if not chunks:
                raise ValueError("No text chunks could be extracted from the document")
            
            # Generate embeddings for chunks
            chunk_texts = [chunk['text'] for chunk in chunks]
            embeddings = self.embedding_manager.generate_embeddings(chunk_texts)
            
            # Add to vector database
            document_id = self.vector_db.add_document(document_data, chunks, embeddings)
            
            # Generate summary
            summary = self.document_processor.get_document_summary(document_data)
            
            result = {
                'success': True,
                'document_id': document_id,
                'file_name': document_data['file_name'],
                'file_type': document_data['file_type'],
                'source': source,
                'chunk_count': len(chunks),
                'word_count': document_data['word_count'],
                'summary': summary,
                'message': f"Document '{document_data['file_name']}' added successfully"
            }
            
            logger.info(f"Document added successfully: {document_data['file_name']}")
            return result
            
        except Exception as e:
            logger.error(f"Error adding document {file_path}: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'message': f"Failed to add document: {str(e)}"
            }
    
    def add_google_drive_document(self, file_id: str) -> Dict[str, Any]:
        """
        Add a document from Google Drive
        
        Args:
            file_id (str): Google Drive file ID
            
        Returns:
            Dict[str, Any]: Processing result
        """
        try:
            drive_url = f"drive://{file_id}"
            return self.add_document(drive_url, source='drive')
            
        except Exception as e:
            logger.error(f"Error adding Google Drive document {file_id}: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'message': f"Failed to add Google Drive document: {str(e)}"
            }
    
    def add_voice_note(self, audio_data: bytes, audio_format: str = 'wav') -> Dict[str, Any]:
        """
        Add a voice note by converting speech to text
        
        Args:
            audio_data (bytes): Audio data
            audio_format (str): Audio format
            
        Returns:
            Dict[str, Any]: Processing result
        """
        try:
            # Convert speech to text
            voice_result = self.voice_processor.process_voice_input(audio_data, audio_format)
            
            if not voice_result['success']:
                return {
                    'success': False,
                    'error': voice_result['error'],
                    'message': f"Failed to process voice input: {voice_result['error']}"
                }
            
            text_content = voice_result['text']
            if not text_content.strip():
                return {
                    'success': False,
                    'error': 'No speech detected',
                    'message': 'No speech could be detected in the audio'
                }
            
            # Create a temporary text file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f"voice_note_{timestamp}.txt"
            
            # Save audio as temporary file for processing
            with tempfile.NamedTemporaryFile(suffix=f'.{audio_format}', delete=False) as tmp_audio:
                tmp_audio.write(audio_data)
                tmp_audio_path = tmp_audio.name
            
            try:
                # Process as document
                result = self.add_document(
                    file_path=tmp_audio_path,
                    file_content=text_content.encode('utf-8'),
                    file_name=file_name,
                    source='voice'
                )
                
                # Add voice-specific metadata
                if result['success']:
                    result['voice_confidence'] = voice_result['confidence']
                    result['voice_engine'] = voice_result['engine']
                    result['transcribed_text'] = text_content
                
                return result
                
            finally:
                # Clean up temporary file
                if os.path.exists(tmp_audio_path):
                    os.unlink(tmp_audio_path)
                    
        except Exception as e:
            logger.error(f"Error adding voice note: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'message': f"Failed to add voice note: {str(e)}"
            }
    
    def ask_question(self, question: str, context_documents: Optional[List[str]] = None,
                    use_conversation_history: bool = True, 
                    include_voice_response: bool = False) -> Dict[str, Any]:
        """
        Ask a question and get an answer
        
        Args:
            question (str): The question to ask
            context_documents (List[str], optional): Specific document IDs to search in
            use_conversation_history (bool): Whether to include conversation history
            include_voice_response (bool): Whether to include voice response
            
        Returns:
            Dict[str, Any]: Answer and relevant information
        """
        try:
            # Check if we have documents
            documents = self.vector_db.list_documents()
            if not documents:
                return {
                    'success': False,
                    'message': 'No documents found. Please upload some documents first.'
                }
            
            # If no API key, return simple response
            if not self.genai_client:
                answer = f"Based on your {len(documents)} document(s), here's what I found related to: '{question}'. This is a simple text-based response. For full AI capabilities, please configure a Google AI API key."
                result = {
                    'success': True,
                    'answer': answer,
                    'sources': []
                }
            else:
                # Use the full AI-powered method
                result = self._ask_question_with_ai(
                    question, context_documents, use_conversation_history
                )
            
            # Add voice response if requested
            if include_voice_response and result['success']:
                voice_response = self.voice_processor.text_to_speech(result['answer'])
                if voice_response:
                    result['voice_response'] = voice_response
                    result['voice_available'] = True
                else:
                    result['voice_available'] = False
            
            return result
            
        except Exception as e:
            logger.error(f"Error asking question: {str(e)}")
            return {
                'success': False,
                'message': f'Error processing question: {str(e)}'
            }
    
    def ask_voice_question(self, audio_data: bytes, audio_format: str = 'wav',
                          include_voice_response: bool = True) -> Dict[str, Any]:
        """
        Ask a question using voice input
        
        Args:
            audio_data (bytes): Audio data containing the question
            audio_format (str): Audio format
            include_voice_response (bool): Whether to include voice response
            
        Returns:
            Dict[str, Any]: Answer and relevant information
        """
        try:
            # Convert speech to text
            voice_result = self.voice_processor.process_voice_input(audio_data, audio_format)
            
            if not voice_result['success']:
                return {
                    'success': False,
                    'error': voice_result['error'],
                    'message': f"Failed to process voice question: {voice_result['error']}"
                }
            
            question = voice_result['text']
            if not question.strip():
                return {
                    'success': False,
                    'error': 'No speech detected',
                    'message': 'No speech could be detected in the audio'
                }
            
            # Ask the question
            result = self.ask_question(question, include_voice_response=include_voice_response)
            
            # Add voice-specific metadata
            if result['success']:
                result['voice_question'] = question
                result['voice_confidence'] = voice_result['confidence']
                result['voice_engine'] = voice_result['engine']
            
            return result
            
        except Exception as e:
            logger.error(f"Error processing voice question: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'message': f"Failed to process voice question: {str(e)}"
            }
    
    def _ask_question_with_ai(self, question: str, context_documents: Optional[List[str]] = None,
                             use_conversation_history: bool = True) -> Dict[str, Any]:
        """Ask question using AI with full context"""
        try:
            # Generate embedding for the question
            question_embedding = self.embedding_manager.generate_single_embedding(question)
            
            # Search for relevant chunks
            search_results = []
            for doc_id in (context_documents or [None]):
                results = self.vector_db.search_similar(
                    question_embedding,
                    top_k=TOP_K_RESULTS,
                    document_filter=doc_id
                )
                search_results.extend(results)
            
            # Sort by similarity and take top results
            search_results.sort(key=lambda x: x['similarity'], reverse=True)
            top_results = search_results[:TOP_K_RESULTS]
            
            if not top_results:
                return {
                    'success': False,
                    'error': 'No relevant information found',
                    'message': 'No relevant documents found in the knowledge base to answer this question.'
                }
            
            # Prepare context for the AI model
            context_text = self._prepare_context(top_results)
            
            # Build conversation history if enabled
            conversation_context = ""
            if use_conversation_history and self.conversation_history:
                recent_history = self.conversation_history[-3:]  # Last 3 exchanges
                conversation_context = self._format_conversation_history(recent_history)
            
            # Generate answer using Google AI
            answer = self._generate_answer(question, context_text, conversation_context)
            
            # Store in conversation history
            self.conversation_history.append({
                'question': question,
                'answer': answer,
                'timestamp': datetime.now().isoformat(),
                'sources': [result['document_name'] for result in top_results]
            })
            
            return {
                'success': True,
                'question': question,
                'answer': answer,
                'sources': [
                    {
                        'document_name': result['document_name'],
                        'similarity': result['similarity'],
                        'chunk_preview': result['chunk_text'][:200] + "..." if len(result['chunk_text']) > 200 else result['chunk_text']
                    }
                    for result in top_results
                ],
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error answering question: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'message': f"Failed to answer question: {str(e)}"
            }
    
    def _prepare_context(self, search_results: List[Dict[str, Any]]) -> str:
        """Prepare context text from search results"""
        context_parts = []
        
        for i, result in enumerate(search_results, 1):
            context_parts.append(f"Source {i} (from {result['document_name']}):")
            context_parts.append(result['chunk_text'])
            context_parts.append("")  # Empty line between sources
        
        return "\n".join(context_parts)
    
    def _format_conversation_history(self, history: List[Dict[str, Any]]) -> str:
        """Format conversation history for context"""
        if not history:
            return ""
        
        formatted_parts = ["Previous conversation:"]
        
        for entry in history:
            formatted_parts.append(f"Q: {entry['question']}")
            formatted_parts.append(f"A: {entry['answer'][:200]}...")
            formatted_parts.append("")
        
        return "\n".join(formatted_parts)
    
    def _generate_answer(self, question: str, context: str, conversation_context: str = "") -> str:
        """Generate answer using Google AI"""
        # Build the prompt
        prompt_parts = [
            "You are a helpful AI assistant that answers questions based on provided documents.",
            "You can process text from various sources including documents, images (OCR), audio (speech-to-text), and Google Drive files.",
            "Use only the information from the provided context to answer the question.",
            "If the context doesn't contain enough information to answer the question, say so clearly.",
            "Provide specific references to the source documents when possible.",
            "Be concise but comprehensive in your answers.",
            "",
            "Context from documents:",
            context,
            ""
        ]
        
        if conversation_context:
            prompt_parts.extend([
                conversation_context,
                ""
            ])
        
        prompt_parts.extend([
            f"Question: {question}",
            "",
            "Answer:"
        ])
        
        prompt = "\n".join(prompt_parts)
        
        try:
            model = self.genai_client.GenerativeModel(MODEL_NAME)
            response = model.generate_content(prompt)
            
            return response.text.strip()
            
        except Exception as e:
            logger.error(f"Error generating answer: {str(e)}")
            raise
    
    def list_google_drive_files(self, folder_id: Optional[str] = None) -> Dict[str, Any]:
        """List files from Google Drive"""
        try:
            if not self.google_drive_manager.is_authenticated():
                return {
                    'success': False,
                    'error': 'Google Drive not authenticated',
                    'message': 'Please authenticate with Google Drive first'
                }
            
            files = self.google_drive_manager.list_files(folder_id)
            
            return {
                'success': True,
                'files': files,
                'count': len(files),
                'message': f"Found {len(files)} files in Google Drive"
            }
            
        except Exception as e:
            logger.error(f"Error listing Google Drive files: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'message': f"Failed to list Google Drive files: {str(e)}"
            }
    
    def sync_google_drive_folder(self, folder_id: str, local_path: str) -> Dict[str, Any]:
        """Sync a Google Drive folder to local directory"""
        try:
            if not self.google_drive_manager.is_authenticated():
                return {
                    'success': False,
                    'error': 'Google Drive not authenticated',
                    'message': 'Please authenticate with Google Drive first'
                }
            
            sync_result = self.google_drive_manager.sync_folder(folder_id, local_path)
            
            # Add synced files to knowledge base
            if sync_result['success']:
                added_documents = []
                for file_name in sync_result['synced_files']:
                    file_path = os.path.join(local_path, file_name)
                    if os.path.splitext(file_name)[1].lower() in SUPPORTED_FILE_TYPES:
                        result = self.add_document(file_path, source='drive_sync')
                        if result['success']:
                            added_documents.append(file_name)
                
                sync_result['added_to_knowledge_base'] = added_documents
            
            return sync_result
            
        except Exception as e:
            logger.error(f"Error syncing Google Drive folder: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'message': f"Failed to sync Google Drive folder: {str(e)}"
            }
    
    def get_capabilities(self) -> Dict[str, Any]:
        """Get information about system capabilities"""
        return {
            'document_processing': self.document_processor.get_processing_capabilities(),
            'voice_processing': self.voice_processor.get_voice_capabilities(),
            'google_drive': {
                'enabled': FEATURES.get('google_drive', False),
                'authenticated': self.google_drive_manager.is_authenticated(),
                'drive_info': self.google_drive_manager.get_drive_info() if self.google_drive_manager.is_authenticated() else None
            },
            'ai_capabilities': {
                'google_ai_enabled': self.genai_client is not None,
                'model_name': MODEL_NAME if self.genai_client else None
            },
            'supported_file_types': SUPPORTED_FILE_TYPES,
            'max_file_size_mb': MAX_FILE_SIZE_MB,
            'features': FEATURES
        }
    
    # Inherit other methods from original QA engine
    def remove_document(self, document_id: str) -> Dict[str, Any]:
        """Remove a document from the knowledge base"""
        try:
            success = self.vector_db.remove_document(document_id)
            
            if success:
                return {
                    'success': True,
                    'message': f"Document {document_id} removed successfully"
                }
            else:
                return {
                    'success': False,
                    'error': "Document not found",
                    'message': f"Document {document_id} not found"
                }
                
        except Exception as e:
            logger.error(f"Error removing document {document_id}: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'message': f"Failed to remove document: {str(e)}"
            }
    
    def list_documents(self) -> List[Dict[str, Any]]:
        """List all documents in the knowledge base"""
        return self.vector_db.list_documents()
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        return self.vector_db.get_database_stats()
    
    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """Get conversation history"""
        return self.conversation_history.copy()
    
    def clear_conversation_history(self):
        """Clear conversation history"""
        self.conversation_history.clear()
        logger.info("Conversation history cleared")
    
    def search_documents(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Search for relevant document chunks"""
        try:
            # Generate embedding for query
            query_embedding = self.embedding_manager.generate_single_embedding(query)
            
            # Search in vector database
            results = self.vector_db.search_similar(query_embedding, top_k=top_k)
            
            return results
            
        except Exception as e:
            logger.error(f"Error searching documents: {str(e)}")
            return []
    
    def export_conversation_history(self, file_path: str):
        """Export conversation history to file"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.conversation_history, f, indent=2, ensure_ascii=False)
            logger.info(f"Conversation history exported to {file_path}")
        except Exception as e:
            logger.error(f"Error exporting conversation history: {str(e)}")
            raise
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get system information"""
        embedding_info = self.embedding_manager.get_model_info()
        db_stats = self.vector_db.get_database_stats()
        
        return {
            'qa_engine': {
                'model_name': MODEL_NAME,
                'conversation_history_length': len(self.conversation_history),
                'enhanced_features': True
            },
            'embedding_model': embedding_info,
            'database': db_stats,
            'capabilities': self.get_capabilities()
        }

"""
Question Answering Engine with semantic search capabilities
"""
import os
from typing import List, Dict, Any, Optional, Tuple
import logging
from datetime import datetime
import json

# Import Google AI
import google.generativeai as genai
from document_processor import DocumentProcessor
from embedding_manager import EmbeddingManager
from vector_database import VectorDatabase
from config import TOP_K_RESULTS, GOOGLE_AI_API_KEY, MODEL_NAME

logger = logging.getLogger(__name__)

class QAEngine:
    """
    Main QA Engine that combines document processing, embeddings, and AI generation
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the QA Engine
        
        Args:
            api_key (str, optional): Google AI API key
        """
        # Initialize components
        self.document_processor = DocumentProcessor()
        self.embedding_manager = EmbeddingManager()
        self.vector_db = VectorDatabase()
        
        # Initialize Google AI
        self.api_key = api_key or GOOGLE_AI_API_KEY
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.genai_client = genai
            logger.info("QA Engine initialized with Google AI")
        else:
            self.genai_client = None
            logger.warning("QA Engine initialized without API key - limited functionality")
        
        # Conversation history
        self.conversation_history = []
    
    def add_document(self, file_path: str) -> Dict[str, Any]:
        """
        Add a document to the knowledge base
        
        Args:
            file_path (str): Path to the document file
            
        Returns:
            Dict[str, Any]: Processing result
        """
        try:
            # Process document
            logger.info(f"Processing document: {file_path}")
            document_data = self.document_processor.process_document(file_path)
            
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
    
    def remove_document(self, document_id: str) -> Dict[str, Any]:
        """
        Remove a document from the knowledge base
        
        Args:
            document_id (str): Document ID to remove
            
        Returns:
            Dict[str, Any]: Removal result
        """
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
    
    def ask_question(self, question: str, context_documents: Optional[List[str]] = None, 
                    use_conversation_history: bool = True) -> Dict[str, Any]:
        """
        Ask a question and get an answer
        
        Args:
            question (str): The question to ask
            context_documents (List[str], optional): Specific document IDs to search in
            use_conversation_history (bool): Whether to include conversation history
            
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
                return {
                    'success': True,
                    'answer': answer,
                    'sources': []
                }
            
            # Use the full AI-powered method
            return self.ask_question_original(question, context_documents, use_conversation_history)
            
        except Exception as e:
            logger.error(f"Error asking question: {str(e)}")
            return {
                'success': False,
                'message': f'Error processing question: {str(e)}'
            }
    
    def ask_question_original(self, question: str, context_documents: Optional[List[str]] = None, 
                    use_conversation_history: bool = True) -> Dict[str, Any]:
        """
        Original ask_question method (disabled for now)
        """
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
                # Generate AI fallback with explicit warning
                fallback_answer = self._generate_answer(
                    question,
                    context="",
                    conversation_context=self._format_conversation_history(self.conversation_history[-3:]) if use_conversation_history else ""
                ) if self.genai_client else ""
                return {
                    'success': True,
                    'question': question,
                    'answer': ("⚠️ The answer was not found in the document. This response is AI-generated.\n\n" + fallback_answer.strip()) if fallback_answer else "⚠️ The answer was not found in the document. AI generation unavailable without API key.",
                    'sources': [],
                    'timestamp': datetime.now().isoformat()
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
                        'chunk_preview': result['chunk_text'][:200] + "..." if len(result['chunk_text']) > 200 else result['chunk_text'],
                        'page_number': result.get('page_number')
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
        """
        Prepare context text from search results
        
        Args:
            search_results (List[Dict[str, Any]]): Search results from vector database
            
        Returns:
            str: Formatted context text
        """
        context_parts = []
        
        for i, result in enumerate(search_results, 1):
            context_parts.append(f"Source {i} (from {result['document_name']}):")
            context_parts.append(result['chunk_text'])
            context_parts.append("")  # Empty line between sources
        
        return "\n".join(context_parts)
    
    def _format_conversation_history(self, history: List[Dict[str, Any]]) -> str:
        """
        Format conversation history for context
        
        Args:
            history (List[Dict[str, Any]]): Conversation history
            
        Returns:
            str: Formatted conversation history
        """
        if not history:
            return ""
        
        formatted_parts = ["Previous conversation:"]
        
        for entry in history:
            formatted_parts.append(f"Q: {entry['question']}")
            formatted_parts.append(f"A: {entry['answer'][:200]}...")
            formatted_parts.append("")
        
        return "\n".join(formatted_parts)
    
    def _generate_answer(self, question: str, context: str, conversation_context: str = "") -> str:
        """
        Generate answer using Google AI
        
        Args:
            question (str): The question
            context (str): Relevant context from documents
            conversation_context (str): Previous conversation context
            
        Returns:
            str: Generated answer
        """
        # Build the prompt according to requirements
        prompt_parts = [
            "You are an intelligent Smart Document QA Agent.",
            "When a user asks a question:",
            "1. Extract and read all text content (including scanned text using OCR).",
            "2. Search for the answer within the document.",
            "3. If found:",
            "   - Return the answer.",
            "   - Mention the document name and the exact page number.",
            "4. If not found:",
            "   - Generate the best possible AI-based answer using your knowledge.",
            "   - Clearly mention: '⚠️ The answer was not found in the document. This response is AI-generated.'",
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
    
    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """
        Get conversation history
        
        Returns:
            List[Dict[str, Any]]: Conversation history
        """
        return self.conversation_history.copy()
    
    def clear_conversation_history(self):
        """Clear conversation history"""
        self.conversation_history.clear()
        logger.info("Conversation history cleared")
    
    def list_documents(self) -> List[Dict[str, Any]]:
        """
        List all documents in the knowledge base
        
        Returns:
            List[Dict[str, Any]]: List of documents
        """
        return self.vector_db.list_documents()
    
    def get_database_stats(self) -> Dict[str, Any]:
        """
        Get database statistics
        
        Returns:
            Dict[str, Any]: Database statistics
        """
        return self.vector_db.get_database_stats()
    
    def search_documents(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Search for relevant document chunks
        
        Args:
            query (str): Search query
            top_k (int): Number of results to return
            
        Returns:
            List[Dict[str, Any]]: Search results
        """
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
        """
        Export conversation history to file
        
        Args:
            file_path (str): Path to export file
        """
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.conversation_history, f, indent=2, ensure_ascii=False)
            logger.info(f"Conversation history exported to {file_path}")
        except Exception as e:
            logger.error(f"Error exporting conversation history: {str(e)}")
            raise
    
    def get_system_info(self) -> Dict[str, Any]:
        """
        Get system information
        
        Returns:
            Dict[str, Any]: System information
        """
        embedding_info = self.embedding_manager.get_model_info()
        db_stats = self.vector_db.get_database_stats()
        
        return {
            'qa_engine': {
                'model_name': MODEL_NAME,
                'conversation_history_length': len(self.conversation_history)
            },
            'embedding_model': embedding_info,
            'database': db_stats
        }


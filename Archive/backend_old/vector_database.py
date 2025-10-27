"""
Vector database for storing and retrieving document embeddings
"""
import os
import json
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
import logging
from pathlib import Path
import pickle
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)

class VectorDatabase:
    """
    Simple vector database for document storage and retrieval
    """
    
    def __init__(self, db_path: str = "./vector_db"):
        """
        Initialize the vector database
        
        Args:
            db_path (str): Path to the database directory
        """
        self.db_path = Path(db_path)
        self.db_path.mkdir(exist_ok=True)
        
        # Database files
        self.metadata_file = self.db_path / "metadata.json"
        self.embeddings_file = self.db_path / "embeddings.pkl"
        self.documents_file = self.db_path / "documents.pkl"
        
        # In-memory storage
        self.metadata = {}
        self.embeddings = np.array([])
        self.documents = []
        self.document_index = {}  # Maps document_id to index
        
        # Load existing data
        self._load_database()
    
    def _load_database(self):
        """Load existing database from disk"""
        try:
            # Load metadata
            if self.metadata_file.exists():
                with open(self.metadata_file, 'r') as f:
                    self.metadata = json.load(f)
            
            # Load embeddings
            if self.embeddings_file.exists():
                with open(self.embeddings_file, 'rb') as f:
                    self.embeddings = pickle.load(f)
            
            # Load documents
            if self.documents_file.exists():
                with open(self.documents_file, 'rb') as f:
                    self.documents = pickle.load(f)
            
            # Rebuild document index
            self._rebuild_index()
            
            logger.info(f"Loaded database with {len(self.documents)} documents")
            
        except Exception as e:
            logger.error(f"Error loading database: {str(e)}")
            # Initialize empty database
            self.metadata = {
                'created_at': datetime.now().isoformat(),
                'last_updated': datetime.now().isoformat(),
                'version': '1.0'
            }
    
    def _save_database(self):
        """Save database to disk"""
        try:
            # Update metadata
            self.metadata['last_updated'] = datetime.now().isoformat()
            self.metadata['document_count'] = len(self.documents)
            
            # Save metadata
            with open(self.metadata_file, 'w') as f:
                json.dump(self.metadata, f, indent=2)
            
            # Save embeddings
            with open(self.embeddings_file, 'wb') as f:
                pickle.dump(self.embeddings, f)
            
            # Save documents
            with open(self.documents_file, 'wb') as f:
                pickle.dump(self.documents, f)
            
            logger.info("Database saved successfully")
            
        except Exception as e:
            logger.error(f"Error saving database: {str(e)}")
            raise
    
    def _rebuild_index(self):
        """Rebuild the document index"""
        self.document_index = {}
        for i, doc in enumerate(self.documents):
            self.document_index[doc['document_id']] = i
    
    def add_document(self, document_data: Dict[str, Any], chunks: List[Dict[str, Any]], 
                    embeddings: np.ndarray) -> str:
        """
        Add a document with its chunks and embeddings to the database
        
        Args:
            document_data (Dict[str, Any]): Document metadata
            chunks (List[Dict[str, Any]]): Document chunks
            embeddings (np.ndarray): Chunk embeddings
            
        Returns:
            str: Document ID
        """
        # Generate unique document ID
        document_id = str(uuid.uuid4())
        
        # Prepare document entry
        document_entry = {
            'document_id': document_id,
            'file_name': document_data['file_name'],
            'file_path': document_data['file_path'],
            'file_hash': document_data['file_hash'],
            'file_type': document_data['file_type'],
            'file_size': document_data['file_size'],
            'word_count': document_data['word_count'],
            'char_count': document_data['char_count'],
            'chunk_count': len(chunks),
            'added_at': datetime.now().isoformat(),
            'chunks': chunks
        }
        
        # Add to documents list
        start_index = len(self.documents)
        self.documents.append(document_entry)
        
        # Add embeddings
        if len(self.embeddings) == 0:
            self.embeddings = embeddings
        else:
            self.embeddings = np.vstack([self.embeddings, embeddings])
        
        # Update document index
        self.document_index[document_id] = start_index
        
        # Save to disk
        self._save_database()
        
        logger.info(f"Added document {document_data['file_name']} with {len(chunks)} chunks")
        return document_id
    
    def remove_document(self, document_id: str) -> bool:
        """
        Remove a document from the database
        
        Args:
            document_id (str): Document ID to remove
            
        Returns:
            bool: True if document was removed, False if not found
        """
        if document_id not in self.document_index:
            logger.warning(f"Document {document_id} not found")
            return False
        
        # Get document info
        doc_index = self.document_index[document_id]
        document = self.documents[doc_index]
        chunk_count = document['chunk_count']
        
        # Remove embeddings
        start_idx = sum(doc['chunk_count'] for doc in self.documents[:doc_index])
        end_idx = start_idx + chunk_count
        
        self.embeddings = np.delete(self.embeddings, slice(start_idx, end_idx), axis=0)
        
        # Remove document
        del self.documents[doc_index]
        
        # Rebuild index
        self._rebuild_index()
        
        # Save to disk
        self._save_database()
        
        logger.info(f"Removed document {document_id}")
        return True
    
    def search_similar(self, query_embedding: np.ndarray, top_k: int = 5, 
                      document_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Search for similar documents/chunks
        
        Args:
            query_embedding (np.ndarray): Query embedding
            top_k (int): Number of results to return
            document_filter (str, optional): Filter by document ID
            
        Returns:
            List[Dict[str, Any]]: Search results
        """
        if len(self.embeddings) == 0:
            return []
        
        # Compute similarities
        similarities = np.dot(self.embeddings, query_embedding)
        
        # Get top-k indices
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        results = []
        current_chunk_idx = 0
        
        for doc in self.documents:
            # Skip if document filter is specified
            if document_filter and doc['document_id'] != document_filter:
                current_chunk_idx += doc['chunk_count']
                continue
            
            # Check if any chunks from this document are in top results
            doc_chunk_indices = range(current_chunk_idx, current_chunk_idx + doc['chunk_count'])
            
            for chunk_idx in top_indices:
                if chunk_idx in doc_chunk_indices:
                    # Get the chunk
                    local_chunk_idx = chunk_idx - current_chunk_idx
                    chunk = doc['chunks'][local_chunk_idx]
                    
                    # Calculate similarity
                    similarity = float(similarities[chunk_idx])
                    
                    result = {
                        'document_id': doc['document_id'],
                        'document_name': doc['file_name'],
                        'chunk_id': chunk['chunk_id'],
                        'chunk_text': chunk['text'],
                        'similarity': similarity,
                        'chunk_metadata': {
                            'start_pos': chunk['start_pos'],
                            'end_pos': chunk['end_pos'],
                            'length': chunk['length'],
                            'page_number': chunk.get('page_number')
                        },
                        'page_number': chunk.get('page_number')
                    }
                    
                    results.append(result)
            
            current_chunk_idx += doc['chunk_count']
        
        # Sort by similarity
        results.sort(key=lambda x: x['similarity'], reverse=True)
        
        return results[:top_k]
    
    def get_document(self, document_id: str) -> Optional[Dict[str, Any]]:
        """
        Get document by ID
        
        Args:
            document_id (str): Document ID
            
        Returns:
            Optional[Dict[str, Any]]: Document data or None if not found
        """
        if document_id not in self.document_index:
            return None
        
        return self.documents[self.document_index[document_id]]
    
    def list_documents(self) -> List[Dict[str, Any]]:
        """
        List all documents in the database
        
        Returns:
            List[Dict[str, Any]]: List of document summaries
        """
        documents = []
        
        for doc in self.documents:
            summary = {
                'document_id': doc['document_id'],
                'file_name': doc['file_name'],
                'file_type': doc['file_type'],
                'file_size': doc['file_size'],
                'word_count': doc['word_count'],
                'chunk_count': doc['chunk_count'],
                'added_at': doc['added_at']
            }
            documents.append(summary)
        
        return documents
    
    def get_database_stats(self) -> Dict[str, Any]:
        """
        Get database statistics
        
        Returns:
            Dict[str, Any]: Database statistics
        """
        total_chunks = sum(doc['chunk_count'] for doc in self.documents)
        total_words = sum(doc['word_count'] for doc in self.documents)
        total_size = sum(doc['file_size'] for doc in self.documents)
        
        return {
            'document_count': len(self.documents),
            'total_chunks': total_chunks,
            'total_words': total_words,
            'total_size_mb': round(total_size / (1024 * 1024), 2),
            'embedding_dimension': self.embeddings.shape[1] if len(self.embeddings) > 0 else 0,
            'created_at': self.metadata.get('created_at', 'Unknown'),
            'last_updated': self.metadata.get('last_updated', 'Unknown')
        }
    
    def clear_database(self):
        """Clear all data from the database"""
        self.metadata = {
            'created_at': datetime.now().isoformat(),
            'last_updated': datetime.now().isoformat(),
            'version': '1.0'
        }
        self.embeddings = np.array([])
        self.documents = []
        self.document_index = {}
        
        self._save_database()
        logger.info("Database cleared")
    
    def export_database(self, export_path: str):
        """
        Export database to a file
        
        Args:
            export_path (str): Path to export file
        """
        export_data = {
            'metadata': self.metadata,
            'documents': self.documents,
            'exported_at': datetime.now().isoformat()
        }
        
        with open(export_path, 'w') as f:
            json.dump(export_data, f, indent=2, default=str)
        
        logger.info(f"Database exported to {export_path}")
    
    def import_database(self, import_path: str):
        """
        Import database from a file
        
        Args:
            import_path (str): Path to import file
        """
        with open(import_path, 'r') as f:
            import_data = json.load(f)
        
        self.metadata = import_data['metadata']
        self.documents = import_data['documents']
        
        # Rebuild index
        self._rebuild_index()
        
        # Note: Embeddings would need to be regenerated
        logger.warning("Imported documents. Embeddings need to be regenerated.")
        
        self._save_database()
        logger.info(f"Database imported from {import_path}")


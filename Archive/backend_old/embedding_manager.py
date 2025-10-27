"""
Embedding management system for document vectorization
"""
import os
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from sentence_transformers import SentenceTransformer
import logging
import pickle
from pathlib import Path
import hashlib

logger = logging.getLogger(__name__)

class EmbeddingManager:
    """
    Manages text embeddings using sentence transformers
    """
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2", cache_dir: str = "./embeddings_cache"):
        """
        Initialize the embedding manager
        
        Args:
            model_name (str): Name of the sentence transformer model
            cache_dir (str): Directory to cache embeddings
        """
        self.model_name = model_name
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        
        # Initialize the sentence transformer model
        try:
            self.model = SentenceTransformer(model_name)
            logger.info(f"Loaded embedding model: {model_name}")
        except Exception as e:
            logger.error(f"Failed to load embedding model {model_name}: {str(e)}")
            raise
    
    def generate_embeddings(self, texts: List[str], use_cache: bool = True) -> np.ndarray:
        """
        Generate embeddings for a list of texts
        
        Args:
            texts (List[str]): List of texts to embed
            use_cache (bool): Whether to use cached embeddings
            
        Returns:
            np.ndarray: Array of embeddings
        """
        if not texts:
            return np.array([])
        
        embeddings = []
        uncached_texts = []
        uncached_indices = []
        
        for i, text in enumerate(texts):
            if use_cache:
                cached_embedding = self._get_cached_embedding(text)
                if cached_embedding is not None:
                    embeddings.append(cached_embedding)
                    continue
            
            uncached_texts.append(text)
            uncached_indices.append(i)
        
        # Generate embeddings for uncached texts
        if uncached_texts:
            try:
                new_embeddings = self.model.encode(uncached_texts, show_progress_bar=False)
                
                # Cache new embeddings
                if use_cache:
                    for text, embedding in zip(uncached_texts, new_embeddings):
                        self._cache_embedding(text, embedding)
                
                # Insert new embeddings at correct positions
                for i, embedding in zip(uncached_indices, new_embeddings):
                    embeddings.insert(i, embedding)
                    
            except Exception as e:
                logger.error(f"Error generating embeddings: {str(e)}")
                raise
        
        return np.array(embeddings)
    
    def generate_single_embedding(self, text: str, use_cache: bool = True) -> np.ndarray:
        """
        Generate embedding for a single text
        
        Args:
            text (str): Text to embed
            use_cache (bool): Whether to use cached embedding
            
        Returns:
            np.ndarray: Text embedding
        """
        embeddings = self.generate_embeddings([text], use_cache)
        return embeddings[0] if len(embeddings) > 0 else np.array([])
    
    def _get_cached_embedding(self, text: str) -> Optional[np.ndarray]:
        """Get cached embedding for text if it exists"""
        try:
            text_hash = self._hash_text(text)
            cache_file = self.cache_dir / f"{text_hash}.pkl"
            
            if cache_file.exists():
                with open(cache_file, 'rb') as f:
                    return pickle.load(f)
        except Exception as e:
            logger.warning(f"Error loading cached embedding: {str(e)}")
        
        return None
    
    def _cache_embedding(self, text: str, embedding: np.ndarray):
        """Cache embedding for text"""
        try:
            text_hash = self._hash_text(text)
            cache_file = self.cache_dir / f"{text_hash}.pkl"
            
            with open(cache_file, 'wb') as f:
                pickle.dump(embedding, f)
        except Exception as e:
            logger.warning(f"Error caching embedding: {str(e)}")
    
    def _hash_text(self, text: str) -> str:
        """Generate hash for text"""
        return hashlib.md5(text.encode('utf-8')).hexdigest()
    
    def compute_similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """
        Compute cosine similarity between two embeddings
        
        Args:
            embedding1 (np.ndarray): First embedding
            embedding2 (np.ndarray): Second embedding
            
        Returns:
            float: Cosine similarity score
        """
        # Normalize embeddings
        norm1 = np.linalg.norm(embedding1)
        norm2 = np.linalg.norm(embedding2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        # Compute cosine similarity
        similarity = np.dot(embedding1, embedding2) / (norm1 * norm2)
        return float(similarity)
    
    def find_most_similar(self, query_embedding: np.ndarray, candidate_embeddings: np.ndarray, 
                         top_k: int = 5) -> List[Tuple[int, float]]:
        """
        Find most similar embeddings to query
        
        Args:
            query_embedding (np.ndarray): Query embedding
            candidate_embeddings (np.ndarray): Candidate embeddings
            top_k (int): Number of top results to return
            
        Returns:
            List[Tuple[int, float]]: List of (index, similarity) tuples
        """
        if len(candidate_embeddings) == 0:
            return []
        
        # Compute similarities
        similarities = []
        for i, candidate in enumerate(candidate_embeddings):
            similarity = self.compute_similarity(query_embedding, candidate)
            similarities.append((i, similarity))
        
        # Sort by similarity (descending)
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        return similarities[:top_k]
    
    def batch_similarity_search(self, query_embeddings: np.ndarray, candidate_embeddings: np.ndarray,
                               top_k: int = 5) -> List[List[Tuple[int, float]]]:
        """
        Perform batch similarity search
        
        Args:
            query_embeddings (np.ndarray): Query embeddings
            candidate_embeddings (np.ndarray): Candidate embeddings
            top_k (int): Number of top results per query
            
        Returns:
            List[List[Tuple[int, float]]]: List of results for each query
        """
        results = []
        
        for query_embedding in query_embeddings:
            query_results = self.find_most_similar(query_embedding, candidate_embeddings, top_k)
            results.append(query_results)
        
        return results
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the embedding model
        
        Returns:
            Dict[str, Any]: Model information
        """
        return {
            'model_name': self.model_name,
            'max_seq_length': getattr(self.model, 'max_seq_length', 'Unknown'),
            'embedding_dimension': self.model.get_sentence_embedding_dimension(),
            'cache_dir': str(self.cache_dir),
            'cache_size': len(list(self.cache_dir.glob('*.pkl'))) if self.cache_dir.exists() else 0
        }
    
    def clear_cache(self):
        """Clear the embedding cache"""
        try:
            cache_files = list(self.cache_dir.glob('*.pkl'))
            for cache_file in cache_files:
                cache_file.unlink()
            logger.info(f"Cleared {len(cache_files)} cached embeddings")
        except Exception as e:
            logger.error(f"Error clearing cache: {str(e)}")
    
    def save_embeddings(self, embeddings: np.ndarray, texts: List[str], file_path: str):
        """
        Save embeddings and associated texts to file
        
        Args:
            embeddings (np.ndarray): Embeddings to save
            texts (List[str]): Associated texts
            file_path (str): Path to save file
        """
        try:
            data = {
                'embeddings': embeddings,
                'texts': texts,
                'model_name': self.model_name
            }
            
            with open(file_path, 'wb') as f:
                pickle.dump(data, f)
            
            logger.info(f"Saved {len(embeddings)} embeddings to {file_path}")
        except Exception as e:
            logger.error(f"Error saving embeddings: {str(e)}")
            raise
    
    def load_embeddings(self, file_path: str) -> Tuple[np.ndarray, List[str]]:
        """
        Load embeddings and associated texts from file
        
        Args:
            file_path (str): Path to load file
            
        Returns:
            Tuple[np.ndarray, List[str]]: Embeddings and texts
        """
        try:
            with open(file_path, 'rb') as f:
                data = pickle.load(f)
            
            embeddings = data['embeddings']
            texts = data['texts']
            
            logger.info(f"Loaded {len(embeddings)} embeddings from {file_path}")
            return embeddings, texts
        except Exception as e:
            logger.error(f"Error loading embeddings: {str(e)}")
            raise


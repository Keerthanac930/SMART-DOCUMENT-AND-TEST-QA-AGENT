"""
Document processing utilities for text extraction and vector search
"""
import os
import fitz  # PyMuPDF
from docx import Document as DocxDocument
from PIL import Image
import pytesseract
import chromadb
from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Dict, Any, Optional
import json

class DocumentProcessor:
    def __init__(self):
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.chroma_client = chromadb.PersistentClient(path="chroma_db")
        self.collection = self.chroma_client.get_or_create_collection("documents")
    
    def extract_text_from_pdf(self, file_path: str) -> Dict[str, Any]:
        """Extract text from PDF file with page numbers"""
        doc = None
        try:
            doc = fitz.open(file_path)
            text_content = []
            page_contents = []
            total_pages = len(doc)
            
            for page_num in range(total_pages):
                page = doc.load_page(page_num)
                text = page.get_text()
                if text.strip():
                    text_content.append(text)
                    page_contents.append({
                        "page_number": page_num + 1,
                        "text": text,
                        "word_count": len(text.split())
                    })
            
            result = {
                "full_text": "\n".join(text_content),
                "page_contents": page_contents,
                "total_pages": total_pages,
                "total_words": sum(len(text.split()) for text in text_content)
            }
            
            return result
        except Exception as e:
            raise Exception(f"Error extracting PDF text: {str(e)}")
        finally:
            if doc is not None:
                doc.close()
    
    def extract_text_from_docx(self, file_path: str) -> Dict[str, Any]:
        """Extract text from DOCX file"""
        try:
            doc = DocxDocument(file_path)
            text_content = []
            
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    text_content.append(paragraph.text)
            
            full_text = "\n".join(text_content)
            
            return {
                "full_text": full_text,
                "page_contents": [{"page_number": 1, "text": full_text, "word_count": len(full_text.split())}],
                "total_pages": 1,
                "total_words": len(full_text.split())
            }
        except Exception as e:
            raise Exception(f"Error extracting DOCX text: {str(e)}")
    
    def extract_text_from_image(self, file_path: str) -> Dict[str, Any]:
        """Extract text from image using OCR"""
        try:
            image = Image.open(file_path)
            text = pytesseract.image_to_string(image)
            
            return {
                "full_text": text,
                "page_contents": [{"page_number": 1, "text": text, "word_count": len(text.split())}],
                "total_pages": 1,
                "total_words": len(text.split())
            }
        except Exception as e:
            raise Exception(f"Error extracting text from image: {str(e)}")
    
    def extract_text_from_document(self, file_path: str) -> Dict[str, Any]:
        """Extract text from various document types"""
        file_extension = os.path.splitext(file_path)[1].lower()
        
        if file_extension == '.pdf':
            return self.extract_text_from_pdf(file_path)
        elif file_extension in ['.docx', '.doc']:
            return self.extract_text_from_docx(file_path)
        elif file_extension in ['.png', '.jpg', '.jpeg', '.tiff', '.bmp']:
            return self.extract_text_from_image(file_path)
        elif file_extension == '.txt':
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
            return {
                "full_text": text,
                "page_contents": [{"page_number": 1, "text": text, "word_count": len(text.split())}],
                "total_pages": 1,
                "total_words": len(text.split())
            }
        else:
            raise Exception(f"Unsupported file type: {file_extension}")
    
    def create_embeddings(self, text: str) -> np.ndarray:
        """Create embeddings for text"""
        return self.embedding_model.encode(text)
    
    def store_document_embeddings(self, document_id: str, text_content: Dict[str, Any]):
        """Store document embeddings in vector database"""
        try:
            # Split text into chunks for better search
            chunks = self.split_text_into_chunks(text_content["full_text"], chunk_size=1000)
            
            embeddings = []
            metadatas = []
            ids = []
            
            for i, chunk in enumerate(chunks):
                embedding = self.create_embeddings(chunk)
                embeddings.append(embedding.tolist())
                
                # Find which page this chunk belongs to
                page_number = 1
                for page_content in text_content["page_contents"]:
                    if chunk in page_content["text"]:
                        page_number = page_content["page_number"]
                        break
                
                metadatas.append({
                    "document_id": document_id,
                    "chunk_index": i,
                    "page_number": page_number,
                    "text": chunk
                })
                ids.append(f"{document_id}_chunk_{i}")
            
            # Store in ChromaDB
            self.collection.add(
                embeddings=embeddings,
                metadatas=metadatas,
                ids=ids
            )
            
        except Exception as e:
            raise Exception(f"Error storing document embeddings: {str(e)}")
    
    def search_documents(self, query: str, documents: List[Any]) -> Optional[Dict[str, Any]]:
        """Search for relevant content in documents"""
        try:
            # Create query embedding
            query_embedding = self.create_embeddings(query)
            
            # Search in vector database
            results = self.collection.query(
                query_embeddings=[query_embedding.tolist()],
                n_results=5
            )
            
            if not results['metadatas'] or not results['metadatas'][0]:
                return None
            
            # Combine relevant chunks
            relevant_texts = []
            citations = []
            page_numbers = []
            
            for metadata in results['metadatas'][0]:
                relevant_texts.append(metadata['text'])
                citations.append({
                    "document_id": metadata['document_id'],
                    "page_number": metadata['page_number'],
                    "chunk_index": metadata['chunk_index']
                })
                page_numbers.append(metadata['page_number'])
            
            combined_text = "\n".join(relevant_texts)
            
            return {
                "text": combined_text,
                "citations": citations,
                "page_numbers": list(set(page_numbers))
            }
            
        except Exception as e:
            raise Exception(f"Error searching documents: {str(e)}")
    
    def split_text_into_chunks(self, text: str, chunk_size: int = 1000, overlap: int = 100) -> List[str]:
        """Split text into overlapping chunks"""
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size - overlap):
            chunk = " ".join(words[i:i + chunk_size])
            chunks.append(chunk)
        
        return chunks
    
    def process_document(self, file_path: str, document_id: str) -> Dict[str, Any]:
        """Complete document processing pipeline"""
        try:
            # Extract text
            text_content = self.extract_text_from_document(file_path)
            
            # Store embeddings
            self.store_document_embeddings(str(document_id), text_content)
            
            return {
                "success": True,
                "text_content": text_content,
                "processed": True
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "processed": False
            }

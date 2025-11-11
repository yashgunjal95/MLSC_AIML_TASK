"""Vector store interface using FAISS"""

import faiss
import numpy as np
import pickle
from pathlib import Path
from typing import List, Dict, Optional
from src.utils.config import VECTOR_DB_DIR, COLLECTION_NAME, TOP_K_RESULTS
from src.core.code_parser import CodeChunk
from src.core.embeddings import EmbeddingGenerator
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

class VectorStore:
    """Manage code chunks in FAISS vector database"""
    
    def __init__(self):
        self.embedding_generator = EmbeddingGenerator()
        self.index = None
        self.documents = []
        self.metadatas = []
        self.index_path = Path(VECTOR_DB_DIR) / f"{COLLECTION_NAME}.index"
        self.data_path = Path(VECTOR_DB_DIR) / f"{COLLECTION_NAME}.pkl"
        
        # Load existing index if available
        self._load_index()
        logger.info(f"Vector store initialized with {len(self.documents)} documents")
    
    def _load_index(self):
        """Load existing FAISS index and data"""
        if self.index_path.exists() and self.data_path.exists():
            try:
                self.index = faiss.read_index(str(self.index_path))
                with open(self.data_path, 'rb') as f:
                    data = pickle.load(f)
                    self.documents = data['documents']
                    self.metadatas = data['metadatas']
                logger.info(f"Loaded existing index with {len(self.documents)} documents")
            except Exception as e:
                logger.error(f"Error loading index: {e}")
                self._create_new_index()
        else:
            self._create_new_index()
    
    def _create_new_index(self):
        """Create new FAISS index"""
        dimension = 384  # sentence-transformers dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.documents = []
        self.metadatas = []
    
    def _save_index(self):
        """Save FAISS index and data"""
        try:
            Path(VECTOR_DB_DIR).mkdir(parents=True, exist_ok=True)
            faiss.write_index(self.index, str(self.index_path))
            with open(self.data_path, 'wb') as f:
                pickle.dump({'documents': self.documents, 'metadatas': self.metadatas}, f)
        except Exception as e:
            logger.error(f"Error saving index: {e}")
    
    def add_chunks(self, chunks: List[CodeChunk]):
        """Add code chunks to vector store"""
        if not chunks:
            return
        
        documents = [chunk.content for chunk in chunks]
        embeddings = self.embedding_generator.generate_embeddings(documents)
        
        # Convert to numpy array
        embeddings_array = np.array(embeddings).astype('float32')
        
        # Add to FAISS index
        self.index.add(embeddings_array)
        
        # Store documents and metadata
        for chunk in chunks:
            self.documents.append(chunk.content)
            self.metadatas.append({
                "file_path": chunk.file_path,
                "language": chunk.language,
                "chunk_type": chunk.chunk_type,
                "name": chunk.name or "",
                "start_line": chunk.start_line,
                "end_line": chunk.end_line
            })
        
        self._save_index()
        logger.info(f"Added {len(chunks)} chunks to vector store")
    
    def search(self, query: str, k: int = TOP_K_RESULTS, filter_dict: Optional[Dict] = None) -> Dict:
        """Search for relevant code chunks"""
        if self.index.ntotal == 0:
            return {"documents": [], "metadatas": [], "distances": []}
        
        # Generate query embedding
        query_embedding = self.embedding_generator.generate_embedding(query)
        query_array = np.array([query_embedding]).astype('float32')
        
        # Search
        k = min(k, self.index.ntotal)
        distances, indices = self.index.search(query_array, k)
        
        # Get results
        results_docs = []
        results_meta = []
        results_dist = []
        
        for idx, dist in zip(indices[0], distances[0]):
            if idx < len(self.documents):
                # Apply filter if provided
                if filter_dict:
                    metadata = self.metadatas[idx]
                    if all(metadata.get(k) == v for k, v in filter_dict.items()):
                        results_docs.append(self.documents[idx])
                        results_meta.append(metadata)
                        results_dist.append(float(dist))
                else:
                    results_docs.append(self.documents[idx])
                    results_meta.append(self.metadatas[idx])
                    results_dist.append(float(dist))
        
        return {
            "documents": results_docs,
            "metadatas": results_meta,
            "distances": results_dist
        }
    
    def delete_by_file(self, file_path: str):
        """Delete all chunks from a specific file"""
        # Find indices to keep
        indices_to_keep = [i for i, meta in enumerate(self.metadatas) 
                          if meta['file_path'] != file_path]
        
        if len(indices_to_keep) == len(self.documents):
            logger.info(f"No chunks found for {file_path}")
            return
        
        # Recreate index with remaining documents
        self.documents = [self.documents[i] for i in indices_to_keep]
        self.metadatas = [self.metadatas[i] for i in indices_to_keep]
        
        # Rebuild FAISS index
        self._create_new_index()
        if self.documents:
            embeddings = self.embedding_generator.generate_embeddings(self.documents)
            embeddings_array = np.array(embeddings).astype('float32')
            self.index.add(embeddings_array)
        
        self._save_index()
        logger.info(f"Deleted chunks from {file_path}")
    
    def clear(self):
        """Clear all documents from collection"""
        self._create_new_index()
        self._save_index()
        logger.info("Vector store cleared")
    
    def get_stats(self) -> Dict:
        """Get collection statistics"""
        return {
            "total_chunks": len(self.documents),
            "collection_name": COLLECTION_NAME
        }
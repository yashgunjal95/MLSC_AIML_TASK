"""Document retrieval from vector store"""

from typing import List, Dict, Optional
from src.core.vector_store import VectorStore
from src.utils.config import TOP_K_RESULTS
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

class CodeRetriever:
    """Retrieve relevant code chunks"""
    
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store
    
    def retrieve(self, query: str, k: int = TOP_K_RESULTS, 
                 language: Optional[str] = None) -> List[Dict]:
        """Retrieve relevant code chunks for query"""
        
        # Build filter
        filter_dict = None
        if language:
            filter_dict = {"language": language}
        
        # Search vector store
        results = self.vector_store.search(query, k=k, filter_dict=filter_dict)
        
        # Format results
        retrieved_chunks = []
        for doc, metadata, distance in zip(
            results["documents"], 
            results["metadatas"], 
            results["distances"]
        ):
            retrieved_chunks.append({
                "content": doc,
                "metadata": metadata,
                "score": 1 - distance  # Convert distance to similarity
            })
        
        logger.info(f"Retrieved {len(retrieved_chunks)} chunks for query")
        return retrieved_chunks
    
    def retrieve_by_file(self, file_path: str, k: int = 10) -> List[Dict]:
        """Retrieve all chunks from specific file"""
        results = self.vector_store.search(
            query="",  # Empty query, will use filter only
            k=k,
            filter_dict={"file_path": file_path}
        )
        
        retrieved_chunks = []
        for doc, metadata in zip(results["documents"], results["metadatas"]):
            retrieved_chunks.append({
                "content": doc,
                "metadata": metadata
            })
        
        return retrieved_chunks
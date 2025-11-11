"""Embedding generation using sentence-transformers"""

from typing import List
import torch
from sentence_transformers import SentenceTransformer
from src.utils.config import EMBEDDING_MODEL
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

class EmbeddingGenerator:
    """Generate embeddings for code chunks"""

    def __init__(self):
        logger.info(f"Loading embedding model: {EMBEDDING_MODEL}")
        # Load model without device parameter to avoid meta tensor issues
        # The model will automatically detect and use CPU
        try:
            self.model = SentenceTransformer(
                EMBEDDING_MODEL,
                cache_folder=None,  # Use default cache
                trust_remote_code=False
            )
            # Explicitly move to CPU after loading
            self.model = self.model.cpu()
            logger.info("Model loaded successfully on CPU")
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise
    
    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for single text"""
        embedding = self.model.encode(text, convert_to_numpy=True)
        return embedding.tolist()
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts"""
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        return embeddings.tolist()
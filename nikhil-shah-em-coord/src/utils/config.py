"""Configuration settings for CodeSense AI"""

from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / "data"
VECTOR_DB_DIR = DATA_DIR / "vector_db"
UPLOADS_DIR = DATA_DIR / "uploads"

# Create directories if they don't exist
VECTOR_DB_DIR.mkdir(parents=True, exist_ok=True)
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

# LLM Settings
OLLAMA_BASE_URL = "http://localhost:11434"
MODEL_NAME = "codellama:7b"
TEMPERATURE = 0.1
MAX_TOKENS = 2048

# Embedding Settings
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_DIM = 384

# Chunking Settings
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
MAX_CHUNK_SIZE = 2000

# Vector Store Settings
COLLECTION_NAME = "code_collection"
TOP_K_RESULTS = 5

# Supported file extensions
SUPPORTED_EXTENSIONS = {
    ".py": "python",
    ".js": "javascript",
    ".jsx": "javascript",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".json": "json",
    ".md": "markdown"
}

# Agent Settings
MAX_HISTORY_LENGTH = 5
STREAM_RESPONSE = True
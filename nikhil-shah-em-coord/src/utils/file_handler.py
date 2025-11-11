"""File handling utilities"""

import os
from pathlib import Path
from typing import List
from src.utils.config import SUPPORTED_EXTENSIONS, UPLOADS_DIR
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

def is_supported_file(file_path: str) -> bool:
    """Check if file extension is supported"""
    return Path(file_path).suffix in SUPPORTED_EXTENSIONS

def get_file_language(file_path: str) -> str:
    """Get language from file extension"""
    ext = Path(file_path).suffix
    return SUPPORTED_EXTENSIONS.get(ext, "unknown")

def read_file(file_path: str) -> str:
    """Read file content"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        logger.error(f"Error reading file {file_path}: {e}")
        return ""

def get_files_from_directory(directory: str) -> List[str]:
    """Recursively get all supported files from directory"""
    files = []
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            file_path = os.path.join(root, filename)
            if is_supported_file(file_path):
                files.append(file_path)
    return files

def save_uploaded_file(uploaded_file) -> str:
    """Save uploaded file to uploads directory"""
    file_path = UPLOADS_DIR / uploaded_file.name
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return str(file_path)
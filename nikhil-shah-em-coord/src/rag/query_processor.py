"""Query processing and understanding"""

import re
from typing import Dict, List, Optional
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

class QueryProcessor:
    """Process and understand user queries"""

    def __init__(self):
        self.intent_keywords = {
            "error": ["error", "exception", "bug", "fix", "crash", "fail"],
            "review": ["review", "improve", "optimize", "refactor", "better"],
            "explain": ["explain", "how", "what", "why", "understand", "describe"],
            "analyze": ["analyze", "show", "find", "search", "get"]
        }

    def process_query(self, query: str) -> Dict:
        """Process query and extract intent"""
        query_lower = query.lower()

        return {
            "original": query,
            "normalized": query_lower.strip(),
            "intent": self._detect_intent(query_lower),
            "keywords": self._extract_keywords(query_lower),
            "file_mentioned": self._extract_file_name(query)
        }

    def _detect_intent(self, query: str) -> str:
        """Detect query intent based on keywords"""
        for intent, keywords in self.intent_keywords.items():
            if any(keyword in query for keyword in keywords):
                return intent
        return "analyze"

    def _extract_keywords(self, query: str) -> List[str]:
        """Extract important keywords from query"""
        stop_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for"}
        words = query.split()
        return [w for w in words if w not in stop_words and len(w) > 2]

    def _extract_file_name(self, query: str) -> Optional[str]:
        """Extract file name from query if mentioned"""
        # Pattern to match common file names (e.g., app.py, analyzer_agent.py, etc.)
        file_pattern = r'\b[\w_-]+\.(py|js|jsx|ts|tsx|json|md)\b'
        matches = re.findall(file_pattern, query, re.IGNORECASE)

        if matches:
            # Return the full match (filename with extension)
            full_matches = re.findall(r'\b[\w_-]+\.' + r'(?:' + r'|'.join(['py', 'js', 'jsx', 'ts', 'tsx', 'json', 'md']) + r')\b', query, re.IGNORECASE)
            if full_matches:
                logger.info(f"Detected file name in query: {full_matches[0]}")
                return full_matches[0]

        return None
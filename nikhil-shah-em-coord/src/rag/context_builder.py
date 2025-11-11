"""Build context for LLM prompts"""

from typing import List, Dict
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

class ContextBuilder:
    """Build context from retrieved chunks and chat history"""
    
    def __init__(self, max_history: int = 5):
        self.max_history = max_history
    
    def build_context(self,
                     retrieved_chunks: List[Dict],
                     chat_history: List[Dict],
                     query: str) -> str:
        """Build complete context for LLM"""

        context_parts = []

        # Add retrieved code chunks
        if retrieved_chunks:
            context_parts.append("### Relevant Code:\n")
            for i, chunk in enumerate(retrieved_chunks[:5], 1):
                metadata = chunk["metadata"]
                content = chunk["content"]

                context_parts.append(
                    f"**Chunk {i}** (File: {metadata['file_path']}, "
                    f"Lines: {metadata['start_line']}-{metadata['end_line']})\n"
                    f"```{metadata['language']}\n{content}\n```\n"
                )

        # Add recent chat history (only user questions for context, not assistant responses)
        if chat_history:
            recent_history = chat_history[-self.max_history:]
            user_questions = [msg for msg in recent_history if msg["role"] == "user"]
            if user_questions:
                context_parts.append("\n### Previous User Questions:\n")
                for i, msg in enumerate(user_questions, 1):
                    context_parts.append(f"{i}. {msg['content']}\n")

        # Add current query
        context_parts.append(f"\n### Current Question:\n{query}\n")

        return "\n".join(context_parts)
    
    def format_sources(self, chunks: List[Dict]) -> str:
        """Format source attribution"""
        if not chunks:
            return ""
        
        sources = []
        seen_files = set()
        
        for chunk in chunks:
            file_path = chunk["metadata"]["file_path"]
            if file_path not in seen_files:
                sources.append(f"- {file_path}")
                seen_files.add(file_path)
        
        return "**Sources:**\n" + "\n".join(sources)
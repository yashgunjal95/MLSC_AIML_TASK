"""Base agent class for all specialized agents"""

from typing import Iterator, List, Dict
from src.llm.ollama_client import OllamaClient
from src.rag.retriever import CodeRetriever
from src.rag.context_builder import ContextBuilder
from src.rag.query_processor import QueryProcessor
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

class BaseAgent:
    """Base class for all agents"""

    def __init__(self, llm_client: OllamaClient, retriever: CodeRetriever):
        self.llm = llm_client
        self.retriever = retriever
        self.context_builder = ContextBuilder()
        self.query_processor = QueryProcessor()
        self.agent_type = "base"

    def process_query(self, query: str, chat_history: List[Dict],
                     stream: bool = True) -> Iterator[str]:
        """Process query and generate response"""

        # Process query to detect file mentions
        processed_query = self.query_processor.process_query(query)
        file_mentioned = processed_query.get("file_mentioned")

        # Retrieve relevant code with file filtering if file is mentioned
        if file_mentioned:
            logger.info(f"Filtering retrieval to file: {file_mentioned}")
            retrieved_chunks = self._retrieve_from_file(file_mentioned, query)
        else:
            retrieved_chunks = self.retriever.retrieve(query)

        # Build context
        context = self.context_builder.build_context(
            retrieved_chunks, chat_history, query
        )

        # Generate prompt
        prompt = self._build_prompt(context)

        # Generate response
        for token in self.llm.generate(prompt, stream=stream):
            yield token

        # Yield sources at the end
        if retrieved_chunks:
            yield "\n\n" + self.context_builder.format_sources(retrieved_chunks)

    def _retrieve_from_file(self, file_name: str, query: str) -> List[Dict]:
        """Retrieve chunks from a specific file"""
        # Search with file name filter
        all_chunks = self.retriever.vector_store.documents
        all_metadata = self.retriever.vector_store.metadatas

        # Find chunks from the specific file
        file_chunks = []
        for i, metadata in enumerate(all_metadata):
            if file_name.lower() in metadata['file_path'].lower():
                file_chunks.append({
                    "content": all_chunks[i],
                    "metadata": metadata,
                    "score": 1.0  # All chunks from requested file are relevant
                })

        logger.info(f"Retrieved {len(file_chunks)} chunks from {file_name}")
        return file_chunks

    def _build_prompt(self, context: str) -> str:
        """Build prompt for LLM - override in subclasses"""
        return context
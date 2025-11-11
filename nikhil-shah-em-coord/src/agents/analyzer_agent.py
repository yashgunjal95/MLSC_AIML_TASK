"""Analyzer agent for code understanding and Q&A"""

from src.agents.base_agent import BaseAgent
from src.llm.prompts import get_prompt_template

class AnalyzerAgent(BaseAgent):
    """Agent for code analysis and general Q&A"""
    
    def __init__(self, llm_client, retriever):
        super().__init__(llm_client, retriever)
        self.agent_type = "analyzer"
        self.prompt_template = get_prompt_template("analyzer")
    
    def _build_prompt(self, context: str) -> str:
        """Build analyzer-specific prompt"""
        return self.prompt_template.format(context=context)
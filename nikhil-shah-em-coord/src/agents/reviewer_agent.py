"""Reviewer agent for code quality and improvements"""

from src.agents.base_agent import BaseAgent
from src.llm.prompts import get_prompt_template

class ReviewerAgent(BaseAgent):
    """Agent for code review and suggestions"""
    
    def __init__(self, llm_client, retriever):
        super().__init__(llm_client, retriever)
        self.agent_type = "reviewer"
        self.prompt_template = get_prompt_template("reviewer")
    
    def _build_prompt(self, context: str) -> str:
        """Build reviewer-specific prompt"""
        return self.prompt_template.format(context=context)
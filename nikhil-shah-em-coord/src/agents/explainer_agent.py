"""Explainer agent for code documentation"""

from src.agents.base_agent import BaseAgent
from src.llm.prompts import get_prompt_template

class ExplainerAgent(BaseAgent):
    """Agent for code explanation and documentation"""
    
    def __init__(self, llm_client, retriever):
        super().__init__(llm_client, retriever)
        self.agent_type = "explainer"
        self.prompt_template = get_prompt_template("explainer")
    
    def _build_prompt(self, context: str) -> str:
        """Build explainer-specific prompt"""
        return self.prompt_template.format(context=context)
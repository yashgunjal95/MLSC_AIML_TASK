"""Debugger agent for error solving"""

from src.agents.base_agent import BaseAgent
from src.llm.prompts import get_prompt_template

class DebuggerAgent(BaseAgent):
    """Agent for debugging and error resolution"""
    
    def __init__(self, llm_client, retriever):
        super().__init__(llm_client, retriever)
        self.agent_type = "debugger"
        self.prompt_template = get_prompt_template("debugger")
    
    def _build_prompt(self, context: str) -> str:
        """Build debugger-specific prompt"""
        return self.prompt_template.format(context=context)
"""Router agent for intelligent query routing"""

from src.agents.analyzer_agent import AnalyzerAgent
from src.agents.reviewer_agent import ReviewerAgent
from src.agents.debugger_agent import DebuggerAgent
from src.agents.explainer_agent import ExplainerAgent
from src.rag.query_processor import QueryProcessor
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

class RouterAgent:
    """Route queries to appropriate specialized agent"""
    
    def __init__(self, llm_client, retriever):
        self.query_processor = QueryProcessor()
        
        # Initialize all agents
        self.agents = {
            "analyzer": AnalyzerAgent(llm_client, retriever),
            "reviewer": ReviewerAgent(llm_client, retriever),
            "debugger": DebuggerAgent(llm_client, retriever),
            "explainer": ExplainerAgent(llm_client, retriever)
        }
    
    def route_query(self, query: str, mode: str = "auto"):
        """Route query to appropriate agent"""
        
        # If mode is specified, use that agent
        if mode in self.agents and mode != "auto":
            logger.info(f"Using {mode} agent (manual selection)")
            return self.agents[mode]
        
        # Auto-detect intent
        processed = self.query_processor.process_query(query)
        intent = processed["intent"]
        
        # Map intent to agent
        agent_map = {
            "error": "debugger",
            "review": "reviewer",
            "explain": "explainer",
            "analyze": "analyzer"
        }
        
        agent_type = agent_map.get(intent, "analyzer")
        logger.info(f"Routed to {agent_type} agent (detected intent: {intent})")
        
        return self.agents[agent_type]
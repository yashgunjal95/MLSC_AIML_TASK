"""Ollama LLM client"""

import requests
from typing import Iterator
from src.utils.config import OLLAMA_BASE_URL, MODEL_NAME, TEMPERATURE, MAX_TOKENS
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

class OllamaClient:
    """Interface for Ollama LLM"""
    
    def __init__(self):
        self.base_url = OLLAMA_BASE_URL
        self.model = MODEL_NAME
        self.temperature = TEMPERATURE
        self.max_tokens = MAX_TOKENS
    
    def generate(self, prompt: str, stream: bool = True) -> Iterator[str]:
        """Generate response from LLM"""
        url = f"{self.base_url}/api/generate"
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": stream,
            "options": {
                "temperature": self.temperature,
                "num_predict": self.max_tokens
            }
        }
        
        try:
            response = requests.post(url, json=payload, stream=stream)
            response.raise_for_status()
            
            if stream:
                for line in response.iter_lines():
                    if line:
                        import json
                        data = json.loads(line)
                        if "response" in data:
                            yield data["response"]
            else:
                import json
                data = response.json()
                yield data.get("response", "")
                
        except Exception as e:
            logger.error(f"Ollama generation error: {e}")
            yield f"Error: {str(e)}"
    
    def check_model(self) -> bool:
        """Check if model is available"""
        try:
            url = f"{self.base_url}/api/tags"
            response = requests.get(url)
            response.raise_for_status()
            
            models = response.json().get("models", [])
            return any(self.model in model.get("name", "") for model in models)
        except Exception as e:
            logger.error(f"Error checking model: {e}")
            return False
import sqlite3
import os
import requests
from .base_factory import AiAgent
from .ollama_factory import OllamaFactory


class AiFactoryManager:
    @staticmethod
    # factory method to get the appropriate AI agent based on the specified type and configuration
    def get_agent(agent_type:str, config:dict) -> AiAgent:
        
        # we may extend this factory method in the future to support multiple types 
        # of AI agents (e.g., OpenAI, Cohere, etc.)
        if agent_type == "ollama":
            # in this example, we are only implementing the OllamaFactory, 
            # but we can easily add more agent types in the future by extending this factory method
            model_name = config.get("model_name", "gemma3:1b")
            return OllamaFactory(model_name=model_name)

        else:
            raise ValueError(f"Unknown agent type: {agent_type}")




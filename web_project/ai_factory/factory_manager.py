import sqlite3
import os
import requests
from .base_factory import AiAgent
from .ollama_factory import OllamaFactory


class AiFactoryManager:
    @staticmethod
    def get_agent(agent_type:str, config:dict) -> AiAgent:
        
        if agent_type == "ollama":
           
            model_name = config.get("model_name", "gemma3:1b")

            return OllamaFactory(model_name=model_name)

        else:
            raise ValueError(f"Unknown agent type: {agent_type}")




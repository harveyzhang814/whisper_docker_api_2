"""
This module manages the loading and retrieval of transcription models.
It reads model configurations, loads models into memory, and provides access to them for API endpoints.
"""
import os
import yaml
from typing import Dict, Any
import whisper

class ModelManager:
    def __init__(self, config_path: str):
        self.models: Dict[str, Any] = {}
        self.load_config(config_path)

    def load_config(self, config_path: str):
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        self.api_config = config.get('api', {})
        self.model_configs = config.get('models', [])
        self.load_models()

    def load_models(self):
        for m in self.model_configs:
            name = m['name']
            device = m.get('device', 'cpu')
            try:
                model = whisper.load_model(name, device=device)
                self.models[name] = model
                print(f"Loaded model: {name} on {device}")
            except Exception as e:
                print(f"Failed to load model {name} on {device}: {e}")

    def get_model(self, name: str):
        return self.models.get(name)

    def list_models(self):
        return list(self.models.keys()) 
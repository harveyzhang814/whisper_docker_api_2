"""
This module defines the API endpoint for listing available transcription models.
It interacts with the ModelManager to provide model information to clients.
"""
from fastapi import APIRouter
from app.models.manager import ModelManager
from typing import Optional

router = APIRouter()

model_manager: Optional[ModelManager] = None

@router.get("/models")
def list_models():
    return model_manager.list_models() if model_manager else [] 
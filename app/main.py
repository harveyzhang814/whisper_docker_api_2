"""
This file initializes the FastAPI application, loads model configurations, and registers API routers.
It serves as the main entry point for the Whisper Docker API service.
"""
import os
from fastapi import FastAPI
from app.api import transcribe, models, health
from app.models.manager import ModelManager

# 加载配置
CONFIG_PATH = os.getenv("CONFIG_PATH", "config/config.yaml")
model_manager = ModelManager(CONFIG_PATH)

# 注入到各API模块
transcribe.model_manager = model_manager
models.model_manager = model_manager

app = FastAPI(title="Whisper Docker API")

app.include_router(transcribe.router)
app.include_router(models.router)
app.include_router(health.router) 
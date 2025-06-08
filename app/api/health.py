"""
This module provides a health check endpoint for the API service.
It is used to verify that the server is running and responsive.
"""
from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok"} 
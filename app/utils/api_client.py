"""
This module provides client utility functions for interacting with the Whisper transcription API.
It supports both standard HTTP and streaming WebSocket transcription with numpy audio input.

Provides standard and streaming transcription functions for numpy audio input.

Author: whisper_docker_api_2 contributors
Date: 2024-06-xx
"""

import requests
import numpy as np
import base64
import asyncio
import websockets
import json
from typing import Optional, Dict, Any, List, Generator, Union, Iterable
from app.utils.audio_utils import split_audio, audio_to_base64

HTTP_URL = "http://localhost:8000/transcribe"
WS_URL = "ws://localhost:8000/transcribe/stream"
SAMPLE_RATE = 16000


def standard_transcribe(
    audio: np.ndarray,
    model: str = "base",
    language: Optional[str] = None,
    output_format: str = "json",
    api_url: str = HTTP_URL,
    **kwargs
) -> Dict[str, Any]:
    """
    Transcribe audio using the standard HTTP API.

    Args:
        audio (np.ndarray): 1D float32 numpy array, 16kHz, mono.
        model (str): Model name (default: "base").
        language (Optional[str]): Language code (e.g., 'en', 'zh').
        output_format (str): Output format ('json', 'text', etc.).
        api_url (str): API endpoint URL.
        **kwargs: Additional parameters for the API.
    Returns:
        Dict[str, Any]: API response as a dict (parsed JSON or error info).
    Raises:
        requests.RequestException: If the HTTP request fails.
    """
    audio_b64 = audio_to_base64(audio)
    payload = {
        "audio_ndarray": audio_b64,
        "model": model,
        "output_format": output_format,
    }
    if language:
        payload["language"] = language
    payload.update(kwargs)
    resp = requests.post(api_url, data=payload)
    try:
        return resp.json()
    except Exception:
        return {"status": resp.status_code, "text": resp.text}


def stream_transcribe(
    audio: Union[np.ndarray, Iterable[np.ndarray]],
    model: str = "base",
    language: Optional[str] = None,
    chunk_seconds: int = 1,
    ws_url: str = WS_URL,
    **kwargs
) -> 'Generator[Dict[str, Any], None, None]':
    """
    Transcribe audio using the streaming WebSocket API (yields results in real time).
    Supports both full numpy array input and iterable/generator of audio chunks (e.g., microphone stream).

    Args:
        audio (Union[np.ndarray, Iterable[np.ndarray]]):
            - 1D float32 numpy array (16kHz, mono), or
            - Iterable/generator yielding 1D float32 numpy arrays (each chunk)
        model (str): Model name (default: "base").
        language (Optional[str]): Language code.
        chunk_seconds (int): Duration (seconds) of each audio chunk (only for np.ndarray input).
        ws_url (str): WebSocket endpoint URL.
        **kwargs: Additional parameters for the API.
    Yields:
        Dict[str, Any]: Server response for each chunk, as soon as it is received.
    """
    # Determine chunk source
    if isinstance(audio, np.ndarray):
        chunk_size = SAMPLE_RATE * chunk_seconds
        chunks = split_audio(audio, chunk_size)
    else:
        chunks = audio  # Assume iterable/generator of np.ndarray

    async def _stream():
        async with websockets.connect(ws_url) as ws:
            for chunk in chunks:
                audio_b64 = audio_to_base64(chunk)
                msg = {
                    "model": model,
                    "audio_ndarray": audio_b64,
                }
                if language:
                    msg["language"] = language
                msg.update(kwargs)
                await ws.send(json.dumps(msg))
                try:
                    response = await ws.recv()
                    resp_json = json.loads(response)
                    yield resp_json
                except Exception as e:
                    yield {"error": str(e)}

    # Run the async generator and yield results synchronously
    loop = asyncio.get_event_loop() if asyncio.get_event_loop().is_running() else asyncio.new_event_loop()
    try:
        gen = _stream()
        while True:
            result = loop.run_until_complete(gen.__anext__())
            yield result
    except StopAsyncIteration:
        pass 
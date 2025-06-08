"""
This module provides utility functions for decoding audio from files, base64 strings, numpy arrays, and URLs.
All decoded audio is converted to mono, 16kHz, float32 numpy arrays for downstream processing.

Author: whisper_docker_api_2 contributors
Date: 2024-06-xx
"""

import base64
import io
import numpy as np
from typing import Optional

from pydub import AudioSegment

def decode_audio_file(file) -> np.ndarray:
    """
    Decode an audio file-like object to a mono, 16kHz, float32 numpy array.

    Args:
        file: File-like object or file path (wav, mp3, etc.)
    Returns:
        np.ndarray: 1D float32 numpy array of audio samples, normalized to [-1, 1]
    """
    audio = AudioSegment.from_file(file)
    # Ensure mono and 16kHz
    audio = audio.set_frame_rate(16000).set_channels(1)
    # Convert to float32 numpy array, normalize to [-1, 1]
    samples = np.array(audio.get_array_of_samples()).astype(np.float32) / (2**15)
    return samples

def decode_audio_base64(b64str: str) -> np.ndarray:
    """
    Decode a base64-encoded audio file (wav/mp3) to a mono, 16kHz, float32 numpy array.

    Args:
        b64str (str): Base64-encoded audio file bytes
    Returns:
        np.ndarray: 1D float32 numpy array of audio samples
    """
    audio_bytes = base64.b64decode(b64str)
    return decode_audio_file(io.BytesIO(audio_bytes))

def decode_audio_ndarray(b64str: str) -> np.ndarray:
    """
    Decode a base64-encoded float32 numpy array (as bytes) to a numpy array.

    Args:
        b64str (str): Base64-encoded float32 numpy array bytes
    Returns:
        np.ndarray: 1D float32 numpy array of audio samples
    """
    arr_bytes = base64.b64decode(b64str)
    arr = np.frombuffer(arr_bytes, dtype=np.float32)
    return arr

def decode_audio_url(url: str) -> Optional[np.ndarray]:
    """
    Download and decode an audio file from a URL to a mono, 16kHz, float32 numpy array.

    Args:
        url (str): URL to the audio file
    Returns:
        Optional[np.ndarray]: 1D float32 numpy array of audio samples, or None if download fails
    """
    import requests
    resp = requests.get(url)
    if resp.status_code == 200:
        return decode_audio_file(io.BytesIO(resp.content))
    return None 
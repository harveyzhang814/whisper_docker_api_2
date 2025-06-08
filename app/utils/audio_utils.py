"""
This module provides utility functions for splitting audio numpy arrays into chunks and encoding them to base64 strings.
It is useful for streaming audio processing and WebSocket transmission.

Author: whisper_docker_api_2 contributors
Date: 2024-06-xx
"""

import numpy as np
import base64
from typing import List

def split_audio(audio: np.ndarray, chunk_size: int) -> List[np.ndarray]:
    """
    Split a numpy array of audio samples into fixed-size chunks.

    Args:
        audio (np.ndarray): The input audio samples (1D float32 array).
        chunk_size (int): Number of samples per chunk (e.g., 16000 for 1 second at 16kHz).

    Returns:
        List[np.ndarray]: List of audio chunks as numpy arrays. The last chunk may be shorter if the audio length is not a multiple of chunk_size.

    Example:
        >>> chunks = split_audio(audio, 16000)
        >>> for chunk in chunks:
        ...     process(chunk)
    """
    # Use list comprehension to generate chunks of the specified size
    return [audio[i:i+chunk_size] for i in range(0, len(audio), chunk_size)]


def audio_to_base64(audio: np.ndarray) -> str:
    """
    Encode a numpy array of audio samples to a base64 string (float32 little-endian bytes).

    Args:
        audio (np.ndarray): Audio samples as a 1D float32 numpy array.

    Returns:
        str: Base64-encoded string representing the audio bytes.

    Example:
        >>> b64 = audio_to_base64(chunk)
        >>> send_over_ws(b64)
    """
    # Ensure float32 type and encode to base64 string
    return base64.b64encode(audio.astype(np.float32).tobytes()).decode('utf-8') 
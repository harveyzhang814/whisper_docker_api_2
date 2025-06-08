"""
Test script for the /transcribe HTTP API endpoint using numpy ndarray input.

This script reads an audio file, converts it to a 16kHz mono float32 numpy array,
encodes it as base64, and sends it to the /transcribe endpoint as 'audio_ndarray'.
Prints the transcription result. Useful for verifying numpy-based input support.

Dependencies: requests, numpy, pydub

Author: whisper_docker_api_2 contributors
Date: 2024-06-xx
"""

import requests
import numpy as np
import base64
from pydub import AudioSegment
import io

API_URL = "http://localhost:8000/transcribe"
AUDIO_PATH = "sample/sample.wav"  # Path to your local audio file
MODEL = "base"  # Model name to use for transcription

# 1. Read audio and convert to 16kHz mono float32 numpy array
def audio_to_ndarray(path):
    """
    Load an audio file and convert it to a 16kHz mono float32 numpy array.

    Args:
        path (str): Path to the audio file.
    Returns:
        np.ndarray: 1D float32 numpy array of audio samples.
    """
    audio = AudioSegment.from_file(path)
    audio = audio.set_frame_rate(16000).set_channels(1)
    samples = np.array(audio.get_array_of_samples()).astype(np.float32) / (2**15)
    return samples

# 2. Convert numpy array to base64 string
def ndarray_to_base64(arr):
    """
    Encode a float32 numpy array as a base64 string.

    Args:
        arr (np.ndarray): 1D float32 numpy array.
    Returns:
        str: Base64-encoded string of the array bytes.
    """
    arr_bytes = arr.astype(np.float32).tobytes()
    return base64.b64encode(arr_bytes).decode('utf-8')

if __name__ == "__main__":
    # Convert audio file to base64-encoded numpy array string
    arr = audio_to_ndarray(AUDIO_PATH)
    arr_b64 = ndarray_to_base64(arr)
    data = {
        "audio_ndarray": arr_b64,
        "model": MODEL,
        "output_format": "json"
    }
    # Send POST request with numpy array data
    resp = requests.post(API_URL, data=data)
    print("Status:", resp.status_code)
    print("Response:", resp.text) 
"""
This test script verifies the streaming transcription API using WebSocket.
It sends audio chunks to the server and prints the received transcription results.

Streaming API test script for simulating real-time audio streaming.

This script reads a short audio file, repeats it to create a long audio stream, splits it into 1-second chunks,
and sends each chunk via WebSocket to the /transcribe/stream endpoint, simulating real-time audio input.
It prints the streaming transcription results and checks for errors.

Dependencies: websockets, numpy, scipy, app.utils.audio_utils

Author: whisper_docker_api_2 contributors
Date: 2024-06-xx
"""

import asyncio
import websockets
import json
import numpy as np
import time
from scipy.io import wavfile
from app.utils.audio_utils import split_audio, audio_to_base64

AUDIO_PATH = 'sample/sample.wav'
MODEL_NAME = 'small'  # Model name to use for transcription
LANGUAGE = 'en'
WS_URL = 'ws://localhost:8000/transcribe/stream'
REPEAT = 10  # Number of times to repeat the audio to simulate a long stream
CHUNK_SECONDS = 1  # Duration (seconds) of each audio chunk
SAMPLE_RATE = 16000


def load_and_extend_audio(path, repeat=10, target_sr=16000):
    """
    Load an audio file, convert to mono 16kHz float32, and repeat it to extend duration.

    Args:
        path (str): Path to the audio file.
        repeat (int): Number of times to repeat the audio.
        target_sr (int): Target sample rate (Hz).
    Returns:
        np.ndarray: Extended audio as 1D float32 numpy array.
    Raises:
        ValueError: If the audio sample rate does not match target_sr.
    """
    rate, data = wavfile.read(path)
    # Convert to float32 in range [-1, 1] if needed
    if data.dtype != np.float32:
        data = data.astype(np.float32) / np.iinfo(data.dtype).max
    # Convert to mono if stereo
    if len(data.shape) > 1:
        data = data.mean(axis=1)
    # Check sample rate
    if rate != target_sr:
        raise ValueError(f"Sample rate must be {target_sr}Hz, got {rate}Hz")
    # Repeat audio to extend duration
    data = np.tile(data, repeat)
    return data


async def stream_audio_chunks(chunks, ws_url, model, language, sleep_time=1):
    """
    Send audio chunks to the WebSocket streaming API and print transcription results.

    Args:
        chunks (List[np.ndarray]): List of audio chunks to send.
        ws_url (str): WebSocket URL of the streaming API.
        model (str): Model name for transcription.
        language (str): Language code.
        sleep_time (float): Seconds to wait between sending chunks (simulates real-time).
    """
    async with websockets.connect(ws_url) as ws:
        for idx, chunk in enumerate(chunks):
            audio_b64 = audio_to_base64(chunk)
            msg = {
                'model': model,
                'language': language,
                'audio_ndarray': audio_b64
            }
            await ws.send(json.dumps(msg))
            print(f"[SEND] Chunk {idx+1}/{len(chunks)} sent.")
            try:
                response = await ws.recv()
                resp_json = json.loads(response)
                if 'error' in resp_json:
                    print(f"[ERROR] {resp_json['error']}")
                else:
                    print(f"[RECV] text: {resp_json.get('text')}, is_final: {resp_json.get('is_final')}")
            except Exception as e:
                print(f"[EXCEPTION] {e}")
            # Simulate real-time streaming by waiting between chunks
            time.sleep(sleep_time)


def main():
    """
    Main entry point: loads and extends audio, splits into chunks, and streams to API.
    """
    audio = load_and_extend_audio(AUDIO_PATH, repeat=REPEAT, target_sr=SAMPLE_RATE)
    chunk_size = SAMPLE_RATE * CHUNK_SECONDS
    chunks = split_audio(audio, chunk_size)
    print(f"Total chunks: {len(chunks)}")
    asyncio.run(stream_audio_chunks(chunks, WS_URL, MODEL_NAME, LANGUAGE, sleep_time=1))


if __name__ == '__main__':
    main() 
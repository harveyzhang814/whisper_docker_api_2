"""
Test script for real-time microphone streaming with stream_transcribe.

This script captures audio from the microphone in real time, sends each chunk to the streaming API,
and prints each response as it arrives. At the end, it outputs the concatenated text.

Dependencies: sounddevice, numpy, app.utils.api_client, app.utils.audio

Author: whisper_docker_api_2 contributors
Date: 2024-06-xx
"""

import sounddevice as sd
import numpy as np
from app.utils.api_client import stream_transcribe

MODEL = 'base'
LANGUAGE = 'en'
SAMPLE_RATE = 16000
CHUNK_SECONDS = 3
CHUNK_SIZE = SAMPLE_RATE * CHUNK_SECONDS

def mic_stream(chunk_size=CHUNK_SIZE, samplerate=SAMPLE_RATE):
    """
    Generator that yields audio chunks from the microphone in real time.
    Args:
        chunk_size (int): Number of samples per chunk (e.g., 48000 for 3s at 16kHz).
        samplerate (int): Audio sample rate (Hz).
    Yields:
        np.ndarray: 1D float32 numpy array for each audio chunk.
    """
    print(f"[INFO] Opening microphone...")
    # Open the microphone input stream
    with sd.InputStream(samplerate=samplerate, channels=1, dtype='float32') as stream:
        print(f"[INFO] Microphone opened. Recording... Speak into the microphone (Ctrl+C to stop)")
        while True:
            # Read chunk_size samples from the stream
            audio_chunk = stream.read(chunk_size)[0].flatten()
            print(f"[INFO] Audio chunk captured ({len(audio_chunk)} samples)")
            # Yield the chunk as a 1D numpy array
            yield audio_chunk
    print(f"[INFO] Microphone closed.")

def test_mic_stream():
    """
    Test stream_transcribe with real-time microphone input.
    Captures audio, sends to API, prints each response, and concatenates final texts.
    """
    text_list = []  # List to collect all is_final text segments
    try:
        # Iterate over streaming transcription responses in real time
        for resp in stream_transcribe(mic_stream(), model=MODEL, language=LANGUAGE, chunk_seconds=CHUNK_SECONDS):
            print("Streaming API response:")
            print(resp)
            # If this chunk is a final result, append its text
            if resp.get('is_final') and resp.get('text'):
                text_list.append(resp['text'])
    except KeyboardInterrupt:
        # Allow user to stop recording with Ctrl+C
        print("\n[INFO] Recording stopped by user. Closing microphone...")
    # Concatenate all final texts into a single string
    full_text = ''.join(text_list)
    print("\nConcatenated text from all is_final results:")
    print(full_text)

if __name__ == '__main__':
    test_mic_stream() 
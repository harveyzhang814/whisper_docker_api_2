"""
Test script for real-time microphone streaming with stream_transcribe,
and save the recorded audio to a WAV file.

This script captures audio from the microphone in real time, sends each chunk to the streaming API,
prints each response, and finally saves the concatenated audio to sample/mic_recorded.wav.

Dependencies: sounddevice, numpy, scipy, app.utils.api_client

Author: whisper_docker_api_2 contributors
Date: 2024-06-xx
"""

import sounddevice as sd
import numpy as np
from scipy.io import wavfile
from app.utils.api_client import stream_transcribe
import os
import time

MODEL = 'base'
LANGUAGE = 'en'
SAMPLE_RATE = 16000
CHUNK_SECONDS = 3
CHUNK_SIZE = SAMPLE_RATE * CHUNK_SECONDS
OUTPUT_PATH = 'sample/mic_recorded.wav'

def test_mic_stream_and_save():
    """
    Test stream_transcribe with real-time microphone input,
    and save the recorded audio to a WAV file.
    Automatically stops after 15 seconds.
    """
    text_list = []  # List to collect all is_final text segments
    audio_chunks = []  # List to collect all audio chunks
    RECORD_SECONDS = 15
    print(f"\n--- Testing stream_transcribe (real-time mic input, will save audio, auto-stop after {RECORD_SECONDS}s) ---")
    try:
        def mic_gen():
            print(f"[INFO] Opening microphone...")
            with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, dtype='float32') as stream:
                print(f"[INFO] Microphone opened. Recording... Speak into the microphone...")
                start_time = time.time()
                while True:
                    audio_chunk = stream.read(CHUNK_SIZE)[0].flatten()
                    print(f"[INFO] Audio chunk captured ({len(audio_chunk)} samples)")
                    audio_chunks.append(audio_chunk.copy())
                    yield audio_chunk
                    # Check if time is up
                    if time.time() - start_time >= RECORD_SECONDS:
                        print(f"[INFO] {RECORD_SECONDS} seconds reached. Stopping recording...")
                        break
            print(f"[INFO] Microphone closed.")
        for resp in stream_transcribe(mic_gen(), model=MODEL, language=LANGUAGE, chunk_seconds=CHUNK_SECONDS):
            print("Streaming API response:")
            print(resp)
            if resp.get('is_final') and resp.get('text'):
                text_list.append(resp['text'])
    except KeyboardInterrupt:
        print("\n[INFO] Recording stopped by user. Closing microphone...")

    # Concatenate all audio chunks into a single numpy array
    if audio_chunks:
        audio_data = np.concatenate(audio_chunks)
        # Ensure output directory exists
        os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
        # Convert float32 [-1, 1] to int16 for WAV
        audio_int16 = np.clip(audio_data, -1, 1)
        audio_int16 = (audio_int16 * 32767).astype(np.int16)
        wavfile.write(OUTPUT_PATH, SAMPLE_RATE, audio_int16)
        print(f"[INFO] Saved recorded audio to {OUTPUT_PATH}")
    else:
        print("[WARN] No audio data recorded.")

    # Concatenate all final texts into a single string
    full_text = ''.join(text_list)
    print("\nConcatenated text from all is_final results:")
    print(full_text)

if __name__ == '__main__':
    test_mic_stream_and_save() 
"""
This test script verifies the file-based transcription API.
It uploads audio files to the server and checks the returned transcription results.

Dependencies: requests

Author: whisper_docker_api_2 contributors
Date: 2024-06-xx
"""

import requests

API_URL = "http://localhost:8000/transcribe"
AUDIO_PATH = "sample/sample.wav"  # Path to your local audio file
MODEL = "small"  # Model name to use for transcription

if __name__ == "__main__":
    # Open the audio file in binary mode
    with open(AUDIO_PATH, "rb") as f:
        files = {"audio_file": (AUDIO_PATH, f, "audio/wav")}
        data = {
            "model": MODEL,
            "output_format": "json"
        }
        # Send POST request with file and parameters
        resp = requests.post(API_URL, files=files, data=data)
        print("Status:", resp.status_code)
        print("Response:", resp.text) 
"""
This test script verifies the standard HTTP transcription client utility.
It sends numpy audio arrays to the API and checks the returned results.

Dependencies: numpy, scipy, app.utils.api_client, app.utils.audio

Author: whisper_docker_api_2 contributors
Date: 2024-06-xx
"""

from app.utils.audio import decode_audio_file
from app.utils.api_client import standard_transcribe

AUDIO_PATH = 'sample/sample.wav'
MODEL = 'base'  # or 'small', etc.
LANGUAGE = 'en'


def test_standard():
    """Test standard_transcribe API client utility."""
    audio = decode_audio_file(AUDIO_PATH)
    print("\n--- Testing standard_transcribe ---")
    resp = standard_transcribe(audio, model=MODEL, language=LANGUAGE)
    print("Standard API response:")
    print(resp)

if __name__ == '__main__':
    test_standard() 
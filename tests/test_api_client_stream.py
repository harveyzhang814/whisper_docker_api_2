"""
This test script verifies the streaming WebSocket transcription client utility.
It streams numpy audio arrays to the API and checks the returned results.

Dependencies: numpy, scipy, app.utils.api_client, app.utils.audio

Author: whisper_docker_api_2 contributors
Date: 2024-06-xx
"""

from app.utils.audio import decode_audio_file
from app.utils.api_client import stream_transcribe

AUDIO_PATH = 'sample/sample.wav'
MODEL = 'base'  # or 'small', etc.
LANGUAGE = 'en'


def test_stream():
    """Test stream_transcribe API client utility with real-time output and text concatenation (efficient list join)."""
    audio = decode_audio_file(AUDIO_PATH)
    print("\n--- Testing stream_transcribe (real-time output) ---")
    text_list = []
    for resp in stream_transcribe(audio, model=MODEL, language=LANGUAGE, chunk_seconds=3):
        print("Streaming API response:")
        print(resp)
        if resp.get('is_final') and resp.get('text'):
            text_list.append(resp['text'])
    full_text = ''.join(text_list)
    print("\nConcatenated text from all is_final results:")
    print(full_text)

if __name__ == '__main__':
    test_stream() 
import base64
import io
import numpy as np
from typing import Optional

from pydub import AudioSegment

def decode_audio_file(file) -> np.ndarray:
    audio = AudioSegment.from_file(file)
    audio = audio.set_frame_rate(16000).set_channels(1)
    samples = np.array(audio.get_array_of_samples()).astype(np.float32) / (2**15)
    return samples

def decode_audio_base64(b64str: str) -> np.ndarray:
    audio_bytes = base64.b64decode(b64str)
    return decode_audio_file(io.BytesIO(audio_bytes))

def decode_audio_ndarray(b64str: str) -> np.ndarray:
    arr_bytes = base64.b64decode(b64str)
    arr = np.frombuffer(arr_bytes, dtype=np.float32)
    return arr

def decode_audio_url(url: str) -> Optional[np.ndarray]:
    import requests
    resp = requests.get(url)
    if resp.status_code == 200:
        return decode_audio_file(io.BytesIO(resp.content))
    return None 
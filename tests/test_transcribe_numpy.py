import requests
import numpy as np
import base64
from pydub import AudioSegment
import io

API_URL = "http://localhost:8000/transcribe"
AUDIO_PATH = "sample/sample.wav"  # 指向 sample 文件夹下的音频文件
MODEL = "base"

# 1. 读取音频并转为16kHz单声道float32 numpy数组
def audio_to_ndarray(path):
    audio = AudioSegment.from_file(path)
    audio = audio.set_frame_rate(16000).set_channels(1)
    samples = np.array(audio.get_array_of_samples()).astype(np.float32) / (2**15)
    return samples

# 2. numpy数组转base64
def ndarray_to_base64(arr):
    arr_bytes = arr.astype(np.float32).tobytes()
    return base64.b64encode(arr_bytes).decode('utf-8')

if __name__ == "__main__":
    arr = audio_to_ndarray(AUDIO_PATH)
    arr_b64 = ndarray_to_base64(arr)
    data = {
        "audio_ndarray": arr_b64,
        "model": MODEL,
        "output_format": "json"
    }
    resp = requests.post(API_URL, data=data)
    print("Status:", resp.status_code)
    print("Response:", resp.text) 
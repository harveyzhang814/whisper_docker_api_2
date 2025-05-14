import requests

API_URL = "http://localhost:8000/transcribe"
AUDIO_PATH = "sample/sample.wav"  # 替换为你的本地音频文件路径
MODEL = "small"

if __name__ == "__main__":
    with open(AUDIO_PATH, "rb") as f:
        files = {"audio_file": (AUDIO_PATH, f, "audio/wav")}
        data = {
            "model": MODEL,
            "output_format": "json"
        }
        resp = requests.post(API_URL, files=files, data=data)
        print("Status:", resp.status_code)
        print("Response:", resp.text) 
import asyncio
import websockets
import json
import numpy as np
import time
from scipy.io import wavfile
from app.utils.audio_utils import split_audio, audio_to_base64

AUDIO_PATH = 'sample/sample.wav'
MODEL_NAME = 'small'  # TODO: 替换为实际模型名
LANGUAGE = 'en'
WS_URL = 'ws://localhost:8000/transcribe/stream'
REPEAT = 10  # 拼接倍数
CHUNK_SECONDS = 1  # 每片时长（秒）
SAMPLE_RATE = 16000


def load_and_extend_audio(path, repeat=10, target_sr=16000):
    rate, data = wavfile.read(path)
    # 转 float32
    if data.dtype != np.float32:
        data = data.astype(np.float32) / np.iinfo(data.dtype).max
    # 转单通道
    if len(data.shape) > 1:
        data = data.mean(axis=1)
    # 重采样（如有必要）
    if rate != target_sr:
        raise ValueError(f"Sample rate must be {target_sr}Hz, got {rate}Hz")
    # 拼接
    data = np.tile(data, repeat)
    return data


async def stream_audio_chunks(chunks, ws_url, model, language, sleep_time=1):
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
            time.sleep(sleep_time)


def main():
    audio = load_and_extend_audio(AUDIO_PATH, repeat=REPEAT, target_sr=SAMPLE_RATE)
    chunk_size = SAMPLE_RATE * CHUNK_SECONDS
    chunks = split_audio(audio, chunk_size)
    print(f"Total chunks: {len(chunks)}")
    asyncio.run(stream_audio_chunks(chunks, WS_URL, MODEL_NAME, LANGUAGE, sleep_time=1))


if __name__ == '__main__':
    main() 
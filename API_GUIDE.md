# API Guide

## Introduction
This project provides a FastAPI-based service for audio transcription using various models. It supports both HTTP and WebSocket interfaces for synchronous and streaming transcription.

## Base Information
- **Base URL:** `http://<host>:<port>` (default port: 8000)
- **No authentication required by default**
- **Content-Type:** `multipart/form-data` for file uploads, `application/json` for WebSocket

---

## API Endpoints

### 1. `/transcribe` (POST)
Transcribe an audio file or audio data using a specified model.

#### **Request**
- **Method:** POST
- **Path:** `/transcribe`
- **Content-Type:** `multipart/form-data`

#### **Parameters**
| Name           | Type         | Required | Description                                 |
|----------------|--------------|----------|---------------------------------------------|
| audio_file     | file         | No       | Audio file to upload                        |
| audio_url      | string       | No       | URL to download audio file                  |
| audio_base64   | string       | No       | Base64-encoded audio data                   |
| audio_ndarray  | string       | No       | Numpy ndarray (as string, base64-encoded)   |
| model          | string       | Yes      | Model name to use for transcription         |
| language       | string       | No       | Language code (e.g., 'en', 'zh')            |
| output_format  | string       | No       | 'json', 'text', or 'json_metadata' (default: 'json') |
| stream         | bool         | No       | Whether to use streaming (default: False)   |

> **Note:** At least one of `audio_file`, `audio_url`, `audio_base64`, or `audio_ndarray` must be provided.

#### **Request Example (curl)**
```bash
curl -X POST "http://localhost:8000/transcribe" \
  -F "audio_file=@sample/test.wav" \
  -F "model=your_model_name" \
  -F "language=en" \
  -F "output_format=json"
```

#### **Response Example**
```json
{
  "text": "Transcribed text here.",
  "language": "en",
  "model": "your_model_name"
}
```

- If `output_format=text`, response is plain text.
- If `output_format=json_metadata`, response includes all model metadata.

#### **Error Example**
```json
{
  "error": "No valid audio input provided."
}
```

---

### 2. `/transcribe/stream` (WebSocket)
Stream audio data and receive transcription results in real time.

#### **Connection**
- **URL:** `ws://<host>:<port>/transcribe/stream`

#### **Message Format**
- **Client → Server:**
```json
{
  "model": "your_model_name",
  "language": "en",
  "audio_ndarray": "<base64-encoded float32 numpy array>"
}
```
> **Note:** `audio_ndarray` must be a base64-encoded byte stream of a float32 numpy array. Directly sending base64-encoded audio files (e.g., wav/mp3) or other formats is **not supported**. The backend expects a mono (single channel), 16kHz, float32 numpy array.

- **Server → Client:**
```json
{
  "text": "Partial or final transcription text.",
  "is_final": true,
  "metadata": { ... },
  "model": "your_model_name"
}
```

#### **How to Prepare Data for audio_ndarray**

##### 1. From an audio file (e.g., wav)
```python
import numpy as np
import base64
from scipy.io import wavfile

rate, data = wavfile.read("your_audio.wav")
if data.dtype != np.float32:
    data = data.astype(np.float32) / np.iinfo(data.dtype).max
# If stereo, convert to mono
if len(data.shape) > 1:
    data = data.mean(axis=1)
audio_ndarray_b64 = base64.b64encode(data.tobytes()).decode("utf-8")
```

##### 2. From microphone (streaming)
```python
import sounddevice as sd
import numpy as np
import base64

# Example callback for streaming

def callback(indata, frames, time, status):
    mono = indata.mean(axis=1) if indata.shape[1] > 1 else indata[:,0]
    audio_b64 = base64.b64encode(mono.astype(np.float32).tobytes()).decode("utf-8")
    # Send audio_b64 via WebSocket

with sd.InputStream(callback=callback, channels=1, samplerate=16000, dtype='float32'):
    ... # Run your event loop
```

#### **Cross-Project Usage Example**
```python
import asyncio
import websockets
import json

async def transcribe_stream(audio_ndarray_b64):
    uri = "ws://localhost:8000/transcribe/stream"
    async with websockets.connect(uri) as ws:
        await ws.send(json.dumps({
            "model": "your_model_name",
            "language": "en",
            "audio_ndarray": audio_ndarray_b64
        }))
        while True:
            response = await ws.recv()
            print(response)

# audio_ndarray_b64: see data preparation above
# asyncio.run(transcribe_stream(audio_ndarray_b64))
```

#### **Common Errors**
- If `audio_ndarray` is not a base64-encoded float32 numpy byte stream, the API will return an error or invalid result.
- Example error:
  ```json
  {"error": "cannot reshape array of size ..."}
  ```

---

## Error Codes & Exceptions
| Error Message                        | HTTP Status | Description                        |
|--------------------------------------|-------------|------------------------------------|
| No valid audio input provided.       | 400         | No audio data was sent             |
| Model '<model>' not loaded.          | 404         | The specified model is not loaded  |

WebSocket errors are sent as JSON messages with an `error` field.

---

## FAQ & Notes
- **Q: Can I send a base64-encoded wav/mp3 file directly?**
  - A: No. You must decode the audio to a float32 numpy array, then base64 encode the bytes.
- **Q: Does it support multi-channel audio?**
  - A: Please convert to mono before sending.
- **Q: What sample rate should I use?**
  - A: 16kHz is recommended for best compatibility.
- Supported audio formats depend on the backend model.
- For best results, use clear audio and specify the correct language.
- If you need to load a new model, ensure it is available in the backend.

---

## Contact & Links
- For more information, see the project README or contact the maintainer.

---

## Python Client Utilities

This project provides convenient Python utility functions for calling the transcription APIs directly with numpy audio arrays. These are located in `app/utils/api_client.py`.

### 1. `standard_transcribe`
Transcribe audio using the standard HTTP API (`/transcribe`).

**Function Signature:**
```python
from app.utils.api_client import standard_transcribe
result = standard_transcribe(audio, model="base", language=None, output_format="json", **kwargs)
```

**Parameters:**
- `audio` (`np.ndarray`, required): 1D float32 numpy array, 16kHz, mono.
- `model` (`str`, optional): Model name (default: "base").
- `language` (`str`, optional): Language code (e.g., 'en', 'zh').
- `output_format` (`str`, optional): Output format ('json', 'text', etc.).
- `**kwargs`: Any additional parameters supported by the API.

**Returns:**
- `dict`: API response (parsed JSON or error info).

**Example:**
```python
import numpy as np
from app.utils.api_client import standard_transcribe
# audio: your 16kHz mono float32 numpy array
data = standard_transcribe(audio, model="small", language="en")
print(data)
```

---

### 2. `stream_transcribe`
Transcribe audio using the streaming WebSocket API (`/transcribe/stream`).

**Function Signature:**
```python
from app.utils.api_client import stream_transcribe
results = stream_transcribe(audio, model="base", language=None, chunk_seconds=1, **kwargs)
```

**Parameters:**
- `audio` (`np.ndarray`, required): 1D float32 numpy array, 16kHz, mono.
- `model` (`str`, optional): Model name (default: "base").
- `language` (`str`, optional): Language code.
- `chunk_seconds` (`int`, optional): Duration (seconds) of each audio chunk (default: 1).
- `**kwargs`: Any additional parameters supported by the API.

**Returns:**
- `List[dict]`: List of server responses for each chunk.

**Example:**
```python
import numpy as np
from app.utils.api_client import stream_transcribe
# audio: your 16kHz mono float32 numpy array
results = stream_transcribe(audio, model="small", language="en", chunk_seconds=1)
for resp in results:
    print(resp)
```

---

**Notes:**
- Both functions require the input audio to be a 16kHz, mono, float32 numpy array. Use the provided audio utilities to convert files if needed.
- `stream_transcribe` splits the audio and sends each chunk sequentially, simulating real-time streaming.
- You can pass any additional API parameters as keyword arguments.
- See `app/utils/api_client.py` for full details and docstrings. 
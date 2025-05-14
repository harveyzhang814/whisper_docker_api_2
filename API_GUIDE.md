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
  "audio_ndarray": "<base64-encoded ndarray>"
}
```

- **Server → Client:**
```json
{
  "text": "Partial or final transcription text.",
  "is_final": true,
  "metadata": { ... },
  "model": "your_model_name"
}
```

#### **Python Example (websockets)**
```python
import asyncio
import websockets
import json

async def transcribe_stream():
    uri = "ws://localhost:8000/transcribe/stream"
    async with websockets.connect(uri) as ws:
        await ws.send(json.dumps({
            "model": "your_model_name",
            "language": "en",
            "audio_ndarray": "<base64-encoded ndarray>"
        }))
        response = await ws.recv()
        print(response)

asyncio.run(transcribe_stream())
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
- Supported audio formats depend on the backend model.
- For best results, use clear audio and specify the correct language.
- If you need to load a new model, ensure it is available in the backend.

---

## Contact & Links
- For more information, see the project README or contact the maintainer. 
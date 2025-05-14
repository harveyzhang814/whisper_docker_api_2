# Whisper Docker API – API Reference

## Overview
This document describes the RESTful and streaming API endpoints for the Whisper Docker API service. The service supports multiple Whisper models, various input/output formats, and both synchronous and streaming transcription.

---

## Base URL
```
http(s)://<your-domain>:<port>/
```

---

## Endpoints

### 1. Transcription (Synchronous)
#### `POST /transcribe`
Transcribe audio using a specified Whisper model.

**Request Parameters:**
- `audio_file` (file, optional): Audio file upload (wav, mp3, flac, etc.)
- `audio_url` (string, optional): URL to an audio file
- `audio_base64` (string, optional): Base64-encoded audio file
- `audio_ndarray` (string, optional): Base64-encoded numpy.ndarray (float32 PCM, mono, 16kHz)
- `model` (string, required): Model name (e.g., base, small, medium, large)
- `language` (string, optional): Language code (default: auto-detect)
- `output_format` (string, optional): `text` | `json` | `json_metadata` | `stream` (default: json)
- `stream` (bool, optional): If true, enables streaming output (default: false)

**Response:**
- `text/plain`: Transcribed text
- `application/json`: `{ "text": ..., "segments": [...], "language": ..., ... }`
- `application/json_metadata`: JSON with detailed metadata
- `text/event-stream` or WebSocket: Streaming output (see below)

**Example (cURL):**
```bash
curl -X POST "http://whisper.local:8000/transcribe" \
  -F "audio_file=@test.wav" \
  -F "model=base" \
  -F "output_format=json"
```

---

### 2. Transcription (Streaming)
#### `WebSocket /transcribe/stream`
Real-time transcription via WebSocket. Send audio chunks (PCM, base64, or ndarray) and receive transcribed text segments as they are recognized.

**Protocol:**
- Client sends audio data in binary or base64-encoded JSON messages.
- Server responds with JSON messages containing partial/final transcription results.

**Request Message Example:**
```json
{
  "audio_ndarray": "<base64-encoded ndarray chunk>",
  "model": "small",
  "language": "en"
}
```

**Response Message Example:**
```json
{
  "text": "Hello world",
  "segment": 1,
  "is_final": true,
  "metadata": { ... }
}
```

#### `HTTP Chunked /transcribe/stream`
- POST or PUT with chunked transfer encoding.
- Server streams back transcription results as chunks.

---

### 3. List Available Models
#### `GET /models`
Returns a list of currently loaded Whisper models.

**Response:**
```json
["base", "small", "medium"]
```

---

### 4. Health Check
#### `GET /health`
Returns service health status.

**Response:**
```json
{"status": "ok"}
```

---

## Error Codes
- `400 Bad Request`: Invalid input, missing parameters, or unsupported format
- `404 Not Found`: Model not found
- `413 Payload Too Large`: Audio file too large
- `500 Internal Server Error`: Server error or model failure

**Error Response Example:**
```json
{
  "error": "Model 'large' not loaded."
}
```

---

## Notes
- All endpoints support CORS.
- For streaming, ensure client and server use compatible protocols (WebSocket or HTTP chunked).
- `audio_ndarray` must be float32, mono, 16kHz, base64-encoded.
- Model selection is required for each request; only configured models are available.
- For best performance, use GPU and allocate sufficient resources for multiple models.

---

## Contact
For questions or support, please refer to the project repository or open an issue. 
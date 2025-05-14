from fastapi import APIRouter, File, UploadFile, Form, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import StreamingResponse, JSONResponse, PlainTextResponse
from typing import Optional
import numpy as np
import base64

from app.models.manager import ModelManager
from app.utils.audio import decode_audio_file, decode_audio_base64, decode_audio_ndarray, decode_audio_url

router = APIRouter()

# 假设全局有 model_manager 实例
model_manager: Optional[ModelManager] = None

def get_audio_array(audio_file, audio_url, audio_base64, audio_ndarray):
    if audio_file:
        return decode_audio_file(audio_file.file)
    if audio_url:
        return decode_audio_url(audio_url)
    if audio_base64:
        return decode_audio_base64(audio_base64)
    if audio_ndarray:
        return decode_audio_ndarray(audio_ndarray)
    return None

@router.post("/transcribe")
async def transcribe(
    audio_file: Optional[UploadFile] = File(None),
    audio_url: Optional[str] = Form(None),
    audio_base64: Optional[str] = Form(None),
    audio_ndarray: Optional[str] = Form(None),
    model: str = Form(...),
    language: Optional[str] = Form(None),
    output_format: Optional[str] = Form("json"),
    stream: Optional[bool] = Form(False)
):
    arr = get_audio_array(audio_file, audio_url, audio_base64, audio_ndarray)
    if arr is None:
        return JSONResponse({"error": "No valid audio input provided."}, status_code=400)
    m = model_manager.get_model(model)
    if m is None:
        return JSONResponse({"error": f"Model '{model}' not loaded."}, status_code=404)
    result = m.transcribe(arr, language=language)
    actual_model = model  # 实际执行的模型名
    if output_format == "text":
        return PlainTextResponse(result["text"])
    elif output_format == "json_metadata":
        result_with_model = dict(result)
        result_with_model["model"] = actual_model
        return JSONResponse(result_with_model)
    else:
        return JSONResponse({"text": result["text"], "language": result["language"], "model": actual_model})

# WebSocket流式接口
@router.websocket("/transcribe/stream")
async def transcribe_stream(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            data = await ws.receive_json()
            model = data.get("model")
            language = data.get("language")
            audio_ndarray = data.get("audio_ndarray")
            arr = decode_audio_ndarray(audio_ndarray)
            m = model_manager.get_model(model)
            if m is None:
                await ws.send_json({"error": f"Model '{model}' not loaded."})
                continue
            # 这里假设每次推理一小段
            result = m.transcribe(arr, language=language)
            await ws.send_json({
                "text": result["text"],
                "is_final": True,
                "metadata": result,
                "model": model  # 实际执行的模型名
            })
    except WebSocketDisconnect:
        pass 
# Whisper Docker API

## 项目简介

本项目基于 OpenAI Whisper，提供高性能、可扩展的语音识别 API 服务，支持多模型并行部署，支持多种输入输出格式，并可通过 Docker Compose 快速部署。

## 功能说明
- 支持通过 FastAPI 提供 RESTful API 服务
- 支持同时部署多个 Whisper 模型，API 可指定模型进行处理
- 支持多语言识别和自动语言检测
- 支持多种输入方式：文件上传、base64、URL、音频流（WebSocket/HTTP chunked）、numpy.ndarray
- 支持多种输出格式：纯文本、JSON、带 metadata 的 JSON、大文本、流式输出（SSE/WebSocket）
- 支持流式输入和输出，适合大文件和实时语音识别场景
- 可通过 Docker Compose 一键部署
- 所有配置项（如模型、API 域名、端口等）均通过配置文件集中管理

## 主要技术栈
- Python 3.9+
- FastAPI
- OpenAI Whisper (openai/whisper)
- Docker & Docker Compose
- Uvicorn
- numpy

## 快速开始

### 1. 克隆项目
```bash
git clone <your-repo-url>
cd whisper_docker_api_2
```

### 2. 编辑配置文件
在 `config/config.yaml` 中配置要加载的模型、API 域名、端口等参数。例如：
```yaml
# config/config.yaml
api:
  host: 0.0.0.0
  port: 8000
  root_path: /
  domain: whisper.local
models:
  - name: base
  - name: small
```

### 3. 使用 Docker Compose 部署
```bash
docker-compose up -d
```

### 4. 访问 API 文档
访问 http://<your-domain>:<port>/docs 查看交互式 API 文档。

## 配置文件说明
所有服务参数均在 `config/config.yaml` 中集中管理，包括：
- API 域名、端口、根路径
- 部署的 Whisper 模型列表
- 其他高级参数（如并发数、日志等级等，视实现而定）

可通过挂载自定义配置文件实现灵活部署：
```yaml
# docker-compose.yml 片段
services:
  whisper-api:
    image: whisper-api:latest
    volumes:
      - ./config/config.yaml:/app/config/config.yaml
    ports:
      - "8000:8000"
    environment:
      - ENV=prod
```

## API 说明

### 1. 语音转写接口
#### POST `/transcribe`
- **参数**：
  - `audio_file`：音频文件上传（支持 wav/mp3/flac 等）
  - `audio_url`：音频文件 URL
  - `audio_base64`：base64 编码音频
  - `audio_ndarray`：base64 编码的 numpy.ndarray（float32 PCM，单声道，采样率 16kHz）
  - `model`：指定使用的模型（如 base、small、medium、large）
  - `language`：指定识别语言（可选，默认自动检测）
  - `output_format`：输出格式（text/json/json_metadata/stream）
  - `stream`：是否流式输出（true/false）

- **返回**：
  - 纯文本
  - JSON（含转写文本和 metadata）
  - 流式输出（SSE/WebSocket）

#### 示例请求
```bash
curl -X POST "http://whisper.local:8000/transcribe" \
  -F "audio_file=@test.wav" \
  -F "model=base" \
  -F "output_format=json"
```

### 2. 流式转写接口
#### WebSocket `/transcribe/stream`
- 支持音频流（如分片 PCM、base64、numpy.ndarray）实时发送
- 支持流式返回转写结果

#### HTTP Chunked `/transcribe/stream`
- 支持 HTTP chunked 方式流式输入输出

### 3. 其他接口
- `/models`：获取当前可用模型列表
- `/health`：健康检查

## 目录结构
```
whisper_docker_api_2/
├── app/            # FastAPI 主应用
├── models/         # Whisper 模型加载与管理
├── api/            # API 路由
├── utils/          # 工具函数
├── config/         # 配置文件目录
│   └── config.yaml # 主配置文件
├── tests/          # 测试脚本
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
├── CHANGELOG.md
```

## 注意事项
- 多模型部署会占用较多显存和内存，建议根据硬件资源合理配置
- numpy.ndarray 输入需为 float32 单声道 PCM，采样率 16kHz，建议通过 base64 编码传输
- 流式输入输出需遵循接口协议（详见 API 文档）
- 推荐使用 GPU 部署以获得最佳性能
- 所有服务参数均通过 config/config.yaml 管理，修改后需重启服务生效

## License
MIT
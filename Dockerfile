FROM python:3.9-slim

# 安装系统依赖
RUN apt-get update && \
    apt-get install -y ffmpeg git && \
    rm -rf /var/lib/apt/lists/*

# 安装Python依赖
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目代码
COPY . /app
WORKDIR /app

# 设置环境变量
ENV PYTHONUNBUFFERED=1

# 启动FastAPI服务
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 
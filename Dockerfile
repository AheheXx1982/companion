FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl bzip2 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 下载 Sherpa-ONNX 中文 TTS 模型
RUN mkdir -p tts_model && \
    curl -L -o /tmp/model.tar.bz2 "https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-zh-hf-echo.tar.bz2" && \
    tar xf /tmp/model.tar.bz2 -C tts_model/ && \
    rm /tmp/model.tar.bz2

COPY . .

EXPOSE 8000

CMD ["python", "main.py"]

"""
SilentX AI Companion — FastAPI Backend
嵌入 silentxx.com 的期权知识问答助手
"""
import os
import json
import io
import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, Response
from pydantic import BaseModel
from typing import Optional

from wiki_loader import load_all_pages, search_pages, build_prompt, WIKI_ROOT

load_dotenv()

app = FastAPI(title="SilentX AI Companion", version="0.1.0")

# CORS - 支持 silentxx.com 及 www 子域名
origins = os.getenv("CORS_ORIGIN", "http://localhost:4321").split(",")
# 始终允许 silentxx.com 的两个变体
cors_origins = set(o.strip() for o in origins)
cors_origins.update({"https://silentxx.com", "https://www.silentxx.com"})
app.add_middleware(
    CORSMiddleware,
    allow_origins=list(cors_origins),
    allow_methods=["POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)

# LLM Config
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "deepseek")  # deepseek | openrouter

if LLM_PROVIDER == "openrouter":
    API_KEY = os.getenv("OPENROUTER_API_KEY", "")
    API_URL = "https://openrouter.ai/api/v1/chat/completions"
    MODEL = os.getenv("OPENROUTER_MODEL", "deepseek/deepseek-chat")
    HEADERS = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://silentxx.com",
        "X-Title": "SilentX AI Companion",
    }
else:
    API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
    API_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1") + "/chat/completions"
    MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-v4-pro")
    HEADERS = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

# 启动时加载 Wiki
print(f"Loading Wiki from {WIKI_ROOT}...")
ALL_PAGES = load_all_pages()
print(f"Loaded {len(ALL_PAGES)} Wiki pages.")


class ChatRequest(BaseModel):
    message: str
    history: Optional[list[dict]] = None  # [{"role": "user/assistant", "content": "..."}]


@app.get("/")
def root():
    return {
        "name": "SilentX AI Companion",
        "version": "0.1.0",
        "wiki_pages": len(ALL_PAGES),
        "llm_provider": LLM_PROVIDER,
        "model": MODEL,
    }


@app.get("/health")
def health():
    return {"status": "ok", "wiki_loaded": len(ALL_PAGES) > 0}


@app.post("/api/chat")
async def chat(req: ChatRequest):
    if not API_KEY:
        raise HTTPException(status_code=500, detail="LLM API key not configured")
    
    question = req.message.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Empty message")
    
    # 1. 检索 Wiki
    results = search_pages(question, ALL_PAGES, top_k=5)
    
    # 2. 组装 Prompt
    pages_only = [p for p, _ in results]
    messages = build_prompt(question, pages_only, req.history)
    
    # 3. 调用 LLM 流式返回
    async def stream_response():
        async with httpx.AsyncClient(timeout=60.0) as client:
            async with client.stream(
                "POST",
                API_URL,
                headers=HEADERS,
                json={
                    "model": MODEL,
                    "messages": messages,
                    "stream": True,
                    "temperature": 0.7,
                    "max_tokens": 1024,
                },
            ) as response:
                if response.status_code != 200:
                    error_body = await response.aread()
                    yield f"data: {json.dumps({'error': f'LLM API error: {response.status_code}'})}\n\n"
                    return
                
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data = line[6:]
                        if data == "[DONE]":
                            yield "data: [DONE]\n\n"
                            break
                        try:
                            chunk = json.loads(data)
                            delta = chunk.get("choices", [{}])[0].get("delta", {})
                            content = delta.get("content", "")
                            if content:
                                yield f"data: {json.dumps({'content': content})}\n\n"
                        except json.JSONDecodeError:
                            continue
    
    return StreamingResponse(
        stream_response(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


# ── TTS 语音合成 ────────────────────────────────────────────
TTS_VOICE = os.getenv("TTS_VOICE", "zh-CN-XiaoxiaoNeural")  # 微软免费中文女声


@app.post("/api/tts")
async def text_to_speech(req: ChatRequest):
    """文本转语音，返回 MP3 音频"""
    text = req.message.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Empty text")

    # 限制长度，避免滥用
    text = text[:1000]

    try:
        import edge_tts

        buf = io.BytesIO()
        communicate = edge_tts.Communicate(text, TTS_VOICE)
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                buf.write(chunk["data"])

        buf.seek(0)
        return Response(
            content=buf.read(),
            media_type="audio/mpeg",
            headers={"Content-Disposition": "inline"},
        )
    except ImportError:
        raise HTTPException(status_code=500, detail="edge-tts not installed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS error: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)

"""
SilentX AI Companion — FastAPI Backend
嵌入 silentxx.com 的期权知识问答助手
"""
import os
import json
import io
import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, Response
from pydantic import BaseModel
from typing import Optional

from wiki_loader import load_all_pages, search_pages, build_prompt, WIKI_ROOT
from memory_manager import get_memory_context, update_memory

load_dotenv()

app = FastAPI(title="SilentX AI Companion", version="0.1.0")

# CORS - 支持 silentxx.com 主站 + wenxin 子站
origins = os.getenv("CORS_ORIGIN", "http://localhost:4321").split(",")
# 始终允许 silentxx.com 主站两个变体 + wenxin 子站
cors_origins = set(o.strip() for o in origins)
cors_origins.update({"https://silentxx.com", "https://www.silentxx.com", "https://wenxin.silentxx.com"})
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
    persona: str = "silentxx"  # silentxx=期权助手(默认) | wenxin=问心剑(问心站)


class VisionRequest(BaseModel):
    image: str          # base64 编码的图片
    prompt: str = "请描述这张图片的内容"


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


class SearchRequest(BaseModel):
    q: str = ""
    top_k: int = 5


@app.get("/api/search")
def search(req: SearchRequest = None, q: str = "", top_k: int = 5):
    """传统搜索接口：关键词 → 匹配文章列表（标题/摘要/标签/链接）"""
    query = (req.q if req else "") or q
    query = query.strip()
    if not query:
        return {"query": "", "results": []}

    results = search_pages(query, ALL_PAGES, top_k=max(1, min(top_k, 10)))
    items = []
    for p, score in results:
        # 生成摘要（正文前 120 字符）
        summary = p.content.strip().replace("\n", " ")[:120]
        items.append({
            "title": p.title,
            "url": f"https://www.google.com/search?q=site%3Asilentxx.com+{p.title.replace(' ', '+')}",
            "summary": summary,
            "tags": p.tags[:5],
            "score": score,
            "confidence": p.confidence,
        })
    return {"query": query, "results": items}


@app.post("/api/chat")
async def chat(req: ChatRequest, background_tasks: BackgroundTasks):
    if not API_KEY:
        raise HTTPException(status_code=500, detail="LLM API key not configured")
    
    question = req.message.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Empty message")
    
    # 1. 检索 Wiki
    results = search_pages(question, ALL_PAGES, top_k=5)
    
    # 2. 获取记忆 + 组装 Prompt
    memory_context = get_memory_context()
    pages_only = [p for p, _ in results]
    messages = build_prompt(question, pages_only, req.history, memory_context, persona=req.persona)
    
    # 3. 调用 LLM 流式返回 + 缓冲完整回复用于记忆
    full_reply = ""
    
    async def stream_response():
        nonlocal full_reply
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
                                full_reply += content
                                yield f"data: {json.dumps({'content': content})}\n\n"
                        except json.JSONDecodeError:
                            continue
    
    # 流式完成后更新记忆
    background_tasks.add_task(update_memory, question, "")
    
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


# ── Fish Audio TTS（自然语音）──────────────────────────
FISH_API_KEY = os.getenv("FISH_AUDIO_KEY", "")
FISH_VOICE = os.getenv("FISH_VOICE", "default")  # 可换具体 voice ID


@app.post("/api/tts-fish")
async def fish_tts(req: ChatRequest):
    """Fish Audio 自然语音合成"""
    text = req.message.strip()[:800]
    if not text:
        raise HTTPException(status_code=400, detail="Empty text")
    if not FISH_API_KEY:
        raise HTTPException(status_code=500, detail="Fish Audio API key not configured")

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(
                "https://api.fish.audio/v1/tts",
                headers={
                    "Authorization": f"Bearer {FISH_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={"text": text, "voice": FISH_VOICE, "format": "mp3"},
            )
            if resp.status_code != 200:
                raise HTTPException(status_code=resp.status_code, detail=f"Fish Audio: {resp.text[:200]}")
            return Response(content=resp.content, media_type="audio/mpeg",
                          headers={"Content-Disposition": "inline"})
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fish TTS error: {str(e)}")


# ── Sherpa-ONNX TTS（本地推理，免费无限）─────────────────
SHERPA_MODEL_DIR = os.path.join(os.path.dirname(__file__), "tts_model", "vits-zh-hf-echo")
_tts_engine = None


def _get_tts_engine():
    global _tts_engine
    if _tts_engine is None:
        import sherpa_onnx
        if not os.path.exists(os.path.join(SHERPA_MODEL_DIR, "echo.onnx")):
            raise RuntimeError("TTS model not found. Run download script first.")
        _tts_engine = sherpa_onnx.OfflineTts(
            sherpa_onnx.OfflineTtsConfig(
                model=sherpa_onnx.OfflineTtsModelConfig(
                    vits=sherpa_onnx.OfflineTtsVitsModelConfig(
                        model=os.path.join(SHERPA_MODEL_DIR, "echo.onnx"),
                        tokens=os.path.join(SHERPA_MODEL_DIR, "tokens.txt"),
                        lexicon=os.path.join(SHERPA_MODEL_DIR, "lexicon.txt"),
                        dict_dir=os.path.join(SHERPA_MODEL_DIR, "dict"),
                    ),
                ),
            ),
        )
        print(f"Sherpa-ONNX TTS loaded from {SHERPA_MODEL_DIR}")
    return _tts_engine


@app.post("/api/tts-sherpa")
async def sherpa_tts(req: ChatRequest):
    """Sherpa-ONNX 本地 TTS"""
    text = req.message.strip()[:800]
    if not text:
        raise HTTPException(status_code=400, detail="Empty text")
    try:
        import soundfile as sf
        tts = _get_tts_engine()
        audio = tts.generate(text, sid=0, speed=1.0)
        buf = io.BytesIO()
        sf.write(buf, audio.samples, audio.sample_rate, format="WAV")
        buf.seek(0)
        return Response(content=buf.read(), media_type="audio/wav",
                       headers={"Content-Disposition": "inline"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sherpa TTS error: {str(e)}")


# ── 火山引擎 TTS（抖音同款，免费 100万字符/月）────────
VOLC_APP_ID = os.getenv("VOLC_APP_ID", "")
VOLC_TOKEN = os.getenv("VOLC_TOKEN", "")
VOLC_VOICE = os.getenv("VOLC_VOICE", "BV001_streaming")  # 自然女声


@app.post("/api/tts-volc")
async def volc_tts(req: ChatRequest):
    """火山引擎 TTS — 自然语音"""
    text = req.message.strip()[:500]
    if not text:
        raise HTTPException(status_code=400, detail="Empty text")
    if not VOLC_APP_ID or not VOLC_TOKEN:
        raise HTTPException(status_code=500, detail="Volcengine not configured")

    try:
        payload = {
            "app": {"appid": VOLC_APP_ID, "token": VOLC_TOKEN, "cluster": "volcano_tts"},
            "user": {"uid": "silentxx"},
            "audio": {"voice_type": VOLC_VOICE, "encoding": "mp3", "speed_ratio": 1.0},
            "request": {"text": text, "text_type": "plain"},
        }
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(
                "https://openspeech.bytedance.com/api/v1/tts",
                headers={"Authorization": f"Bearer; {VOLC_TOKEN}", "Content-Type": "application/json"},
                json=payload,
            )
            if resp.status_code != 200:
                raise HTTPException(status_code=resp.status_code, detail=f"Volcengine: {resp.text[:200]}")
            return Response(content=resp.content, media_type="audio/mpeg",
                          headers={"Content-Disposition": "inline"})
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Volc TTS error: {str(e)}")


# ── 视觉理解（OpenRouter 免费模型）────────────────────
VISION_MODEL = os.getenv("VISION_MODEL", "google/gemini-2.0-flash-exp:free")
OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY", "")


@app.post("/api/vision")
async def vision(req: VisionRequest):
    """图片理解，调用免费视觉模型"""
    if not OPENROUTER_KEY:
        raise HTTPException(status_code=500, detail="OpenRouter API key not configured")

    try:
        # 移除 data:image/...;base64, 前缀
        image_data = req.image
        if "," in image_data:
            image_data = image_data.split(",", 1)[1]

        payload = {
            "model": VISION_MODEL,
            "messages": [{
                "role": "user",
                "content": [
                    {"type": "text", "text": req.prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}},
                ],
            }],
            "max_tokens": 800,
        }
        async with httpx.AsyncClient(timeout=60) as client:
            resp = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENROUTER_KEY}",
                    "Content-Type": "application/json",
                },
                json=payload,
            )
            if resp.status_code != 200:
                raise HTTPException(status_code=resp.status_code, detail=f"Vision API: {resp.text[:200]}")
            data = resp.json()
            content = data["choices"][0]["message"]["content"]
            return {"content": content}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Vision error: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)

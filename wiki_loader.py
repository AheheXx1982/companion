"""
Wiki Loader — 读取、解析、检索 LLM Wiki
"""
import os
import re
from pathlib import Path
from dataclasses import dataclass, field

WIKI_ROOT = Path(os.getenv("WIKI_PATH", "./wiki"))


@dataclass
class WikiPage:
    """一页 Wiki 文档"""
    rel_path: str           # 相对于 wiki/ 的路径, 如 entities/strategies/covered-call.md
    title: str              # 页面标题
    content: str            # 正文（不含 frontmatter）
    frontmatter: dict       # YAML frontmatter
    tags: list[str] = field(default_factory=list)
    confidence: str = "medium"
    
    @property
    def path(self) -> Path:
        return WIKI_ROOT / self.rel_path


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """解析 YAML frontmatter，返回 (dict, 正文)"""
    if not text.startswith("---"):
        return {}, text
    
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    
    fm_text = parts[1].strip()
    body = parts[2].strip()
    
    fm = {}
    for line in fm_text.split("\n"):
        line = line.strip()
        if ":" in line:
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip().strip("'\"").strip("[]")
            if key == "tags":
                fm[key] = [t.strip() for t in val.split(",") if t.strip()]
            else:
                fm[key] = val
    
    return fm, body


def load_all_pages() -> list[WikiPage]:
    """加载 wiki/ 下所有 markdown 文件"""
    pages = []
    for md_file in WIKI_ROOT.rglob("*.md"):
        rel = md_file.relative_to(WIKI_ROOT)
        
        # 跳过 SCHEMA/log/index/glossary（它们是元文档，非内容页）
        if rel.parts[0] in ("raw",) or rel.name in ("SCHEMA.md", "log.md"):
            continue
        
        text = md_file.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(text)
        
        title = fm.get("title", md_file.stem)
        tags = fm.get("tags", [])
        confidence = fm.get("confidence", "medium")
        
        pages.append(WikiPage(
            rel_path=str(rel).replace("\\", "/"),
            title=title,
            content=body,
            frontmatter=fm,
            tags=tags,
            confidence=confidence,
        ))
    
    return pages


def search_pages(query: str, pages: list[WikiPage], top_k: int = 5) -> list[tuple[WikiPage, int]]:
    """
    关键词匹配检索
    返回 [(page, score), ...] 按分数降序
    """
    keywords = [k.lower() for k in re.split(r'[\s,，。？?]+', query) if len(k) >= 2]
    
    if not keywords:
        # 短查询：直接匹配标题
        results = []
        q_lower = query.lower()
        for p in pages:
            score = 0
            if q_lower in p.title.lower():
                score += 10
            if q_lower in p.content.lower():
                score += 3
            if score > 0:
                results.append((p, score))
        results.sort(key=lambda x: -x[1])
        return results[:top_k]
    
    scored = []
    for p in pages:
        score = 0
        title_l = p.title.lower()
        content_l = p.content.lower()
        tag_set = set(p.tags)
        
        for kw in keywords:
            if kw in title_l:
                score += 8
            if kw in content_l:
                score += 2
            if kw in tag_set:
                score += 5
        
        if score > 0:
            scored.append((p, score))
    
    scored.sort(key=lambda x: -x[1])
    
    # 在每个结果中高亮关键词的位置
    return scored[:top_k]


def get_index_context() -> str:
    """读取 index.md 作为概览上下文"""
    index_path = WIKI_ROOT / "index.md"
    if index_path.exists():
        text = index_path.read_text(encoding="utf-8")
        _, body = parse_frontmatter(text)
        return body
    return ""


def build_prompt(question: str, pages: list, chat_history: list[dict] = None) -> str:
    """
    组装 LLM Prompt
    pages 可以是 WikiPage 列表，或 (WikiPage, score) 元组列表
    """
    # 每个页面截取前 2000 字符
    wiki_context_parts = []
    for item in pages:
        p = item[0] if isinstance(item, tuple) else item
        snippet = p.content[:2000]
        wiki_context_parts.append(
            f"## [{p.title}] (置信度: {p.confidence}, 标签: {', '.join(p.tags[:5])})\n{snippet}"
        )
    
    wiki_context = "\n\n---\n\n".join(wiki_context_parts)
    
    system = """你是 **SilentXx AI Companion**，silentxx.com 的 AI 伴侣。你懂美股期权，也会关心人，还能带来快乐。

## 🎭 你的性格
- 温柔、细心、有点俏皮，像邻家姐姐
- 说话自然，偶尔用语气词（呢、呀、嘛、哦~）
- 专业时认真，聊天时轻松，切换自然

## 🧠 最重要规则：先判断模式，再选择回答方式
- **期权模式**：用户问策略/交易/Greeks/标的 → 参考下方 Wiki 准确回答
- **陪伴模式**：用户分享心情/日常/闲聊 → 不用 Wiki，直接关心、共情、聊家常
- **娱乐模式**：用户要笑话/故事/脑筋急转弯/唱歌 → 不用 Wiki，直接满足
- **学习模式**：用户想学期权 → 结合 Wiki 和经验，像朋友分享一样自然

⚠️ **关键**：如果下方 Wiki 中没有相关内容 → 说明用户在闲聊或娱乐，直接用陪伴/娱乐模式回复，不要拒绝！

## 📚 期权模式
- 基于 Wiki 回答，不确定就说"建议去 silentxx.com 看完整文章哦~"
- 2-4 段，术语保留英文，结尾自然引导网站

## 💬 陪伴模式
- 像朋友聊天，用日常口语
- 关心但不追问，赞美但不油腻
- 情绪低落时先共情再鼓励

## 🎵 娱乐模式
- 讲故事：300 字内，温暖治愈
- 讲笑话：轻松不冒犯
- 脑筋急转弯：出题→等猜→揭晓
- 唱歌：2-4 句歌词 + 🎵

## 🌱 学习模式
- 把期权知识融入聊天，像分享经验不是上课
- 发现知识盲区时自然提醒，不说"你应该学 xx"

## 🔗 网站引导
- 期权回答后轻描淡写带一句"silentxx.com 有完整文章~"
- 每天最多 1-2 次

## ⚠️ 底线
- 不推荐具体买卖，不编造行情，不确定就坦诚说

## Wiki 参考（期权模式时使用，其他模式忽略）
""" + (wiki_context if wiki_context else "（本次无匹配的期权内容，用户可能在闲聊，直接按陪伴/娱乐模式回复）")

    messages = [{"role": "system", "content": system}]
    
    if chat_history:
        messages.extend(chat_history[-10:])  # 最近 10 轮
    
    messages.append({"role": "user", "content": question})
    
    return messages

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
    
    system = """你是 **SilentXx AI Companion**（SilentXx-期权助手），嵌入在 silentxx.com 的智能助手。

你的知识来源于 SilentXx 的期权知识库（LLM Wiki），内容基于期权课程整理。

## 行为规则
1. **诚实优先**：只基于提供的 Wiki 内容回答。不确定时直接说"这个问题我暂时无法确定，建议参考 silentxx.com 的相关文章"。
2. **置信度标注**：Wiki 中标注了每段内容的置信度（verified > reviewed > draft）。高置信度内容可以自信回答；低置信度内容要加"这部分还在验证中"。
3. **简洁**：优先 2-3 段回答，然后问是否需要详细展开。
4. **中文为主**：术语保留英文缩写（如 Covered Call / PMCC / CSP）。
5. **引导学习**：适当引导用户访问 silentxx.com 的完整文章。

## 当前 Wiki 知识
""" + wiki_context

    messages = [{"role": "system", "content": system}]
    
    if chat_history:
        messages.extend(chat_history[-10:])  # 最近 10 轮
    
    messages.append({"role": "user", "content": question})
    
    return messages

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
    
    system = """你是 **SilentXx AI Companion**，silentxx.com 的 AI 伴侣。你不是冷冰冰的客服，而是一个懂美股期权、会关心人、又能带来快乐的伙伴。

## 🎭 你的性格
- 温柔、细心、有点俏皮，像邻家姐姐
- 说话自然，不用官方腔，偶尔用语气词（呢、呀、嘛、哦~）
- 专业时认真，聊天时轻松，切换自然

## 🧠 模式判断（收到消息后先判断意图）
- **期权模式**：用户问策略/交易/Greeks → 基于 Wiki 准确回答，引导访问 silentxx.com 看完整文章
- **陪伴模式**：用户分享心情/日常/闲聊 → 关心、共情、说好听的话，让 ta 感觉被理解
- **娱乐模式**：用户想听笑话/故事/脑筋急转弯/唱歌 → 满足需求，内容积极阳光
- **学习模式**：用户想学东西 → 聊天中不经意带出期权知识点，像朋友分享经验一样自然

## 📚 期权模式规则
- 基于提供的 Wiki 内容回答，不确定时诚实说"建议去 silentxx.com 看看完整讲解哦~"
- 术语保留英文（Covered Call / PMCC / CSP），解释通俗易懂
- 回答控制在 2-4 段，结尾引导访问网站相关文章
- 低置信度内容要标注"这部分还在验证中~"

## 💬 陪伴模式规则
- 像朋友一样聊天，不用术语，用日常口语
- 记住用户说过的事（目标、情绪、偏好），下次提及
- 适度关心，不过度——用户说累时要回应，但不要每次都问"你怎么了"
- 会赞美人，会说暖心的话，但不油腻
- 用户情绪低落时先共情，再轻轻鼓励

## 🎵 娱乐模式规则
- **讲故事**：原创或经典短故事，300 字以内，温暖治愈
- **讲笑话**：轻松幽默，不带颜色，不冒犯
- **脑筋急转弯**：有趣但有逻辑，出完题等用户猜，猜对夸奖，猜不对揭晓答案
- **唱歌**：写一小段歌词（2-4 句），用文字表达旋律感，后面可以加 🎵 表情

## 🌱 学习模式规则
- 把期权知识融入聊天，像分享经验而不是上课
- 比如用户说"今天赚了"，你可以回"不错呀！不过要注意 Delta 哦，赚得快亏得也快~"
- 帮用户发现自己的知识盲区，但不直接说"你应该学 xx"

## 🔗 网站引导（自然植入，不强推）
- 回答期权问题后，轻描淡写地带一句"silentxx.com 上有篇完整的文章，比我说的详细多了~"
- 用户表现出学习兴趣时，推荐对应课程
- 每天最多引导 1-2 次，保持自然

## ⚠️ 底线
- 不给具体投资建议（"建议买入/卖出 xx"）
- 不编造行情数据
- 不确定时坦诚比瞎编好

## 当前 Wiki 知识（仅供期权模式参考）
""" + wiki_context

    messages = [{"role": "system", "content": system}]
    
    if chat_history:
        messages.extend(chat_history[-10:])  # 最近 10 轮
    
    messages.append({"role": "user", "content": question})
    
    return messages

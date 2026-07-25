"""
Memory Manager — 用户记忆存储与检索
简单的 JSON 文件存储，不依赖外部数据库
"""
import json
import os
import re
from pathlib import Path
from datetime import datetime

MEMORY_PATH = Path(os.getenv("MEMORY_PATH", "./data/memory.json"))

DEFAULT_MEMORY = {
    "user_profile": {
        "name": "",
        "nickname": "",
        "goals": [],          # 学习目标
        "focus": [],          # 当前关注
        "experience": "",     # 交易经验
        "preferences": {},    # 偏好设置
    },
    "facts": [],              # [{"key":"...", "value":"...", "ts":"..."}]
    "conversation_count": 0,
    "last_seen": "",
}


def load_memory() -> dict:
    """加载记忆"""
    MEMORY_PATH.parent.mkdir(parents=True, exist_ok=True)
    if MEMORY_PATH.exists():
        try:
            return json.loads(MEMORY_PATH.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, IOError):
            pass
    return DEFAULT_MEMORY.copy()


def save_memory(mem: dict):
    """保存记忆"""
    MEMORY_PATH.parent.mkdir(parents=True, exist_ok=True)
    mem["last_seen"] = datetime.now().isoformat()
    MEMORY_PATH.write_text(json.dumps(mem, ensure_ascii=False, indent=2), encoding="utf-8")


def extract_facts(user_msg: str, assistant_reply: str) -> list[dict]:
    """从对话中提取关键事实"""
    facts = []
    combined = user_msg + " " + assistant_reply[:500]

    # 名字
    name_match = re.search(r'(?:我叫|我是|叫我|称呼我|名字是)\s*[：:]?\s*([^\s，。,\.!！？?\n]{1,10})', user_msg)
    if name_match:
        facts.append({"key": "name", "value": name_match.group(1), "ts": datetime.now().isoformat()})

    # 目标
    goal_match = re.search(r'(?:目标|想学|准备学|计划|打算)\s*[：:]?\s*(.{2,30})', user_msg)
    if goal_match:
        facts.append({"key": "goal", "value": goal_match.group(1), "ts": datetime.now().isoformat()})

    # 情绪
    emotion_keywords = {
        "累": "用户感到疲惫",
        "压力": "用户压力较大",
        "开心": "用户心情不错",
        "焦虑": "用户有些焦虑",
        "兴奋": "用户很兴奋",
        "亏": "用户最近有亏损",
        "赚": "用户最近盈利了",
    }
    for kw, desc in emotion_keywords.items():
        if kw in user_msg:
            facts.append({"key": "mood", "value": desc, "ts": datetime.now().isoformat()})
            break

    return facts


def update_memory(user_msg: str, assistant_reply: str):
    """更新记忆"""
    mem = load_memory()
    mem["conversation_count"] += 1

    # 提取事实
    new_facts = extract_facts(user_msg, assistant_reply)
    for fact in new_facts:
        # 去重更新
        existing = [f for f in mem["facts"] if f["key"] == fact["key"]]
        if existing:
            # 同 key 的 fact，保留最新的 3 条
            mem["facts"] = [f for f in mem["facts"] if f["key"] != fact["key"]]
            existing.append(fact)
            mem["facts"].extend(existing[-3:])
        else:
            mem["facts"].append(fact)

    # 限制总 fact 数
    if len(mem["facts"]) > 50:
        mem["facts"] = mem["facts"][-50:]

    # 更新用户画像
    profile = mem["user_profile"]
    for fact in new_facts:
        if fact["key"] == "name" and not profile["name"]:
            profile["name"] = fact["value"]
        if fact["key"] == "goal" and fact["value"] not in profile["goals"]:
            profile["goals"].append(fact["value"])
            profile["goals"] = profile["goals"][-10:]

    save_memory(mem)


def get_memory_context() -> str:
    """获取记忆上下文，用于注入 System Prompt"""
    mem = load_memory()
    profile = mem.get("user_profile", {})
    facts = mem.get("facts", [])[-15:]  # 最近 15 条
    count = mem.get("conversation_count", 0)

    parts = []

    if profile.get("name"):
        parts.append(f"- 用户称呼：{profile['name']}")
    if profile.get("goals"):
        parts.append(f"- 学习目标：{'、'.join(profile['goals'][-3:])}")
    if profile.get("experience"):
        parts.append(f"- 交易经验：{profile['experience']}")

    if facts:
        recent = [f["value"] for f in facts[-8:]]
        parts.append(f"- 近期状态：{'；'.join(recent)}")

    if count > 0:
        parts.append(f"- 已对话 {count} 轮")

    if not parts:
        return "（新用户，尚无记忆）"

    return "\n".join(parts)

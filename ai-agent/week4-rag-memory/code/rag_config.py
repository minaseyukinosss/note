"""
Week4 RAG 共用路径与 Chroma 配置。
"""

from pathlib import Path

CODE_DIR = Path(__file__).resolve().parent
KNOWLEDGE_DIR = CODE_DIR / "knowledge"
CHROMA_DIR = CODE_DIR / ".chroma"
COLLECTION_NAME = "ai_agent_notes"

# Chroma 余弦距离 → 相似度：score = 1 - distance
# 入门阶段用 golden case 标定；0.35 可让 W4-003（PPO 不在库）top-1≈0.33 判为未命中
DEFAULT_SCORE_THRESHOLD = 0.35

# Markdown 切分：保留 heading 层级到 metadata
HEADERS_TO_SPLIT = [
    ("#", "h1"),
    ("##", "h2"),
    ("###", "h3"),
]


def format_citation(source: str, section: str) -> str:
    """统一引用格式，供 rag_agent 与 eval 复用。"""
    return f"[来源: {source}#{section}]"

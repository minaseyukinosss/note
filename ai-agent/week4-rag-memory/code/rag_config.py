"""
Week4 RAG 共用路径与 Chroma 配置。

Path(__file__)：当前 .py 文件的路径，用来拼出 knowledge/、.chroma/ 等目录。
"""

from pathlib import Path

# 本文件所在目录 = week4-rag-memory/code/
CODE_DIR = Path(__file__).resolve().parent
KNOWLEDGE_DIR = CODE_DIR / "knowledge"  # 原始 markdown 笔记
CHROMA_DIR = CODE_DIR / ".chroma"  # 向量库持久化目录（已在 .gitignore）
COLLECTION_NAME = "ai_agent_notes"  # Chroma 里的「表名」

# Chroma 返回的是 cosine distance；相似度 score = 1 - distance
# 0.35 是用 W4-003（PPO）标定出来的：top-1≈0.33 会判为未命中
DEFAULT_SCORE_THRESHOLD = 0.35

# 切 markdown 时按哪些标题切；元组 (markdown符号, metadata字段名)
HEADERS_TO_SPLIT = [
    ("#", "h1"),
    ("##", "h2"),
    ("###", "h3"),
]


def format_citation(source: str, section: str) -> str:
    """拼出统一引用格式，例如 [来源: knowledge/foo.md#ReAct]"""
    return f"[来源: {source}#{section}]"

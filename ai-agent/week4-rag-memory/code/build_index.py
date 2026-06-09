"""
Day 22-23：离线建库 — 读 markdown → 切 chunk → 向量化 → 写入 Chroma。

运行：
  cd ai-agent && source .venv/bin/activate
  python week4-rag-memory/code/build_index.py
"""

from __future__ import annotations

import hashlib
from pathlib import Path

import chromadb
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction
from langchain_core.documents import Document
from langchain_text_splitters import MarkdownHeaderTextSplitter

from rag_config import (
    CHROMA_DIR,
    COLLECTION_NAME,
    HEADERS_TO_SPLIT,
    KNOWLEDGE_DIR,
)


def _section_from_metadata(meta: dict) -> str:
    """从 h3/h2/h1 里取最细一级标题，作为 section（引用时用）。"""
    for key in ("h3", "h2", "h1"):
        # := 海象运算符：赋值的同时判断是否为真
        if title := meta.get(key):
            return str(title).strip()
    return "（无标题）"


def load_chunks(knowledge_dir: Path) -> list[Document]:
    """
    遍历 knowledge/*.md，按 heading 切分。
    返回 Document 列表，每个 Document 有 page_content（正文）和 metadata（来源信息）。
    """
    splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=HEADERS_TO_SPLIT,
        strip_headers=False,  # 保留标题在正文里，方便阅读
    )
    chunks: list[Document] = []

    # sorted + glob：按文件名排序，只匹配 .md
    for md_path in sorted(knowledge_dir.glob("*.md")):
        text = md_path.read_text(encoding="utf-8")
        source = f"knowledge/{md_path.name}"
        for doc in splitter.split_text(text):
            meta = dict(doc.metadata)
            meta["source"] = source
            meta["section"] = _section_from_metadata(meta)
            chunks.append(
                Document(page_content=doc.page_content.strip(), metadata=meta)
            )

    # 列表推导：过滤掉空 chunk
    return [c for c in chunks if c.page_content]


def _chunk_id(source: str, section: str, content: str) -> str:
    """用内容哈希生成稳定 ID，重跑索引时同 chunk 同 ID。"""
    raw = f"{source}|{section}|{content[:200]}"
    return hashlib.sha256(raw.encode()).hexdigest()[:32]


def build_index(*, knowledge_dir: Path = KNOWLEDGE_DIR) -> int:
    """建索引主流程；返回写入的 chunk 数量。"""
    if not knowledge_dir.is_dir():
        raise FileNotFoundError(f"知识库目录不存在: {knowledge_dir}")

    chunks = load_chunks(knowledge_dir)
    if not chunks:
        raise ValueError(f"{knowledge_dir} 下没有可用的 markdown chunk")

    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))

    # 幂等：先删旧 collection 再建，避免重复 add
    try:
        client.delete_collection(COLLECTION_NAME)
    except (ValueError, chromadb.errors.NotFoundError):
        pass  # 第一次跑时没有旧 collection，忽略错误

    collection = client.create_collection(
        name=COLLECTION_NAME,
        embedding_function=DefaultEmbeddingFunction(),  # 本地 onnx 模型，免费
        metadata={"hnsw:space": "cosine"},  # 用余弦相似度
    )

    ids = [
        _chunk_id(c.metadata["source"], c.metadata["section"], c.page_content)
        for c in chunks
    ]
    documents = [c.page_content for c in chunks]
    metadatas = [c.metadata for c in chunks]

    collection.add(ids=ids, documents=documents, metadatas=metadatas)
    return len(chunks)


def main() -> None:
    count = build_index()
    print(f"索引完成：{count} 个 chunk → {CHROMA_DIR}")
    print(f"collection: {COLLECTION_NAME}")


if __name__ == "__main__":
    main()

"""
Day 22-23：读取 knowledge/*.md，切分 + embedding + 写入 Chroma（幂等重跑）。

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
    """从 heading metadata 拼出 section 名，供引用使用。"""
    for key in ("h3", "h2", "h1"):
        if title := meta.get(key):
            return str(title).strip()
    return "（无标题）"


def load_chunks(knowledge_dir: Path) -> list[Document]:
    """按 markdown heading 切分，并为每个 chunk 补全 source / section。"""
    splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=HEADERS_TO_SPLIT,
        strip_headers=False,
    )
    chunks: list[Document] = []

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

    return [c for c in chunks if c.page_content]


def _chunk_id(source: str, section: str, content: str) -> str:
    raw = f"{source}|{section}|{content[:200]}"
    return hashlib.sha256(raw.encode()).hexdigest()[:32]


def build_index(*, knowledge_dir: Path = KNOWLEDGE_DIR) -> int:
    if not knowledge_dir.is_dir():
        raise FileNotFoundError(f"知识库目录不存在: {knowledge_dir}")

    chunks = load_chunks(knowledge_dir)
    if not chunks:
        raise ValueError(f"{knowledge_dir} 下没有可用的 markdown chunk")

    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))

    # 幂等：删旧 collection 再建，避免重复写入
    try:
        client.delete_collection(COLLECTION_NAME)
    except (ValueError, chromadb.errors.NotFoundError):
        pass

    collection = client.create_collection(
        name=COLLECTION_NAME,
        embedding_function=DefaultEmbeddingFunction(),
        metadata={"hnsw:space": "cosine"},
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

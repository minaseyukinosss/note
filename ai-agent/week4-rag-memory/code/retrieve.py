"""
Day 22-23：在线检索 — query 向量化后在 Chroma 里取 top-k。

两个入口：
  search()   — 始终返回 top-k，不过滤（观察分数用，配合 CLI --raw）
  retrieve() — top-1 低于阈值则整批判「未命中」（给 Agent / W4-003 用）
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass

import chromadb
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction

from rag_config import (
    CHROMA_DIR,
    COLLECTION_NAME,
    DEFAULT_SCORE_THRESHOLD,
)


@dataclass
class Hit:
    """一条检索命中：正文 + 来源 + 章节 + 相似度分数。"""

    content: str
    source: str
    section: str
    score: float


@dataclass
class RetrieveResult:
    """retrieve() 的返回值；to_dict() 供 tools.py 转 JSON。"""

    hits: list[Hit]
    reason: str | None = None  # 未命中时填 "未命中"

    def to_dict(self) -> dict:
        if self.hits:
            # asdict：把 dataclass 转成普通 dict
            return {"hits": [asdict(h) for h in self.hits]}
        return {"hits": [], "reason": self.reason or "未命中"}


def get_collection():
    """连接本地 Chroma；向量库不存在时提示先 build_index。"""
    if not CHROMA_DIR.is_dir():
        print(
            f"向量库不存在: {CHROMA_DIR}\n请先运行: python week4-rag-memory/code/build_index.py",
            file=sys.stderr,
        )
        sys.exit(1)

    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    return client.get_collection(
        name=COLLECTION_NAME,
        embedding_function=DefaultEmbeddingFunction(),
    )


def search(query: str, *, top_k: int = 3) -> list[Hit]:
    """
    核心检索：Chroma 按相似度排序，取前 top_k 条。
    * 在参数名前的 * 表示 top_k 必须用关键字传参，如 search(q, top_k=5)
    """
    collection = get_collection()
    result = collection.query(
        query_texts=[query],  # 列表形式，支持批量 query
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )

    hits: list[Hit] = []
    # Chroma 返回二维结构，[0] 表示第一个 query 的结果
    docs = result["documents"][0]
    metas = result["metadatas"][0]
    dists = result["distances"][0]

    # zip 同时遍历三个平行列表；strict=True 要求长度必须相同
    for doc, meta, dist in zip(docs, metas, dists, strict=True):
        score = 1.0 - float(dist)  # distance → 相似度
        hits.append(
            Hit(
                content=doc,
                source=meta.get("source", ""),
                section=meta.get("section", ""),
                score=round(score, 4),
            )
        )

    return hits


def retrieve(
    query: str,
    *,
    top_k: int = 3,
    score_threshold: float = DEFAULT_SCORE_THRESHOLD,
) -> RetrieveResult:
    """
    带阈值的检索：
      1. 先 search 拿 top_k
      2. 若 top-1 分数 < 阈值 → 返回空 hits（未命中）
      3. 否则把 top_k 条全部返回
    """
    hits = search(query, top_k=top_k)
    if hits and hits[0].score < score_threshold:
        return RetrieveResult(hits=[], reason="未命中")
    return RetrieveResult(hits=hits)


def format_result(result: RetrieveResult) -> str:
    return json.dumps(result.to_dict(), ensure_ascii=False, indent=2)


def main() -> None:
    # argparse：解析命令行参数，如 retrieve.py "问题" --raw --top-k 5
    parser = argparse.ArgumentParser(description="RAG 检索：top-k chunk + 来源")
    parser.add_argument("query", help="检索 query")
    parser.add_argument("--top-k", type=int, default=3)
    parser.add_argument(
        "--threshold",
        type=float,
        default=DEFAULT_SCORE_THRESHOLD,
        help="top-1 相似度低于此值视为未命中（--raw 时忽略）",
    )
    parser.add_argument(
        "--raw",
        action="store_true",  # 出现 --raw 则为 True
        help="返回原始 top-k，不过滤阈值",
    )
    args = parser.parse_args()

    if args.raw:
        hits = search(args.query, top_k=args.top_k)
        print(format_result(RetrieveResult(hits=hits)))
    else:
        print(format_result(retrieve(args.query, top_k=args.top_k, score_threshold=args.threshold)))


if __name__ == "__main__":
    main()

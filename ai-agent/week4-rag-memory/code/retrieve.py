"""
Day 22-23：独立检索脚本，给定 query 返回 top-k chunk + 来源 + 相似度。

`search()` 始终返回 top-k（供 Day 22-23 观察分数分布）；
`retrieve()` 应用阈值（供 rag_agent 工具与 W4-003 未命中判定）。

运行：
  python week4-rag-memory/code/retrieve.py "ReAct 是什么"
  python week4-rag-memory/code/retrieve.py "强化学习 PPO 算法"
  python week4-rag-memory/code/retrieve.py "今天股票涨了吗" --raw   # 观察原始 top-k 分数
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
    content: str
    source: str
    section: str
    score: float


@dataclass
class RetrieveResult:
    """工具层统一返回结构，rag_agent 直接复用。"""

    hits: list[Hit]
    reason: str | None = None

    def to_dict(self) -> dict:
        if self.hits:
            return {"hits": [asdict(h) for h in self.hits]}
        return {"hits": [], "reason": self.reason or "未命中"}


def get_collection():
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
    """检索 top-k，不做阈值过滤（Day 22-23 观察用）。"""
    collection = get_collection()
    result = collection.query(
        query_texts=[query],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )

    hits: list[Hit] = []
    docs = result["documents"][0]
    metas = result["metadatas"][0]
    dists = result["distances"][0]

    for doc, meta, dist in zip(docs, metas, dists, strict=True):
        score = 1.0 - float(dist)
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
    带阈值的检索。top-1 低于阈值时返回未命中（W4-003 必做路径）。
    """
    hits = search(query, top_k=top_k)
    if hits and hits[0].score < score_threshold:
        return RetrieveResult(hits=[], reason="未命中")
    return RetrieveResult(hits=hits)


def format_result(result: RetrieveResult) -> str:
    return json.dumps(result.to_dict(), ensure_ascii=False, indent=2)


def main() -> None:
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
        action="store_true",
        help="返回原始 top-k，不过滤阈值（Day 22-23 观察分数分布）",
    )
    args = parser.parse_args()

    if args.raw:
        hits = search(args.query, top_k=args.top_k)
        print(format_result(RetrieveResult(hits=hits)))
    else:
        print(format_result(retrieve(args.query, top_k=args.top_k, score_threshold=args.threshold)))


if __name__ == "__main__":
    main()

"""
Day 17-19：LangGraph Checkpointer 示例。

同一 thread_id 下，第二轮对话能读到上一轮的 messages。

运行：
  python checkpoint_demo.py

会在 code/ 目录生成 checkpoints.db（已在 .gitignore 惯例中勿提交）。
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

from langchain_core.messages import HumanMessage
from langgraph.checkpoint.sqlite import SqliteSaver

from langgraph_agent import SYSTEM_PROMPT, build_graph
from langchain_core.messages import SystemMessage

DB_PATH = Path(__file__).resolve().parent / "checkpoints.db"


def main() -> None:
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    checkpointer = SqliteSaver(conn)
    graph = build_graph(checkpointer=checkpointer)

    thread_id = "demo-thread-1"
    config = {"configurable": {"thread_id": thread_id}}

    print("=" * 60)
    print("第 1 轮：查北京天气")
    r1 = graph.invoke(
        {
            "messages": [
                SystemMessage(content=SYSTEM_PROMPT),
                HumanMessage(content="北京今天天气怎么样？"),
            ]
        },
        config=config,
    )
    print("回答:", r1["messages"][-1].content)

    print("\n" + "=" * 60)
    print("第 2 轮：只问「那上海呢？」—— 应能联系上下文")
    r2 = graph.invoke(
        {"messages": [HumanMessage(content="那上海呢？")]},
        config=config,
    )
    print("回答:", r2["messages"][-1].content)
    print(f"\n（checkpoints 已写入 {DB_PATH}）")


if __name__ == "__main__":
    main()

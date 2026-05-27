"""
Day 17-19：LangGraph Checkpointer 示例。

演示跨轮对话：同一 thread_id 下，第 2 轮只传新消息，框架从 DB 读出旧 messages 合并。

运行：
  python checkpoint_demo.py

会在 code/ 目录生成 checkpoints.db（勿提交 Git）。
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.checkpoint.sqlite import SqliteSaver

from langgraph_agent import SYSTEM_PROMPT, build_graph

DB_PATH = Path(__file__).resolve().parent / "checkpoints.db"


def main() -> None:
    # check_same_thread=False：允许多线程/多次 invoke 共用同一连接（学习 demo 够用）
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    checkpointer = SqliteSaver(conn)

    # 必须 compile 时传入 checkpointer，否则 invoke 不会读写 DB
    graph = build_graph(checkpointer=checkpointer)

    # thread_id = 存档槽位；同一 ID 的多次 invoke 共享历史 state
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
    # 第 1 轮结束后：DB 已存完整 messages（System + Human + AI + Tool + AI …）

    print("\n" + "=" * 60)
    print("第 2 轮：只问「那上海呢？」—— 应能联系上下文")
    r2 = graph.invoke(
        # 只传新 HumanMessage；add_messages 会从 checkpoint 读出旧 messages 再追加
        {"messages": [HumanMessage(content="那上海呢？")]},
        config=config,  # 同一 thread_id → 读到第 1 轮历史
    )
    print("回答:", r2["messages"][-1].content)
    print(f"\n（checkpoints 已写入 {DB_PATH}）")


if __name__ == "__main__":
    main()

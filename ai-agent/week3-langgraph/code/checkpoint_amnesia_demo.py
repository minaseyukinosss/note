"""
实验 2：换 thread_id 验证 checkpoint 隔离。

第 1 轮写入 thread=A，第 2 轮改用 thread=B → 读不到 A 的历史。

判据：看第 2 轮 r2["messages"] 里有没有第 1 轮内容，不要只看最终回答
（「那上海呢？」模型可能靠常识猜对，不代表有记忆）。

对照：checkpoint_demo.py 两轮用同一 thread_id。

运行：
  python checkpoint_amnesia_demo.py
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.checkpoint.sqlite import SqliteSaver

from langgraph_agent import SYSTEM_PROMPT, build_graph

DB_PATH = Path(__file__).resolve().parent / "checkpoints.db"


def main() -> None:
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    checkpointer = SqliteSaver(conn)
    graph = build_graph(checkpointer=checkpointer)

    same_thread = {"configurable": {"thread_id": "amnesia-A"}}
    new_thread = {"configurable": {"thread_id": "amnesia-B"}}  # 故意换槽位

    print("=" * 60)
    print("第 1 轮（thread=amnesia-A）：北京天气怎么样？")
    r1 = graph.invoke(
        {
            "messages": [
                SystemMessage(content=SYSTEM_PROMPT),
                HumanMessage(content="北京今天天气怎么样？"),
            ]
        },
        config=same_thread,
    )
    print("回答:", r1["messages"][-1].content)

    print("\n" + "=" * 60)
    print("第 2 轮（thread=amnesia-B，换了 thread_id）：那上海呢？")
    print("预期：messages 里没有北京相关记录（即使回答看起来合理也算失忆）。")
    r2 = graph.invoke(
        {"messages": [HumanMessage(content="那上海呢？")]},
        config=new_thread,  # 新 thread_id → DB 无历史 → 只有本轮传入的 1 条 Human
    )
    print("回答:", r2["messages"][-1].content)

    print("\n--- 第 2 轮 messages 全量打印 ---")
    print("有记忆时应 8+ 条且含「北京」；失忆时通常 4~6 条且从「那上海呢？」起算。")
    for i, m in enumerate(r2["messages"]):
        text = str(m.content or getattr(m, "tool_calls", None) or "")
        if len(text) > 80:
            text = text[:80] + "..."
        print(f"  [{i}] {m.type}: {text}")


if __name__ == "__main__":
    main()

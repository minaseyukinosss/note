"""
Day 20-21：Week3 Demo 交付脚本（科技新闻摘要 + 多轮续聊）。

基于 checkpoint_demo.py，组合：
  - StateGraph（langgraph_agent.build_graph）
  - SqliteSaver checkpoint（同一 thread_id 续聊）
  - Tavily 真搜索（tools.search）

运行：
  python news_demo.py

会在 code/ 目录写入 checkpoints.db（勿提交 Git）。
交付物填写见 ../demo/
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.checkpoint.sqlite import SqliteSaver

from langgraph_agent import SYSTEM_PROMPT, build_graph

DB_PATH = Path(__file__).resolve().parent / "checkpoints.db"

# TODO：可按场景定制 system prompt
DEMO_SYSTEM_PROMPT = SYSTEM_PROMPT

# TODO：填写 Demo 对话
ROUND_1_QUESTION = "搜索今天的一条 AI 新闻并总结"
ROUND_2_QUESTION = "刚才那条新闻的来源是什么？"

THREAD_ID = "news-demo-thread"


def invoke_round(graph, config, question: str, *, with_system: bool = False, verbose: bool = False) -> str:
    """单轮 invoke，返回最终回答文本。"""
    messages = [HumanMessage(content=question)]
    if with_system:
        messages.insert(0, SystemMessage(content=DEMO_SYSTEM_PROMPT))
    result = graph.invoke({"messages": messages}, config=config)
    if verbose:
        print(f"\n--- messages 共 {len(result['messages'])} 条 ---")
        for i, m in enumerate(result["messages"]):
            preview = m.content or getattr(m, "tool_calls", None) or ""
            text = str(preview)
            if len(text) > 100:
                text = text[:100] + "..."
            print(f"  [{i}] {m.type}: {text}")
    return result["messages"][-1].content or ""


def main() -> None:
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    checkpointer = SqliteSaver(conn)
    graph = build_graph(checkpointer=checkpointer)
    config = {"configurable": {"thread_id": THREAD_ID}}

    # TODO：取消注释并填写 ROUND_*_QUESTION 后运行
    print("=" * 60)
    print("第 1 轮")
    print("回答:", invoke_round(graph, config, ROUND_1_QUESTION, with_system=True, verbose=True))
    
    print("\n" + "=" * 60)
    print("第 2 轮（续聊）")
    print("回答:", invoke_round(graph, config, ROUND_2_QUESTION, verbose=True))


if __name__ == "__main__":
    main()

"""
Day 15-16：用 LangGraph 重写 Week2 ReAct Agent。

图结构：
  START → agent → (有 tool_calls?) → tools → agent → … → END

运行：
  python langgraph_agent.py
"""

from __future__ import annotations

from typing import Annotated, Literal

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from typing_extensions import TypedDict

from config import get_llm
from tools import ALL_TOOLS

SYSTEM_PROMPT = (
    "你是个能调用工具的助手。"
    "需要查天气、做计算或搜索时，请调用对应工具。"
    "拿到所有工具结果后，用自然语言直接回答用户。"
    "若没有合适工具，礼貌说明做不到，不要编造。"
)

RECURSION_LIMIT = 12  # 约等于 Week2 的 max_steps 上限（每轮可能走 agent+tools 两步）


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]


llm_with_tools = get_llm().bind_tools(ALL_TOOLS)
tool_node = ToolNode(ALL_TOOLS)


def call_model(state: AgentState) -> dict:
    """对应 Week2：client.chat.completions.create(...)"""
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}


def route_after_model(state: AgentState) -> Literal["tools", "__end__"]:
    """对应 Week2：if not msg.tool_calls: return"""
    last = state["messages"][-1]
    if isinstance(last, AIMessage) and last.tool_calls:
        return "tools"
    return END


def build_graph(*, checkpointer=None):
    builder = StateGraph(AgentState)
    builder.add_node("agent", call_model)
    builder.add_node("tools", tool_node)
    builder.add_edge(START, "agent")
    builder.add_conditional_edges(
        "agent",
        route_after_model,
        {"tools": "tools", END: END},
    )
    builder.add_edge("tools", "agent")
    return builder.compile(checkpointer=checkpointer)


graph = build_graph()


def run_agent(user_input: str, *, verbose: bool = False) -> str:
    initial = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=user_input),
    ]
    result = graph.invoke(
        {"messages": initial},
        config={"recursion_limit": RECURSION_LIMIT},
    )
    if verbose:
        print(f"\n--- messages 共 {len(result['messages'])} 条 ---")
        for i, m in enumerate(result["messages"]):
            preview = m.content or getattr(m, "tool_calls", None) or ""
            text = str(preview)
            if len(text) > 100:
                text = text[:100] + "..."
            print(f"  [{i}] {m.type}: {text}")

    last = result["messages"][-1]
    return last.content or ""


def main() -> None:
    demos = [
        "北京今天天气怎么样？",
        "北京今天天气怎么样？再帮我算 23 * 47",
        "100 除以 0 等于多少？",
        "帮我订一张明天去上海的机票",
    ]
    for q in demos:
        print("\n" + "#" * 60)
        print("用户:", q)
        answer = run_agent(q, verbose=True)
        print("\n最终回答:", answer)


if __name__ == "__main__":
    main()

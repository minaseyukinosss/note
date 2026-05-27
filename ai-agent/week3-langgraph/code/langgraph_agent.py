"""
Day 15-16：用 LangGraph 重写 Week2 ReAct Agent。

图结构：
  START → agent → (有 tool_calls?) → tools → agent → … → END

与手写版 react_agent.py 对照：
  messages 列表     → AgentState.messages（add_messages reducer）
  for 循环          → tools → agent 固定边 + invoke
  dispatch_tool     → ToolNode
  if not tool_calls → route_after_model 条件边

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

# 图最多跑多少个 node（agent / tools 各算一步）
# 12 ≈ 手写版 max_steps=6（每轮 ReAct 通常走 agent + tools 两步）
RECURSION_LIMIT = 12


class AgentState(TypedDict):
    # Annotated + add_messages：node 返回 {"messages": [新消息]} 时追加合并，而非覆盖
    messages: Annotated[list, add_messages]


# 全局实例：bind_tools 让 LLM 知道有哪些工具；ToolNode 负责执行 tool_calls
llm_with_tools = get_llm().bind_tools(ALL_TOOLS)
tool_node = ToolNode(ALL_TOOLS)


def call_model(state: AgentState) -> dict:
    """agent 节点：读 state["messages"]，调 LLM，可能返回带 tool_calls 的 AIMessage。"""
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}  # add_messages 会 append 到 state


def route_after_model(state: AgentState) -> Literal["tools", "__end__"]:
    """
    条件边路由函数（不是 node）。

    挂在 agent 出口：有 tool_calls → 走 tools 节点；否则 → END。
    等价手写版：if not msg.tool_calls: return
    """
    last = state["messages"][-1]
    if isinstance(last, AIMessage) and last.tool_calls:
        return "tools"
    return END


def build_graph(*, checkpointer=None):
    """
    组装 StateGraph 并 compile。

    checkpointer 可选：
      - None（默认）：单次 invoke，state 不持久化
      - SqliteSaver 等：每跑完一个 node 存 state 快照，配合 thread_id 跨轮续聊
    """
    builder = StateGraph(AgentState)
    builder.add_node("agent", call_model)
    builder.add_node("tools", tool_node)
    builder.add_edge(START, "agent")
    builder.add_conditional_edges(
        "agent",
        route_after_model,
        # 左 key = 路由函数返回值；右 value = add_node 注册的节点名
        {"tools": "tools", END: END},
    )
    builder.add_edge("tools", "agent")  # 固定边：工具跑完必回 agent
    return builder.compile(checkpointer=checkpointer)


# 无 checkpointer 的默认图，供 langgraph_agent.py 单轮 demo 使用
graph = build_graph()


def run_agent(user_input: str, *, verbose: bool = False) -> str:
    """单轮问答入口：每次 invoke 都是新会话（无 thread_id，不读 checkpoint）。"""
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
        # "北京今天天气怎么样？",
        "北京今天天气怎么样？再帮我算 23 * 47",
        # "100 除以 0 等于多少？",
        # "帮我订一张明天去上海的机票",
    ]
    for q in demos:
        print("\n" + "#" * 60)
        print("用户:", q)
        answer = run_agent(q, verbose=True)
        print("\n最终回答:", answer)


if __name__ == "__main__":
    main()

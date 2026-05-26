# Day 15-16：LangGraph 学习笔记

## 背景 / 学习目标

- 读 [LangGraph Quickstart](https://langchain-ai.github.io/langgraph/tutorials/introduction/)，对照 [`react_agent.py`](../../week2-react-agent/code/react_agent.py)（手写 ReAct：openai SDK + `for` 循环，无框架）。
- 用 LangGraph **重写**同一 Agent，功能不变。
- 能口头答：state / node / edge 分别对应手写循环里的什么。

## 今日操作

1. 读 Quickstart 前 2 节（Graph、State）。
2. 对照 [`../code/langgraph_agent.py`](../code/langgraph_agent.py) 与 [`react_agent.py`](../../week2-react-agent/code/react_agent.py)。
3. 运行：

```bash
cd ai-agent/week3-langgraph/code
python langgraph_agent.py
```

4. 用同一问题分别在两个版本各跑一遍，对比 trace 与最终回答。

## 核心概念：与手写 ReAct 一一对应

| 手写版 `react_agent.py` | LangGraph | 干什么 |
| --- | --- | --- |
| `messages: list` | `AgentState.messages` | 唯一要记住的对话状态 |
| 手动 `messages.append(...)` | `add_messages` reducer | 新消息合并进 state，不用自己 list 拼接 |
| `for step in range(max_steps)` | `agent → tools → agent` 环 | 图自动循环，直到条件边走向 `END` |
| `client.chat.completions.create` | `call_model` **node** | 调 LLM，可能返回 `tool_calls` |
| `dispatch_tool` + `role: tool` | `ToolNode` **node** | 执行工具并写回 observation |
| `if not msg.tool_calls: return` | `route_after_model` **条件 edge** | 有 tool_calls → `tools`，否则 → `END` |
| `max_steps=6` | `recursion_limit=12` | 防死循环（图里一步可能含 agent+tools 两次节点） |

### 图结构（ASCII）

```text
        ┌─────────┐
 START ─►│  agent  │─── 无 tool_calls ───► END
        └────┬────┘
             │ 有 tool_calls
             ▼
        ┌─────────┐
        │  tools  │
        └────┬────┘
             │
             └──────────► agent（再一轮）
```

手写版把这些全塞进一个 `for`；LangGraph 拆成**具名节点 + 显式边**，读代码时像看流程图。

## 文件在教什么

| 文件 | 关注点 |
| --- | --- |
| `config.py` | `ChatOpenAI` + `OPENAI_BASE_URL`，DeepSeek 与 Week1 同一套 `.env` |
| `tools.py` | `@tool` 装饰器；docstring 即工具 description |
| `langgraph_agent.py` | `StateGraph` 组装；`build_graph()` 可给 checkpoint 复用 |

### 为什么用 `ToolNode` 而不是手写 dispatch？

手写版里你要自己：

```python
for call in msg.tool_calls:
    result = dispatch_tool(...)
    messages.append({"role": "tool", "tool_call_id": call.id, ...})
```

LangGraph 的 `ToolNode` 帮你做「遍历 tool_calls → 执行 → 生成 ToolMessage」。**协议细节少写，但语义相同。**

## Quickstart 导读（带着三问读）

1. **node 和循环里的一步？** — 一次「调模型」或一次「跑工具」各是一个 node；不是 API 的一行，而是图上的一个框。
2. **state 是什么？** — 这里就是 `messages`；LangGraph 还可以扩展别的字段（如 `step_count`），本仓库先不扩。
3. **edge 是什么？** — 「agent 跑完后下一步去哪」：`tools` 还是 `END`。对应 `if not msg.tool_calls`。

## 对比实验（建议亲手做）

| 问题 | 观察 |
| --- | --- |
| 北京天气 + 23×47 | 两版都应多步完成 |
| 100 除以 0 | observation 含错误串，最终应礼貌失败 |
| 订机票 | 无工具，应拒绝 |
| 长链「北京气温 +10 …」 | **两版都可能心算 +10** — 框架没解决 |

## 易错点

| 现象 | 原因 |
| --- | --- |
| `ImportError: langgraph` / `No module named 'langchain_core'` | 主题根 venv 未装依赖或未激活；`source .venv/bin/activate && pip install -r requirements.txt` |
| DeepSeek 报 auth 错 | `.env` 的 `OPENAI_BASE_URL` / `OPENAI_API_KEY` 配置 |
| 图一直不结束 | `route_after_model` 没判 `tool_calls`；或 `recursion_limit` 太小 |
| 以为 LangGraph 更「聪明」 | 同一模型、同一 prompt、同一工具 — 行为应与手写版接近 |

## 小结

LangGraph 省的是**循环与 tool 回调的样板代码**，不是模型推理。你仍需要：看 `messages` 排错、懂退出条件、知道框架治不了「跳过 calculator」。更完整的复盘见 [day15-16-复盘](./day15-16-复盘.md)。下一步 Day 17-19 加 **Checkpointer** 与真工具，见 [day17-19-真工具与记忆](./day17-19-真工具与记忆.md)。

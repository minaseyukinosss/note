# LangGraph 核心概念

## State

State 是图中每个节点共享和更新的数据。本仓库 LangGraph 版的核心 state 是 `messages` 列表，用 `add_messages` reducer 追加合并，而非覆盖。

State 是系统的事实来源：模型读它决策，工具结果写回它。

## Node

Node 是图上的一步操作。最小 Agent 图通常两个节点：

| node | 作用 |
| --- | --- |
| `agent` | 调 LLM，返回 AIMessage，可能带 `tool_calls` |
| `tools` | 执行 tool_calls，返回 ToolMessage |

Node 职责越单一，trace 和排错越容易。

## Edge

Edge 决定下一步去哪：

```text
START → agent
agent --有 tool_calls--> tools
agent --无 tool_calls--> END
tools → agent
```

`route_after_model` 是挂在 `agent` 出口的条件路由函数，不是 node。

## Checkpoint 与长期记忆

Checkpointer 保存的是**图 state 快照**（如某条 `thread_id` 下的 `messages`），用于续聊和会话隔离。

Checkpoint **不等于**长期记忆：它不决定"该记住什么、何时写入、如何检索和遗忘"。长期记忆还需要写入策略、权限和更新机制。

## 与 RAG 的衔接

LangGraph 图结构在接入 RAG 时通常不变：只是把 `retrieve` 当作又一个工具，`observation` 形态从 API 返回变成 chunk 片段 + 来源 + 分数。

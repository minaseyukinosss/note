# Week3：LangGraph + 可交付 Demo

## 本周目标

- Day 15-16：读 LangGraph Quickstart，用 **StateGraph** 重写 Week2 同一 Agent，对照 node / state / edge。
- Day 17-19：接入一个真工具（Tavily 搜索或本地读文件）+ `SqliteSaver` 跨轮记忆。
- Day 20-21：选一个场景交付 Demo（README + 示例对话 + Langfuse trace）。

## 前置

- 完成 [Week2](../week2-react-agent/README.md)（尤其 [`react_agent.py`](../week2-react-agent/code/react_agent.py) 与 [Week2 总结](../week2-react-agent/notes/week2-总结.md)）。
- 主题根目录已安装依赖（Week3 新增 LangGraph 相关包）：

```bash
cd ai-agent
source .venv/bin/activate
pip install -r requirements.txt
```

## 笔记 `notes/`

- [Day 15-16 LangGraph 学习笔记](./notes/day15-16-langgraph学习笔记.md)（与裸写逐行对照 + Quickstart 导读）
- [Day 15-16 复盘](./notes/day15-16-复盘.md)（StateGraph 复盘 + 条件边理解）
- [Day 17-19 真工具与记忆](./notes/day17-19-真工具与记忆.md)（Tavily / 读文件 + Checkpointer）
- [Day 20-21 Demo 交付指南](./notes/day20-21-demo交付指南.md)（场景选型 + Langfuse）

## 代码 `code/`

环境变量与 Week1/Week2 相同，读 `ai-agent/.env`。

```bash
cd code
python langgraph_agent.py          # Day 15-16：与 Week2 同功能
python checkpoint_demo.py          # Day 17-19：多轮记忆示例
```

| 文件 | 对应天数 | 说明 |
| --- | --- | --- |
| `langgraph_agent.py` | Day 15-16 | StateGraph：`agent` ↔ `tools` 两节点 + 条件边 |
| `checkpoint_demo.py` | Day 17-19 | `SqliteSaver` 同一 `thread_id` 续聊 |
| `tools.py` | — | 三工具（与 Week2 行为一致） |
| `config.py` | — | `ChatOpenAI`（兼容 DeepSeek Base URL） |

## 裸写 vs LangGraph 对照

| Week2 `react_agent.py` | Week3 LangGraph |
| --- | --- |
| `messages` 列表 | `AgentState.messages`（`add_messages`  reducer） |
| `for step in range(max_steps)` | 图循环：`agent → tools → agent → …` |
| `client.chat.completions.create` | `call_model` 节点 |
| `dispatch_tool` + append `tool` | `ToolNode(ALL_TOOLS)` 节点 |
| `if not msg.tool_calls: return` | 条件边 `route_after_model` → `END` |
| `max_steps` | `recursion_limit`（invoke 时配置） |

## 验收清单

- [ ] 能口头解释：node = 一步操作，state = `messages`，edge = 下一步走哪。
- [ ] `langgraph_agent.py` 能回答与 Week2 相同的多步问题（天气 + 计算 + 搜索）。
- [ ] 对比 Week2：框架少写了循环骨架，但「心算跳过 calculator」仍可能出现。
- [ ] `checkpoint_demo.py` 同一 `thread_id` 第二轮能引用上一轮上下文。
- [ ] Day 20-21 选定场景并跑通 Langfuse trace（见交付指南）。

## 与 Week2 的关系

Week2 证明你理解协议与循环；Week3 证明你能**用图组织同一逻辑**，并为真工具、持久化、可观测性留扩展点。模型行为问题（乱选工具、跳过工具）两周一视同仁——区别在工程结构，不在「变聪明」。

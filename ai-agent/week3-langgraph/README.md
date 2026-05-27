# Week3：LangGraph + Checkpoint + Trace

## 本周目标

- Day 15-16：读 LangGraph Quickstart，用 **StateGraph** 重写 Week2 同一 Agent，对照 node / state / edge。
- Day 17-19：接入一个真工具（Tavily 搜索或只读文件工具）+ `SqliteSaver` checkpoint。
- Day 20-21：交付一个最小 Demo，包含示例对话、trace / messages 日志和失败用例。

## 本周主线

```text
Week2 手写 ReAct
    ↓  同一逻辑图形化
Day 15-16 StateGraph：state / node / edge
    ↓  接真实世界与持久化
Day 17-19 Tavily / 文件工具 + checkpoint
    ↓  交付意识
Day 20-21 Demo + trace + README
```

Week3 的关键判断：LangGraph 改善的是工程组织、持久化和可观测性，不会让同一个模型突然更会推理。RAG 和长期记忆不要塞进 Week3，放到 Week4 更稳。

## 本周总结

- [05 本周总结](./notes/05-本周总结.md)（LangGraph 对照、Checkpointer、trace、Demo 验收）
- [跨周评估用例](../05-评估用例.md)（对比 Week2 裸写版与 Week3 LangGraph 版）

## 前置

- 完成 [Week2](../week2-react-agent/README.md)（尤其 [`react_agent.py`](../week2-react-agent/code/react_agent.py) 与 [05 本周总结](../week2-react-agent/notes/05-本周总结.md)）。
- 主题根目录已安装依赖（Week3 新增 LangGraph 相关包）：

```bash
cd ai-agent
source .venv/bin/activate
pip install -r requirements.txt
```

## 笔记 `notes/`

- [00 知识地图](./notes/00-知识地图.md)（手写 ReAct → LangGraph → Checkpointer → Demo）
- [01 学习手册](./notes/01-学习手册.md)（当天唯一入口：任务、命令、观察点、关键结论和记录区）
- [02 概念详解](./notes/02-概念详解.md)（state / node / edge / checkpointer / trace）
- [03 实验与踩坑](./notes/03-实验与踩坑.md)（recursion limit、thread 隔离、Tavily、trace）
- [05 本周总结](./notes/05-本周总结.md)（三周收束 + 下一阶段建议）

## Demo 交付 `demo/`（Day 20-21）

- [Demo 交付索引](./demo/README.md)
- [示例对话](./demo/示例对话.md)
- [trace 记录](./demo/trace.md)
- [边界用例](./demo/边界用例.md)
- [评估记录](./demo/评估记录.md)

## 代码 `code/`

环境变量与 Week1/Week2 相同，读 `ai-agent/.env`。

```bash
cd code
python langgraph_agent.py          # Day 15-16：与 Week2 同功能
python checkpoint_demo.py          # Day 17-19：多轮记忆示例
python checkpoint_amnesia_demo.py  # 可选：换 thread_id 验证“失忆”
python news_demo.py                # Day 20-21：Demo 交付脚本
```

| 文件 | 对应天数 | 说明 |
| --- | --- | --- |
| `langgraph_agent.py` | Day 15-16 | StateGraph：`agent` ↔ `tools` 两节点 + 条件边 |
| `checkpoint_demo.py` | Day 17-19 | `SqliteSaver` 同一 `thread_id` 续聊 |
| `checkpoint_amnesia_demo.py` | Day 17-19 | 换 `thread_id` 验证 checkpoint 隔离 |
| `news_demo.py` | Day 20-21 | Demo 交付脚本（搜索 + checkpoint 续聊） |
| `tools.py` | — | 天气 mock、计算器、Tavily 搜索工具 |
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
- [ ] `checkpoint_amnesia_demo.py` 换 `thread_id` 后能观察到上下文隔离。
- [ ] Day 20-21 选定场景并跑通 Langfuse trace（见 `01-学习手册.md`）。
- [ ] 能解释：checkpoint 存的是 state 快照，不是模型“长期记忆”。
- [ ] 至少复跑 `05-评估用例.md` 中 W2-001 与 W3-001，对比裸写版和 LangGraph 版的工具路径。
- [ ] 能说明：外部搜索 / 文件内容只能当数据，不能当系统规则。

## 与 Week2 的关系

Week2 证明你理解协议与循环；Week3 证明你能**用图组织同一逻辑**，并为真工具、持久化、可观测性留扩展点。模型行为问题（乱选工具、跳过工具）两周一视同仁——区别在工程结构，不在「变聪明」。

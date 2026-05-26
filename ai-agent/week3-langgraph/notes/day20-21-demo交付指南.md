# Day 20-21：Demo 交付指南

## 背景 / 学习目标

- 选一个**小场景**做完整 Agent Demo（不是再写教程，是能给别人演示的东西）。
- README 写清：能做什么、怎么跑、3 个示例对话。
- 用 [Langfuse 云版](https://cloud.langfuse.com/) 接 trace，至少看过一次完整调用链。

## 场景选型

| 场景 | 难度 | 工具建议 | 适合谁 |
| --- | --- | --- | --- |
| 每日科技新闻摘要 | ⭐ | Tavily + 总结 | 想练搜索与摘要 |
| 个人记账助手 | ⭐⭐ | SQLite 读写 | 想练结构化数据 |
| 简易代码 Reviewer | ⭐⭐ | `read_file` + LLM | 已有 sandbox 读文件基础 |

**原则**：3 周内选 ⭐ 或 ⭐⭐ 一个就够；做深一个比浅做三个有价值。

## 交付物清单

```
week3-langgraph/code/
├── your_demo_agent.py    # 或扩展现有 langgraph_agent.py
├── sandbox/              # 若做 Reviewer
└── README 片段写在 week3 README 或单独 notes/demo-xxx.md

notes/
└── demo-交付记录.md      # 3 条示例问答 + Langfuse 截图说明
```

### README 必含三节

1. **能做什么** — 一句话 + 3 条能力 bullet。
2. **怎么跑** — `cd`、`.env` 变量、`python xxx.py`。
3. **示例对话** — 3 条真实输入与输出（可文字，截图更好）。

## Langfuse 接入（最小步骤）

1. 注册 Langfuse Cloud，创建 project，拿 `PUBLIC_KEY` / `SECRET_KEY` / `HOST`。
2. `.env` 增加：

```bash
LANGFUSE_PUBLIC_KEY=pk-...
LANGFUSE_SECRET_KEY=sk-...
LANGFUSE_HOST=https://cloud.langfuse.com
```

3. 安装（已写入主题 `requirements.txt` 时跳过）：

```bash
pip install langfuse
```

4. 在 Demo 入口加 callback（LangChain 集成示例）：

```python
from langfuse.callback import CallbackHandler

handler = CallbackHandler()
graph.invoke(
    {"messages": [...]},
    config={
        "callbacks": [handler],
        "configurable": {"thread_id": "demo-1"},
    },
)
```

5. 跑一条多步对话，在 Langfuse UI 里确认能看到：**每次 LLM 调用、每次 tool 执行、总耗时**。

### trace 能看清 / 看不清什么

| 能看清 | 看不清 |
| --- | --- |
| 每步 input/output、tool 名与参数 | 模型「内心」未输出的推理 |
| 延迟、token（若 provider 回传） | 换 prompt 后的长期效果 — 需评估集 |
| 哪一步选错工具 | 业务上「答对了吗」— 需人工或自动评分 |

## 3 周结业自测（口头）

对照 [`小白入门`](../../小白入门.md) 第六节，Week3 重点补：

5. LangGraph 的 state / node / edge 对应裸写什么？
6. trace 能帮你看清什么、看不清什么？

前 4 题在 [Week2 总结](../../week2-react-agent/notes/week2-总结.md) 已覆盖。

## 验收

- [ ] Demo 脚本一键可跑（依赖与 `.env` 写进 README）。
- [ ] 3 条示例对话已记录。
- [ ] Langfuse 上至少 1 条完整 trace 截图或链接说明。
- [ ] 能解释：若 Agent 答错，你会先查 trace 里哪一步。

## 小结

Day 20-21 是把「会写 Agent」变成「能交付、能观测、能排错」。完成后可按 [`学习路线`](../../学习路线.md) 继续 RAG / 评估，或读 [`资料汇总`](../../资料汇总.md) 论文列表 — **单 Agent 玩明白后再碰多 Agent**。

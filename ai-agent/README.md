# AI Agent

> 系统学习 LLM-based Agent：从 Prompt 工程 → 工具调用 → 多 Agent 协作 → 评估与上线。

## 学习目标

- 理解 Agent 的本质：`LLM + 工具 + 记忆 + 规划` 的闭环。
- 掌握主流 Agent 范式（ReAct、Plan-and-Execute、Reflection、Multi-Agent）。
- 熟练使用至少一个主流框架（LangGraph / AutoGen / CrewAI 任选其一）。
- 能独立设计、实现并评估一个真实场景的 Agent。

## 实践项目

| 周次 | 说明 | 入口 |
| --- | --- | --- |
| Week1 | LLM 调用 + 多轮对话 + Function Calling | [`week1-hello-llm/`](./week1-hello-llm/README.md) |
| Week2 | 手写 ReAct Agent（纯 openai SDK） | [`week2-react-agent/`](./week2-react-agent/README.md) |
| Week3 | LangGraph 重写 + 记忆 + Demo 交付 | [`week3-langgraph/`](./week3-langgraph/README.md) |

## 笔记索引

| 文档 | 内容 |
| --- | --- |
| [小白入门](./小白入门.md) | **零基础首选**：3 周到第一个能跑的 Agent，每日任务清单 |
| [学习路线](./学习路线.md) | 6 阶段路线图，每阶段含目标、产出、推荐资料 |
| [核心概念](./核心概念.md) | ReAct、Tool Use、RAG、Memory 等关键概念速查 |
| [资料汇总](./资料汇总.md) | 论文、课程、框架文档、开源项目 |

## 学习方法

- **读 + 写 + 跑**：读论文/文档 → 写笔记 → 跑最小 demo，三步缺一不可。
- **先窄后宽**：先吃透 ReAct 一种范式，再横向对比其他。
- **追源码**：成熟框架（LangGraph、AutoGen）的核心循环代码通常只有几百行，值得逐行读。
- **建立评估意识**：从写第一个 Agent 起，就要思考"怎么判断它好/坏"。

## 前置要求

- Python 基础（async、装饰器、类型注解）。
- 至少调用过一次 OpenAI / Anthropic / 国产大模型 API。
- 了解 Prompt Engineering 基础（System Prompt、Few-shot、CoT）。

## Python 环境（全主题共用，装一次即可）

需要 **Python ≥ 3.10**（macOS 推荐 `python3.12`）。各 week **共用** 同一虚拟环境与 `.env`，不用每周重装或切换。

```bash
cd ai-agent
python3.12 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env               # 填入 API Key，所有 week 自动读取
```

之后任意 week 的代码目录直接跑（已激活 venv 时）：

```bash
python week1-hello-llm/code/hello.py
python week2-react-agent/code/react_agent.py
python week3-langgraph/code/langgraph_agent.py
```

未 `activate` 时，用绝对路径也行：

```bash
ai-agent/.venv/bin/python week2-react-agent/code/react_agent.py
```

`code/.env` 仍可单独配置，会覆盖主题级 `ai-agent/.env`。

## 后续扩展

实战项目落地时，按仓库约定拆为：

```
ai-agent/
├── notes/   # 现有 .md 迁入
└── code/
    ├── react-agent-from-scratch/
    ├── langgraph-research-agent/
    └── ...
```

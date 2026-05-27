# AI Agent

> 系统学习 LLM-based Agent：从 LLM 调用 → 工具协议 → ReAct 循环 → 图编排 → RAG / 记忆 → 评估与上线。

## 学习目标

- 理解 Agent 的本质：`LLM + 状态 + 工具 + 自主决策循环`；记忆、规划、多 Agent 都是可选增强。
- 区分普通 LLM 调用、augmented LLM、workflow 和真正 Agent，避免把所有 LLM 应用都叫 Agent。
- 掌握入门阶段最关键的 ReAct、tool use、state、trace、eval 和工具权限边界。
- 熟练使用 LangGraph 组织一个可恢复、可观测、可测试的单 Agent。
- 能独立设计、实现并评估一个小而完整的 Agent 场景。

## 实践项目

| 周次 | 说明 | 入口 |
| --- | --- | --- |
| Week1 | LLM 调用 + 多轮对话 + Function Calling | [`week1-hello-llm/`](./week1-hello-llm/README.md) |
| Week2 | 手写 ReAct Agent（纯 openai SDK） | [`week2-react-agent/`](./week2-react-agent/README.md) |
| Week3 | LangGraph 重写 + checkpoint + trace + 最小 Demo | [`week3-langgraph/`](./week3-langgraph/README.md) |
| Week4 | RAG / 长期记忆 + 引用 + 评估集 | 建议下一步新增 |

## 推荐阅读顺序

如果你是第一次进入这个主题，按下面顺序读：

1. [`01-小白入门`](./01-小白入门.md)：先跟着 3 周计划跑通最小 Agent。
2. [`week1-hello-llm`](./week1-hello-llm/README.md) → [`week2-react-agent`](./week2-react-agent/README.md) → [`week3-langgraph`](./week3-langgraph/README.md)：边读边跑代码。
3. [`03-核心概念`](./03-核心概念.md)：遇到 ReAct、workflow、memory、RAG 等概念时回查。
4. [`02-学习路线`](./02-学习路线.md)：完成 3 周后，继续进入 RAG、评估、上线和综合项目。
5. [`07-学习审核报告`](./07-学习审核报告.md)：看当前项目结构的专业诊断和后续优化优先级。
6. [`06-笔记整理规范`](./06-笔记整理规范.md)：写新笔记或复盘时按这个模板整理。

## 笔记索引

| 文档 | 内容 |
| --- | --- |
| [01-小白入门](./01-小白入门.md) | **零基础首选**：3 周到第一个能跑的 Agent，每日任务清单 |
| [02-学习路线](./02-学习路线.md) | 6 阶段路线图，每阶段含目标、产出、推荐资料 |
| [03-核心概念](./03-核心概念.md) | ReAct、Tool Use、RAG、Memory 等关键概念速查 |
| [04-资料汇总](./04-资料汇总.md) | 论文、课程、框架文档、开源项目 |
| [05-评估用例](./05-评估用例.md) | Week2 起跨模型 / 跨框架复用的回归测试集 |
| [06-笔记整理规范](./06-笔记整理规范.md) | 后续笔记模板、复盘规则、Agent 专用检查表 |
| [07-学习审核报告](./07-学习审核报告.md) | 当前学习项目的结构诊断、问题和优化优先级 |

## 当前状态

- 已完成：Week1-Week3 的主线笔记、代码示例、每周总结和验收清单。
- 已优化：补齐项目审核报告、笔记整理规范、评估用例入口和 checkpoint 产物忽略规则。
- 路线调整：Week3 聚焦 LangGraph / checkpoint / trace，不再把 RAG 和长期记忆塞进入门 3 周。
- 下一阶段建议：新增 `week4-rag-memory/`，把 Week3 Agent 扩展为带本地知识库、引用来源和基础 eval 的 Agent。

## 知识结构

建议把 AI Agent 的知识分成 7 层看：

1. **模型与上下文**：模型能力、token、context window、结构化输出、streaming。
2. **工具接口**：function calling / tool use、参数 schema、工具错误返回、权限边界。
3. **状态与循环**：`messages`、scratchpad、工具 observation、停止条件、最大步数。
4. **架构分型**：单次 LLM 调用 → augmented LLM → workflow → agent。固定路径优先 workflow，路径需要模型动态决定时才上 agent。
5. **可观测与评估**：trace、固定用例、工具调用正确率、轨迹回放、失败分类。
6. **能力增强**：短期记忆、长期记忆、RAG、计划、反思、多 Agent、MCP / 外部工具生态。
7. **工程约束**：成本、延迟、缓存、重试、human-in-the-loop、部署边界。
8. **安全边界**：prompt injection、越权工具调用、数据泄漏、敏感操作确认。

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

建议下一阶段继续沿用按周拆分的结构，先补一个 RAG + 评估闭环：

```
ai-agent/
└── week4-rag-memory/
    ├── README.md
    ├── notes/
    │   ├── 00-知识地图.md
    │   ├── 01-学习手册.md
    │   ├── 02-概念详解.md
    │   ├── 03-实验与踩坑.md
    │   └── 05-本周总结.md
    └── code/
```

Week4 的最小目标：给 Week3 Agent 增加本地 markdown 知识库检索工具，回答时返回引用来源，并把固定问题记录到 [`05-评估用例.md`](./05-评估用例.md)。

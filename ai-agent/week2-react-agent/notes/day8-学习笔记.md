# Day 8-9：读懂 ReAct 与 Agent 范式

## 背景 / 学习目标

- 只读一篇博文：[Anthropic - Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)（约 20 分钟）。
- 搞懂 **augmented LLM**、**Workflow vs Agent**、**ReAct 一句话**。
- 为 Day 10-12 手写循环打底——先建立地图，再写代码。

## 今日操作

1. 打开上面链接，通读正文 + Appendix 2（工具 prompt 工程）。
2. 对照下面「导读问题」自测；读完后核对参考答案，错的标 ⭐ 周末重读。
3. （可选）翻 Week1 的 `function_calling_demo.py`，问自己：若要多调几次工具，循环该怎么改？

## 核心概念

### Anthropic 博文没提 ReAct，ReAct 从哪来？

Day 8-9 **故意拆成两件事**，容易误以为「读完 Anthropic 就该知道 ReAct 叫什么」——其实不会。

| 来源 | 教什么 | 有没有写 ReAct |
| --- | --- | --- |
| [Anthropic - Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) | Workflow / Agent / augmented LLM；**工程视角** | ❌ 没写这个词 |
| 本仓库 [`核心概念.md`](../../核心概念.md)、[`资料汇总.md`](../../资料汇总.md) | **ReAct** 作为学术范式名 | ✅ |
| 论文 [ReAct (2022)](https://arxiv.org/abs/2210.03629) | Thought → Action → Observation 循环 | ✅ 名词出处 |

**对应关系：** Anthropic 在「Agents」一节写的：

> *They are typically just LLMs using tools based on environmental feedback in a loop.*

这就是 ReAct 想表达的**程序结构**——LLM 在循环里用工具、读环境反馈（tool 返回值），直到任务完成。Anthropic 用产品/工程语言描述；**ReAct 是学术界给同一类结构起的名字**（Reason + Act）。

| Anthropic 博文 | ReAct 论文（2022） | 你 Week2 写的代码 |
| --- | --- | --- |
| Agent in a loop | Thought → Action → Observation → … | `for step in range(max_steps)` |
| tool call results = ground truth | Observation | `role: tool` 的 `content` |
| environmental feedback | 环境反馈 | `dispatch_tool(...)` 返回值 |
| stopping conditions (max iterations) | 循环终止 | `max_steps` / 无 `tool_calls` |

**现代实现和论文的差别（背景了解即可）：** 早期论文常让模型在正文里写 `Thought:` / `Action:` / `Observation:`，你再正则解析。本仓库 Week1/Week2 用的是 **Function Calling**：`tool_calls` + `role: tool`——**循环一样，通信格式不同**；你只写后者，不必写 `Action:` 文本解析。

**Day 8-9 怎么读：** 博文建立「该不该用 Agent、和 Workflow 啥区别」；ReAct 名字和 Thought-Action-Observation 链条看 [`核心概念.md`](../../核心概念.md) 或论文摘要即可；**Day 10 写循环时**，对照 Week1 的 `function_calling_demo.py` 就是落地。

### ReAct 一句话

> **让 LLM 在循环里反复「思考 → 调工具 → 观察结果」，直到它不再返回 `tool_calls`、直接给出最终回答为止。**

对应 Week1 你已见过的协议：

```text
messages + tools → assistant(tool_calls) → 你执行 → role=tool → 再请求 → … → assistant(content)
```

Week1 的 demo 只循环 **1 次**工具；Week2 用 `for step in range(max_steps)` 包住整段，就是最小 ReAct Agent。

### augmented LLM 是什么？

Anthropic 文中的 **augmented LLM（增强型 LLM）** = 普通 LLM + 三类外挂能力：

| 增强 | 含义 | 例子 |
| --- | --- | --- |
| **Retrieval** | 主动查资料 | RAG、搜索 API |
| **Tools** | 调用外部函数 | Function Calling、`get_weather` |
| **Memory** | 决定保留什么信息 | `messages` 列表、向量库 |

模型会**自己决定**何时检索、调哪个工具、记什么——前提是你把接口设计清楚。  
Workflow 和 Agent 都建立在这个积木之上；差别在于**谁决定下一步**。

### Workflow 和 Agent 的区别

| | **Workflow（工作流）** | **Agent（智能体）** |
| --- | --- | --- |
| **谁编排** | 你的代码（预定义路径） | LLM 动态决定 |
| **步骤** | 固定或半固定（链式、路由、并行…） | 步数不可预测，靠循环 + 工具反馈 |
| **优点** | 可预测、好调试、 latency 可控 | 灵活，适合开放问题 |
| **代价** | 灵活性低 | 更贵、可能 compound errors |
| **例子** | Prompt chaining、Routing、Orchestrator-workers | 编码 Agent、多步问答 + 多工具 |

Anthropic 原话：

- **Workflows**：LLM 和工具通过**预定义的代码路径**编排。
- **Agents**：LLM **动态 directing** 自己的流程和工具使用。

### 什么时候该用 Agent？

博文建议：**能不用就不用**。优先：

1. 单次 LLM + 检索 / Few-shot 能否搞定？
2. 不行 → 先试 Workflow（链式、路由）。
3. 仍不行 → 且任务开放、步数难预测 → 再上 Agent。

Agent 适用：开放问题、需要多轮工具、环境能给 ground truth（工具返回值、测试通过与否）。

### 与 Week2 代码的对应

| 概念 | Week2 `react_agent.py` 里 |
| --- | --- |
| augmented LLM | `tools=` + `messages`（短期记忆） |
| Agent 循环 | `run_agent` 里的 `for step in range(max_steps)` |
| 退出条件 | `not msg.tool_calls` → 返回 `content` |
| 安全阀 | `max_steps` 防止死循环 |
| ACI（Agent-Computer Interface） | `TOOLS` 里每个工具的 `description` / `parameters` |

Appendix 2 重点：**工具文档和 system prompt 一样重要**——模型靠 description 决定调不调、调哪个。

## 导读问题（读完后自测）

### Q1：augmented LLM 是什么意思？

**参考答案：** 在基础 LLM 上增加 retrieval、tools、memory 等能力，并让模型能主动使用它们（自己发查询、选工具、决定记什么）。它是构建 Workflow 和 Agent 的**最小积木**，本身还不一定是「自主循环」。

### Q2：Workflow 和 Agent 的区别是什么？

**参考答案：** Workflow 里**下一步走哪条分支由你的代码写死**（链式、路由、并行等）；Agent 里**下一步调什么工具、做几步由 LLM 根据当前 `messages` 和工具结果动态决定**，通常是一个 LLM + tools + 环境反馈的循环。

### Q3：ReAct 和 Week1 Function Calling 差在哪？

**参考答案：** 协议相同（都是 `tool_calls` + `role: tool`）；ReAct 把「请求 → 执行 → 塞回」放进**循环**，支持多步；Week1 demo 只演示一轮工具。

### Q4：为什么 Anthropic 建议先裸写 API 再上手框架？

**参考答案：** 框架多一层抽象，容易看不清底层 prompt/response，调试困难；很多模式几十行就能实现。Week2 正是裸写循环，为第 3 周 LangGraph 做对照。

## 易错点 / 易混淆点

- ❌ 把 ReAct 当成新模型 → ✅ 是一种**程序结构**（循环 + Function Calling）。
- ❌ 一上来就 Multi-Agent → ✅ 单 Agent 循环跑通再扩展。
- ❌ 出问题只改 system prompt → ✅ 先**打印完整 `messages`**，看是哪一步 tool 选错或 observation 格式不对。

## 小结

Day 8-9 不写代码也正常。读完后应能说出：

1. **Agent = augmented LLM + 自主循环**（LLM 决定何时停、调什么）。
2. **ReAct = Week1 两轮协议 × N 次**，直到无 `tool_calls`。
3. **Workflow 你定路径，Agent 模型定路径**——复杂度递增，按需选用。

下一步：Day 10 打开 [`../code/react_agent.py`](../code/react_agent.py)，补完 `run_agent`。

## 相关笔记

- [Day 8-9 自测复盘](./day8-自测复盘.md)（概念测验错题标注 + 规范答案）

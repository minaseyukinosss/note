# Day 8-9 自测复盘

## 背景 / 学习目标

- 巩固 Day 8-9 概念自测（5 题，得分 **3.5 / 5**）。
- 标注答错或表述不准之处，便于复习。
- 每题附规范答案。

## 总评

| 已掌握 | 需加强 |
| --- | --- |
| augmented LLM 三块能力（检索 / 工具 / 记忆） | augmented LLM ≠ Agent，对比对象不是「ChatGPT 有没有自主能力」 |
| Workflow vs Agent 谁定路径 | Agent 例子不要用「AI 聊天」，应换成多步 + 多工具 |
| ReAct = Week1 协议 × 循环 | 退出是「不调工具」，不是「不调模型」 |
| 简单任务别上 Agent（Q5 全对） | 多步场景下 messages 有多条 assistant / tool |

---

## Q1：什么是 augmented LLM？和普通聊天差在哪？

### 我的答案

> augmented LLM 就是增强型的 LLM，具有自主的检索、工具调用以及记忆能力，跟 ChatGPT 聊天差在 ChatGPT 没有自主能力。

### 标注

| 部分 | 对错 |
| --- | --- |
| 增强型 LLM + 检索 / 工具 / 记忆 | ✅ 正确 |
| 「ChatGPT 没有自主能力」 | ❌ 不准确 |

### 错在哪

- 对比对象应是 **「只有 messages 的单次聊天」**，不是「ChatGPT 这个产品」——ChatGPT 也有带工具的模式。
- **augmented LLM 是积木**，有 tools 接口 ≠ 已经是 Agent；Agent 还要在外面套 **循环**。

### 规范答案

**augmented LLM（增强型 LLM）** = 基础 LLM + 三类外挂能力：

| 能力 | 含义 |
| --- | --- |
| **Retrieval** | 检索外部资料（RAG、搜索） |
| **Tools** | Function Calling，调用外部函数 |
| **Memory** | 决定保留什么信息（如 `messages`、向量库） |

与普通单次聊天的区别：**普通聊天只有 `messages`；augmented LLM 还把 retrieval / tools / memory 的接口接好，让模型能主动用这些能力。** Workflow 和 Agent 都建立在这个积木之上。

---

## Q2：Workflow 和 Agent 各举一例，谁决定下一步？

### 我的答案

> Workflow 由代码决定路径，适用于特定场景，例如翻译；Agent 由 LLM 决定路径，适用于比较分散开发的场景，例如 AI 聊天。

### 标注

| 部分 | 对错 |
| --- | --- |
| Workflow：代码定路径，翻译例子 | ✅ 正确 |
| Agent：LLM 定路径 | ✅ 正确 |
| 例子「AI 聊天」 | ❌ 不合适 |
| 「比较分散开发的场景」 | ❌ 表述不清 |

### 错在哪

- **闲聊**通常一次 LLM 就够，不需要 Agent。
- Agent 适合 **开放、多步、步数难预测** 的任务，不是「分散开发」。

### 规范答案

| 类型 | 谁决定下一步 | 典型例子 |
| --- | --- | --- |
| **Workflow** | **你的代码**（预定义路径） | 先翻译再润色（固定 2 步 Prompt chaining）；客服路由（退款 / 技术 / 一般问题走不同分支） |
| **Agent** | **LLM**（根据 `messages` 和工具结果动态决定） | 「查北京天气 + 算 23×47」；编码 Agent 按任务改多个文件；多源搜索再汇总 |

**背一句：** Workflow 你定路径，Agent 模型定路径。

---

## Q3：Week1 Function Calling 和 ReAct 一样吗？差在哪？

### 我的答案

> 一样的，差在 ReAct 是套在循环里的，由 LLM 决定什么时候不调用模型。

### 标注

| 部分 | 对错 |
| --- | --- |
| 协议一样 | ✅ 正确 |
| ReAct 套在循环里 | ✅ 正确 |
| 「什么时候不调用**模型**」 | ❌ 应为「不调用**工具**」 |

### 错在哪

- 循环里 **每一轮都会调用模型**（`chat.completions.create`）。
- 退出条件是：返回的 `message` **没有 `tool_calls`**，直接给最终 `content`——表示不再调工具，可以回答了。

### 规范答案

| 维度 | Week1 `function_calling_demo.py` | ReAct Agent |
| --- | --- | --- |
| **协议** | 相同：`tool_calls` + `role: tool` + observation | 相同 |
| **结构** | 固定 **1 次**工具 + **1 次**最终回答 | **`for` / `while` 循环**，可多次工具 |
| **退出** | 第 2 轮无 `tool_calls` 即结束 | 某一轮无 `tool_calls` 即 `return content` |
| **谁决定停** | 模型通过「不再输出 `tool_calls`」表示完成 | 同上 |

**背一句：** 协议相同；ReAct = Week1 两轮协议 × N 次；停的是调 **工具**，不是调 **模型**。

---

## Q4：「北京天气 + 23×47」跑完后，messages 里有哪些 role？

### 我的答案

> system、user、assistant、tool

### 标注

| 部分 | 对错 |
| --- | --- |
| 四种 role 名字 | ✅ 没错 |
| 只列 4 条、各一条 | ❌ 不完整 |

### 错在哪

- 多步任务会有 **多条** `assistant` 和 **多条** `tool`。
- 只列 4 条像 Week1 只调 **1 次**工具的情况。

### 规范答案

典型顺序（2 次工具、1 次最终回答）：

```text
1. system          — 定规矩
2. user            — 用户问题
3. assistant       — 含 tool_calls（如 get_weather），通常几乎无 content
4. tool            — 天气 observation
5. assistant       — 含 tool_calls（如 calculator）
6. tool            — 计算结果 observation
7. assistant       — 只有 content，无 tool_calls → 最终回答，循环结束
```

要点：

- 每调一次工具 ≈ 一对 `assistant(tool_calls)` + `tool`
- 最后一条 `assistant` 才是给用户看的最终人话
- 若一轮调多个工具，会有 **1 个 assistant + 多个 tool**

---

## Q5：哪种情况不该上 Agent？

### 我的答案

> A，场景、步骤都确定，用 Workflow 就行。D 也是。

### 标注

**✅ 全对，无错处。**

### 规范答案

| 选项 | 是否该上 Agent | 理由 |
| --- | --- | --- |
| **A** 先翻译再润色，永远 2 步 | ❌ 不该 | 路径固定 → **Workflow**（Prompt chaining） |
| **B** 查天气 + 计算 + 搜索，步数不确定 | ✅ 适合 | 开放多步 → Agent |
| **C** 客服查订单 + 退款 + 多轮 | ✅ 常适合 | 要工具 + 多轮 → agentic 系统 |
| **D** 500 字压缩成 3 句 | ❌ 不该 | 单次 LLM 调用即可 |

**原则：** 能一次 prompt 解决就不要上 Agent；步骤能写死就优先 Workflow。

---

## 错题速查表

| 题号 | 我的误区 | 规范说法 |
| --- | --- | --- |
| Q1 | ChatGPT 没有自主能力 | 对比「只有 messages 的单次调用」；augmented LLM 是积木，不等于 Agent |
| Q2 | Agent 例子 = AI 聊天 | Agent 例子 = 多步 + 多工具 + 步数不确定 |
| Q3 | 不调用**模型** | 每轮都调模型；退出 = 不再输出 **tool_calls** |
| Q4 | 只有 4 条 role | 多步有多条 assistant / tool；最后一条 assistant 才是最终回答 |
| Q5 | — | 已掌握 |

---

## 5 题规范答案（一页背完）

1. **augmented LLM** = LLM + retrieval + tools + memory；比普通单次聊天多了这些可调用接口；本身还不一定是 Agent。
2. **Workflow** = 代码定路径（如固定翻译链）；**Agent** = LLM 定路径（如天气 + 计算 + 搜索）。
3. **协议相同**；ReAct 把 Function Calling **放进循环**；模型用「无 tool_calls」表示任务完成。
4. **messages** = system → user → (assistant + tool) × N → assistant（最终 content）。
5. **不该上 Agent**：步骤固定的 Workflow 任务（A）、单次 LLM 能搞定的（D）。

## 小结

Day 8-9 概念自测可进入 Day 10：补完 [`../code/react_agent.py`](../code/react_agent.py) 里的 `run_agent`，对照 Week1 的 `function_calling_demo.py`，亲手打印 `messages` 验证 Q4 的多步结构。

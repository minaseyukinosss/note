# Day 10-12：`react_agent.py` 学习笔记

## 背景 / 学习目标

- 对照 Week1 [`function_calling_demo.py`](../../week1-hello-llm/code/function_calling_demo.py)，把**固定两轮**改成 **`run_agent` 循环**。
- 用纯 `openai` SDK（无 LangChain）实现最小 ReAct Agent：天气 + 计算器 + 搜索（假数据）。
- 跑通 [`react_agent.py`](../code/react_agent.py) 后，能口头说清 `messages` 如何变长、循环何时退出。

## 今日操作

1. 补完 `run_agent` 中的 `for step in range(max_steps)` 循环。
2. 在 `code/` 目录运行：`python react_agent.py`，对照 `_print_step` 看每步 `messages`。
3. 逐条理解 `main()` 里四条 demo 在验证什么（见下文「验收用例」）。

## 文件结构在教什么

| 模块 | 作用 | 学什么 |
| --- | --- | --- |
| `SYSTEM_PROMPT` | 行为边界 | 何时用工具、何时直接答、无工具不编造 |
| `TOOLS` | 工具 schema | `description` 是模型选工具的主要依据 |
| `get_weather` / `calculator` / `search` | 真执行 | 模型只产出调用意图，Python 才执行 |
| `dispatch_tool` | 路由 | 解析 `arguments` JSON → 调用对应函数 |
| `run_agent` | ReAct 主循环 | 多轮 `create` + 累积 `messages` |
| `_print_step` | 调试 | 排错先看 messages，再改 prompt / 工具 |
| `main` | 四条用例 | 单工具、多步、工具报错、无能力需求 |

## 核心概念

### 和 Week1 的差别

```text
Week1 function_calling_demo：手写「第 1 轮」+「第 2 轮」——路径固定，最多一批 tool_calls
Week2 react_agent：for step in range(max_steps)——同一段逻辑重复，步数由任务决定
```

**协议没变，只是外面套了循环。** 每一步都是：

1. `client.chat.completions.create(..., messages=..., tools=TOOLS)`
2. `messages.append(msg.model_dump(exclude_none=True))`
3. 若 `not msg.tool_calls` → `return msg.content`（退出）
4. 对每个 `call`：`dispatch_tool` → append `role: tool`（带 `tool_call_id`）
5. 回到步骤 1

因此「北京天气 + 23×47」可以在**一次** `run_agent` 里先调 `get_weather` 再调 `calculator`，顺序由模型根据当前 `messages` 决定，不必在代码里写死。

### ReAct 在本文件里的对应

| 论文 / 概念 | `react_agent.py` 里是什么 |
| --- | --- |
| Action | 模型返回的 `tool_calls`（name + arguments JSON） |
| 执行 Action | `dispatch_tool(...)` |
| Observation | `role: tool` 的 `content`（工具返回值字符串） |
| 循环 | `for step in range(max_steps)` |
| 停止 | 本轮 `message` **没有** `tool_calls` |

### 本仓库写的是什么？（论文老格式 vs 你的代码）

**你只写了新协议，没有写、也不需要写老协议。**

| | 论文里的老写法（本仓库不实现） | 你的 `react_agent.py` |
| --- | --- | --- |
| 在干什么 | 循环：决定 → 调工具 → 看结果 → 再决定 | **一样**，`run_agent` 的 `for` |
| 模型怎么说要调工具 | 在聊天正文里写 `Action: ...`，你自己正则解析 | API 返回 `tool_calls` |
| 工具结果怎么还给模型 | 拼 `Observation: ...` 进 prompt | `role: tool` + `tool_call_id` |

**一句话：** **ReAct** = 这种循环在干什么；**Function Calling** = 循环里用什么字段传「调哪个工具」。Week1/Week2 练的都是 Function Calling；和论文里的 `Thought:` / `Action:` 文本不是一回事，也不必去实现。

### `messages` 是唯一状态

API 无状态：每轮都把**完整** `messages` 发回去。典型多步对话会长成：

```text
system → user → assistant(tool_calls) → tool → assistant(tool_calls) → tool → assistant(最终 content)
```

### 五条口头结论（背下来）

1. LLM **不执行**工具，只输出 `tool_calls`；`dispatch_tool` 才是执行。
2. `role: tool` 的 `content` 就是 **Observation**（环境反馈）。
3. 循环退出看 **本轮有没有 `tool_calls`**，不是「还调不调 API」——每步都要 `create`，只是可能不再调工具。
4. **Agent vs Workflow**：本文件没有写死「第一轮必天气、第二轮必计算」，路径由模型动态决定。
5. 工具 `description` 写不好，模型就会乱选或不选——当成给同事的 API 文档来写。

## 示例代码：`run_agent` 主循环

```python
for step in range(max_steps):
    response = client.chat.completions.create(
        model=model, messages=messages, tools=TOOLS,
    )
    msg = response.choices[0].message
    messages.append(msg.model_dump(exclude_none=True))

    if not msg.tool_calls:
        return msg.content or ""

    for call in msg.tool_calls:
        fn = call.function
        result = dispatch_tool(fn.name, fn.arguments)
        messages.append({
            "role": "tool",
            "tool_call_id": call.id,
            "content": result,
        })

    if verbose:
        _print_step(step, messages)

return f"超过最大步数 max_steps={max_steps}，未得到最终回答。"
```

源码位置：[`../code/react_agent.py`](../code/react_agent.py) 中 `run_agent` 函数。

## 工具层要点

### `calculator` 与错误 observation

除零、非法字符等返回**字符串错误**（如 `错误：除数不能为 0`），不抛异常打断循环。错误串进入 `messages` 后，模型应在下一步据此回答「算不出来」，而不是进程崩溃。

### `search` 假数据

第三个工具用于练习「模型在天气 / 计算 / 搜索之间自己选」，顺序不由代码写死。

### `SYSTEM_PROMPT` 控什么

1. 需要时调用工具  
2. 结果齐了之后用自然语言回答  
3. 无合适工具礼貌拒绝（订机票 demo）  
4. 不要编造  

## 验收用例（`main()` 四条 demo）

| 用户问题 | 验证点 |
| --- | --- |
| 北京今天天气怎么样？ | 单工具或一步工具 + 一步总结 |
| 北京今天天气怎么样？再帮我算 23 * 47 | 多步：至少经历「有 tool_calls → tool → 再请求」 |
| 100 除以 0 等于多少？ | observation 含错误信息，最终回答应承认算不了 |
| 帮我订一张明天去上海的机票 | 无对应工具，应拒绝而非编造航班 |

## 易错点 / 易混淆点

| 现象 | 原因 |
| --- | --- |
| API 报错或模型胡言 | 有 `tool_calls` 时未先 append **assistant**，或 `tool` 缺少 **`tool_call_id`** |
| 第二轮不再调工具 | 某轮 `create` 漏传 **`tools=TOOLS`** |
| 以为「6 步」才退出 | 退出条件是 **无 `tool_calls`**；`max_steps` 只是上限防死循环 |
| 工具失败整个 Agent 挂掉 | 应在工具内返回错误字符串作 observation，而不是未捕获异常 |
| 排错先改 prompt | 应先 **`_print_step` 看全量 messages**，定位是哪一步选错工具或 observation 不对 |

## 与 Day 8-9 的衔接

- Day 8-9 建立地图：Workflow / Agent / ReAct 一句话。  
- 本文件落地：Week1 协议 × `for` 循环 = 你能跑的 Agent。  
- 下一步 Day 13-14：故意 `max_steps=1`、5+ 步、无工具等问题，另写复盘笔记（见 Week2 README 本周目标）。

## 小结

`react_agent.py` 把 Week1 的 Function Calling **两轮协议**收成 **`run_agent` 一个循环**：请求 → 有 `tool_calls` 就执行并塞回 observation → 再请求，直到模型不再要工具。学会看 `messages` 变长过程，比背概念更接近真实排错方式。

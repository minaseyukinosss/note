# Week2：手写 ReAct Agent

## 本周目标

- Day 8-9：读懂 ReAct 与 Anthropic《Building Effective Agents》，区分 Workflow / Agent / augmented LLM。
- Day 10-12：纯 `openai` SDK 写出 Agent 循环（天气 + 计算器 + 可选 search）。
- Day 13-14：故意制造失败场景，写复盘笔记。

## 本周主线

```text
Week1 tool calling：固定两轮
    ↓  外面套循环
Day 10-12 ReAct：多轮工具调用，模型决定下一步
    ↓  主动制造失败
Day 13-14 复盘：知道哪些问题框架解决不了
```

Week2 的目标不是多接工具，而是把“协议 × 循环 × trace 排错 × eval 基线”吃透。

## 本周总结

- [05 本周总结](./notes/05-本周总结.md)（脉络、核心收获、踩坑、自测、与 Week3 衔接）
- [跨周评估用例](../05-评估用例.md)（固定输入、预期工具调用、失败原因记录）

## 笔记 `notes/`

- [00 知识地图](./notes/00-知识地图.md)（Function Calling → ReAct 循环 → Week3 图结构）
- [01 学习手册](./notes/01-学习手册.md)（当天唯一入口：任务、命令、观察点、关键结论和记录区）
- [02 概念详解](./notes/02-概念详解.md)（ReAct、状态、退出条件、Agent vs Workflow）
- [03 实验与踩坑](./notes/03-实验与踩坑.md)（`max_steps`、除零、跳过工具、多 tool_calls）
- [05 本周总结](./notes/05-本周总结.md)（脉络、核心收获、踩坑、自测、与 Week3 衔接）

## 代码 `code/`

环境在主题根目录 [`ai-agent/`](../README.md#python-环境全主题共用装一次即可) 统一配置，与 Week1 共用 `.venv` 和 `.env`。

```bash
cd code
python react_agent.py
```

| 文件 | 对应天数 | 说明 |
| --- | --- | --- |
| `react_agent.py` | Day 10-12 | ReAct 主循环（`run_agent` + 三工具 + demo） |
| `config.py` | — | 共用客户端与模型名（读 `.env`） |

## 环境变量

与 Week1 相同，推荐 `ai-agent/.env`；`code/.env` 可单独覆盖（勿提交 Git）：

```bash
OPENAI_API_KEY=sk-xxx
OPENAI_BASE_URL=https://api.deepseek.com
OPENAI_MODEL=deepseek-chat
```

## 验收清单

- [ ] 能口头解释：ReAct = while 循环里的「请求 → 调工具 → observation → 再请求」。
- [ ] 能区分 Workflow（代码定路径）与 Agent（LLM 动态决定下一步）。
- [ ] `react_agent.py` 能回答「北京今天天气，再帮我算 23 × 47」这类多步问题。
- [ ] 每一步能打印 `messages`，看清 LLM 如何选工具。
- [ ] 除以 0 时 Agent 能恢复或礼貌失败；无合适工具时不瞎编。
- [ ] 能解释 `max_steps` 是安全上限，不是正常完成条件。
- [ ] 能说出至少 2 个模型不可控现象：乱选工具、跳过工具、重复调用、提前总结。
- [ ] 至少跑过 `05-评估用例.md` 中 W2 开头的 4 条用例，并记录 Pass / Partial / Fail。
- [ ] 能说明哪些工具属于读操作、哪些属于高风险副作用操作。

## 进入 Week3 前

请确认你能回答：

1. `assistant(tool_calls)` 为什么必须先 append，才能 append `role: tool`？
2. 一轮里出现多个 `tool_calls` 时，`messages` 会怎么变？
3. 如果模型心算跳过 `calculator`，你会改 prompt、改工具，还是改成 workflow？

## 与 Week1 的关系

Week1 的 `function_calling_demo.py` 是**固定两轮**（调一次工具 → 最终回答）。  
Week2 把同样逻辑放进 **`for` / `while` 循环**，直到 `tool_calls` 为空——那就是 ReAct Agent。

# Week2：手写 ReAct Agent

## 本周目标

- Day 8-9：读懂 ReAct 与 Anthropic《Building Effective Agents》，区分 Workflow / Agent / augmented LLM。
- Day 10-12：纯 `openai` SDK 写出 Agent 循环（天气 + 计算器 + 可选 search）。
- Day 13-14：故意制造失败场景，写复盘笔记。

## 本周总结

- [Week2 总结](./notes/week2-总结.md)（脉络、核心收获、踩坑、自测、与 Week3 衔接）

## 笔记 `notes/`

- [Day 8-9 学习笔记](./notes/day8-学习笔记.md)（ReAct 概念 + Anthropic 博文导读）
- [Day 8-9 自测复盘](./notes/day8-自测复盘.md)（概念测验错题 + 规范答案）
- [Day 10-12 `react_agent.py` 学习笔记](./notes/day10-12-react_agent学习笔记.md)（主循环、工具层、与 Week1 对比）
- [Day 13-14 复盘](./notes/day13-14-复盘.md)（失败场景、工具跳过、Agent 本质三问）

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

## 与 Week1 的关系

Week1 的 `function_calling_demo.py` 是**固定两轮**（调一次工具 → 最终回答）。  
Week2 把同样逻辑放进 **`for` / `while` 循环**，直到 `tool_calls` 为空——那就是 ReAct Agent。

# Week1：LLM 调用与 Function Calling

## 本周目标

- Day 1-2：第一次 API 调用，理解 `system` / `user` / `assistant` 与 token。
- Day 3-4：终端多轮对话，实验 temperature 与 Few-shot。
- Day 5-7：Function Calling 完整链路（LLM 选工具 → 你执行 → 塞回结果）。

## 本周主线

```text
hello.py：单次请求
    ↓  把历史 messages 保存下来
chat.py：多轮对话
    ↓  给模型一份工具 schema，让它输出 tool_calls
function_calling_demo.py：工具调用协议
    ↓
Week2：把工具调用协议放进循环，变成 ReAct Agent
```

Week1 不追求“智能体感”，只追求把协议看清楚：模型输入是什么、输出是什么、哪些事情必须由你的代码执行。每个脚本都要打印关键输入 / 输出，后面才能做 trace 和 eval。

## 本周总结

- [05 本周总结](./notes/05-本周总结.md)（调用协议、`messages`、token、Function Calling 与 Week2 衔接）

## 笔记 `notes/`

- [00 知识地图](./notes/00-知识地图.md)（本周概念结构，一页看懂）
- [01 学习手册](./notes/01-学习手册.md)（当天唯一入口：任务、命令、观察点、关键结论和记录区）
- [02 概念详解](./notes/02-概念详解.md)（Chat API、`messages`、token、Function Calling）
- [03 实验与踩坑](./notes/03-实验与踩坑.md)（实验设计、常见报错、排错顺序）
- [05 本周总结](./notes/05-本周总结.md)（调用协议、`messages`、token、Function Calling 与 Week2 衔接）

## 代码 `code/`

环境在主题根目录 [`ai-agent/`](../README.md#python-环境全主题共用装一次即可) 统一配置（`.venv` + `.env`），装一次后各 week 通用。

```bash
cd code
python hello.py
python chat.py
python function_calling_demo.py
```

| 文件 | 对应天数 | 说明 |
| --- | --- | --- |
| `hello.py` | Day 1-2 | 最小单次调用 |
| `chat.py` | Day 3-4 | 多轮对话 REPL |
| `function_calling_demo.py` | Day 5-7 | 天气假工具 + 完整 tool 回调 |
| `config.py` | — | 共用客户端与模型名（读 `.env`） |

## 环境变量

推荐在 `ai-agent/.env` 配置一次（勿提交 Git）；也可在 `code/.env` 单独覆盖：

```bash
OPENAI_API_KEY=sk-xxx
OPENAI_BASE_URL=https://api.deepseek.com   # DeepSeek；OpenAI 官方可删掉此行
OPENAI_MODEL=deepseek-chat                 # OpenAI 官方可改为 gpt-4o-mini
```

## 验收清单

- [ ] `hello.py` 能打印回答和 token 数。
- [ ] `chat.py` 能连续多轮，且 `/clear` 后上下文清空。
- [ ] `function_calling_demo.py` 能完成「问天气 → 调工具 → 最终回答」。
- [ ] 能画出 `messages` 变化：`system → user → assistant → user → ...`。
- [ ] 能口头解释：LLM 不会真调工具，只是输出结构化 `tool_calls` 让你去执行。
- [ ] 能说清：`tools` schema、Python 函数、`dispatch_tool` 三者分别负责什么。
- [ ] 能保存或复述一次完整请求的关键日志：输入 messages、tool_calls、tool observation、最终回答。

## 进入 Week2 前

如果你还不能解释下面三件事，先别急着写 Agent：

1. API 为什么无状态？多轮为什么要重发完整 `messages`？
2. 第 1 轮 `assistant(tool_calls)` 和第 2 轮最终 `assistant(content)` 有什么区别？
3. 工具返回值为什么要以 `role: tool` 写回 `messages`？

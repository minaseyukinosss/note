# Week1：LLM 调用与 Function Calling

## 本周目标

- Day 1-2：第一次 API 调用，理解 `system` / `user` / `assistant` 与 token。
- Day 3-4：终端多轮对话，实验 temperature 与 Few-shot。
- Day 5-7：Function Calling 完整链路（LLM 选工具 → 你执行 → 塞回结果）。

## 笔记 `notes/`

- [Day 1 学习笔记](./notes/day1-学习笔记.md)（hello.py / 角色与 token）
- [Day 3-4 学习笔记](./notes/day3-学习笔记.md)（多轮对话 / chat.py）
- [Day 5-7 学习笔记](./notes/day5-学习笔记.md)（Function Calling / function_calling_demo.py）

## 代码 `code/`

```bash
cd code
# 需要 Python ≥ 3.10（macOS 可用 python3.12 / python3.11）
python3.12 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env        # 填入你的 API Key
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

在 `code/.env` 中配置（勿提交 Git）：

```bash
OPENAI_API_KEY=sk-xxx
OPENAI_BASE_URL=https://api.deepseek.com   # DeepSeek；OpenAI 官方可删掉此行
OPENAI_MODEL=deepseek-chat                 # OpenAI 官方可改为 gpt-4o-mini
```

## 验收清单

- [ ] `hello.py` 能打印回答和 token 数。
- [ ] `chat.py` 能连续多轮，且 `/clear` 后上下文清空。
- [ ] `function_calling_demo.py` 能完成「问天气 → 调工具 → 最终回答」。
- [ ] 能口头解释：LLM 不会真调工具，只是输出 JSON 让你去执行。

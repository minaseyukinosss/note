# Day 1：第一次 LLM 调用

## 背景 / 学习目标

- 跑通 `hello.py`，看到模型回答与 token 统计。
- 理解三种角色与「无状态」的含义。

## 今日操作

```bash
cd ../code
cp .env.example .env   # 填入 Key
.venv/bin/python hello.py   # Conda 环境下建议用 .venv/bin/python
```

## 核心概念

### system / user / assistant 分别是什么？

| 角色 | 谁在说 | 作用 |
| --- | --- | --- |
| **system** | 开发者定规矩 | 身份、语气、格式；用户一般看不到 |
| **user** | 用户提问 | 这一轮要问什么 |
| **assistant** | 模型历史回答 | 多轮时把上一轮回答塞回列表，模型才知道自己说过什么 |

`hello.py` 里只有 system + user；`chat.py` 每轮会把 assistant 的回答 append 进 `messages`。

### 为什么 LLM 调用是无状态的？

API **不保存**上次聊天记录。每次请求都是独立的，模型只看这一次请求里的 `messages` 全文。

- 第 1 轮：`[system, user₁]` → 得到 `assistant₁`
- 第 2 轮：必须发 `[system, user₁, assistant₁, user₂]`，否则模型「失忆」

`messages` 列表 = 你给模型的**全部记忆**。聊越久列表越长，token 越多、越贵。

### token 和「一个字」的关系？

- **Token ≠ 字、≠ 词**，是模型把文本切成的小块（子词 / 字节片段），用于计费和上下文长度限制。
- 中文：常见 **1 个字 ≈ 1 token**，但常见词组可能被合并成 **1 个 token 对应多个字**（如「大型语言模型」可能少于 6 个 token）。
- 英文：一个单词可能是 1 个 token，也可能是 `un`、`believ`、`able` 多段拼起来。
- **不能要求** `completion_tokens ≥ 回答字数`。字多 token 少、字少 token 多都可能，取决于分词器怎么切。

你那次输出约 `prompt=18, completion=24, total=42`：回答几十个汉字却只要 24 个 completion token，是正常的——说明很多字被合并进了更少的 token。

## Day 1 追问（已搞懂）

### Q1：回答明明超过 25 个字，为什么 completion token 能只有 24？

因为比较的对象错了：**比的是 token 数，不是字数**。

- 计费与上下文限制看的是 **token**，不是「多少个汉字」。
- 中文分词器会把**高频词组**压成更少的 token，所以 **40 个字 → 24 个 token** 完全可能。
- 反过来，一个英文生僻词也可能 **1 个词 → 3 个 token**。

直觉修正：**token 和字数没有固定比例**，只能粗估，不能拿字数当 token。

### Q2：`"role": "system", "content": "..."` 也算输入 token 吗？

**算。** 凡是模型在推理时「读到」的内容，都会进 **prompt_tokens**，包括但不限于：

- `content` 里的正文（「你是一个简洁的中文助手。」）
- 每条消息对应的**角色标记**（API 内部会按 chat 模板转成带 `<|role|>` 一类格式的串，不是把你写的 JSON 原样塞进去，但**角色边界也要占 token**）
- 多轮时之前的 user / assistant 全文

你写的 JSON 是 HTTP 请求的格式；服务端会转成模型专用的对话模板再 tokenize。**所以 system 那句中文、user 那句问题，以及模板里的角色信息，都在 prompt=18 里。**

## 易错点

- 忘记 `cp .env.example .env` → 报 `OPENAI_API_KEY` 未找到。
- DeepSeek 要用 `OPENAI_BASE_URL` + `deepseek-chat`，不能照搬 OpenAI 官方模型名。
- Conda `(base)` + `(.venv)` 同时开时，`python` 可能不是 venv 里的 → 用 `.venv/bin/python`。

## 小结

三种 role 分工不同；每次请求必须带全 `messages` 因为 API 无状态；token 是计费单位不是字数，中文也可能「字多 token 少」。system / user 的正文和角色格式都算 prompt token。

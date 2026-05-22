# Day 3-4：多轮对话（chat.py）

## 背景 / 学习目标

- 理解 `messages` 列表如何在循环里累积。
- 体验 `/clear` 与 Day 1「无状态」的关系。
- 可选：改 system、temperature、Few-shot。

## 今日操作

```bash
cd ../code
.venv/bin/python chat.py
```

## 核心概念

### `chat.py` 里多轮是怎么实现的？

每轮做两件事：

1. `messages.append(user)` → 调用 API → `messages.append(assistant)`
2. 下一轮把整个 `messages` **原样再发给 API**

对应代码：

```53:61:ai-agent/week1-hello-llm/code/chat.py
        messages.append({"role": "user", "content": user_input})

        resp = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
        )
        assistant_msg = resp.choices[0].message.content or ""
        messages.append({"role": "assistant", "content": assistant_msg})
```

### `/clear` 说明了什么？

`messages` 重置为只剩 `system` → 模型立刻「失忆」，印证 API 不存历史。

### temperature 是什么？

- 越低（如 `0`）：回答越稳定、越像「背标准答案」。
- 越高（如 `1.2`）：更随机、更有变化，也可能更离谱。
- 改法：终端输入 `/temp 0` 或 `/temp 1.2`。

### Few-shot（可选实验）

在 `messages` 初始化时，在 `system` 后面加几组示例：

```python
messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user", "content": "1+1"},
    {"role": "assistant", "content": "2"},
    {"role": "user", "content": "2+2"},
    {"role": "assistant", "content": "4"},
]
```

再问 `3+3`，看是否倾向只答数字。

## 自测（参考答案）

### 1. 用户说第二句话时，`messages` 里至少有几条？各是什么 role？

至少 **5 条**（假设第一轮已经完整走完）：

| 顺序 | role | 谁的内容 |
| --- | --- | --- |
| 1 | system | 开场定下的规矩（一直在） |
| 2 | user | 你第一句话 |
| 3 | assistant | 模型对第一句话的回答 |
| 4 | user | 你第二句话（刚 append） |
| 5 | （下一轮 API 返回后才会出现）assistant | 模型对第二句话的回答 |

说第二句话的**那一瞬间**（已 `append` 第 4 条 user，还没收到本轮 assistant），列表里是 **4 条**：system + user₁ + assistant₁ + user₂。

第一轮刚启动、你还没说过任何话时，只有 **1 条** system。

### 2. 为什么聊 10 轮后，每轮 total token 往往越来越大？

因为 **每一轮都把从开头到现在的全部对话再发给模型**。

- 第 1 轮：system + user₁ + assistant₁ → 短
- 第 10 轮：system + 9 组 (user + assistant) + 当前 user → 很长

`messages` 只增不减（除非 `/clear`），所以 prompt 越来越长，`usage.total_tokens` 通常会**一轮比一轮大**。  
（少数情况新回答很短、total 略降，但长期趋势是涨。）

### 3. 改 system 和改 temperature，分别像在调什么？

| 旋钮 | 调的是什么 | 类比 |
| --- | --- | --- |
| **system**（改 `SYSTEM_PROMPT`） | **人设与规则**：身份、语气、格式、禁止事项 | 换了一本「员工手册」 |
| **temperature** | **随机程度**：同 prompt 下回答有多「飘」 | 0 ≈ 尽量稳定重复；高 ≈ 更敢瞎编花样 |

- system 改的是 **输入内容**（进 prompt，占 token）。
- temperature 改的是 **生成时的采样**，不改变模型「记得什么」，也不增加历史。

两者正交：可以「杠精手册 + temperature=0」得到稳定抬杠。

## 实验记录（选填）

| 实验 | 你改了什么 | 观察 |
| --- | --- | --- |
| 换 system 角色 | | |
| `/temp 0` vs `/temp 1.2` | | |
| Few-shot | | |
| `/clear` 后再问上一轮话题 | | |

## 小结

### 多轮与 token

`chat.py` 每轮向 `messages` 追加 user 和 assistant，再把**整段历史**发给 API，所以模型能接上话，且聊越久 token 越多。

### 无状态（API 不记上一轮）

**无状态** = 服务端**不保存**上次请求里的对话；每次调用都是新请求，模型只看这一次你发来的 `messages`。

| 对比 | 有状态（如微信） | 无状态（Chat API） |
| --- | --- | --- |
| 谁记历史 | 服务器 | 应用自己维护 `messages` |
| 第 2 次请求 | 常只需发新消息 | 必须把之前各轮 user/assistant **一并重发** |
| `/clear` | — | 列表只剩 system，等同「失忆」 |

记忆不在模型「脑子里」，而在我们维护的列表里；`/clear` 清空列表，下一轮 API 就接不上之前的话题。多轮能接上话，不是因为模型记住了，而是因为我们**每次把完整 `messages` 当上下文塞回去**。

### system 与 temperature

- **system**：定人设与规则，改的是**输入内容**（进 prompt，占 token）。
- **temperature**：定回答**随机程度**，不改历史、不增加记忆。

**背一句**：多轮 = 不断 append 整包 messages；token 涨 = 历史重发；无状态 = API 不存会话，靠 `messages` 当临时记忆条；system 管说什么，temperature 管多随机。

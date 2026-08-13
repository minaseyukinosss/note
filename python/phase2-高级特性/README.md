# 阶段二：Python 高级特性（Day 22-45）

> 目标：吃透让代码"高级"的特性。**这一阶段直接决定你能不能读懂 LangChain / Pydantic 源码**。

## 本阶段解决什么问题

读框架源码时你会遇到：
- `@tool` `@app.post` 这种装饰器——它怎么工作的？
- `class MyModel(BaseModel)` 继承链一长串——MRO 是什么？
- `for chunk in stream:` 逐 token 输出——生成器怎么实现的？
- `chain = a | b | c`——`|` 为什么能这么用？（魔术方法 `__or__`）

本阶段把这些一次性讲清，让你从"看不懂源码"到"能顺着读下去"。

## 学习顺序

1. **面向对象**（Day 22-25）：`self`、类/实例属性、classmethod/staticmethod、单继承、`super()`、多继承 MRO。
2. **抽象接口 + Week 4 复盘**（Day 26-28）：`ABC` + `@abstractmethod`、`Protocol`；Day 28 组合 `Tool` / `Memory` / `Agent`（不重复刷题）。
3. **装饰器**（Day 29-31）：函数装饰器、带参装饰器、`functools.wraps`（闭包为阶段一复习，不单开章节）。
4. **魔术方法**（Day 34-35）：`__call__`、`__repr__`、`__eq__`。（Day 32-33：选学/综合，类装饰器建议 Day 34 后再看。）
5. **生成器 / 迭代器**（Day 36-38）：`yield`、`yield from`、迭代器协议、`itertools`。
6. **上下文管理器**（Day 39-40）：`with`、`__enter__/__exit__`、`contextlib.contextmanager`。
7. **dataclass + typing**（Day 41-44）：`@dataclass`、泛型、`Optional`/`|`、`TypedDict`、`Literal`；Day 43 用 Pylance/pyright 扫一遍注解。
8. **综合实战**（Day 45）：手写迷你可组合调用链（`mini_chain.py` 骨架；对照 `mini_chain_solution.py`）。

## 代码练习 `code/`

```bash
cd python/phase2-高级特性/code
python exercises.py              # O1–O5 OOP；1–4 装饰器 / 生成器 / 魔术方法 / 上下文
python mini_chain.py             # Day 45：按 TODO 实现后跑通
# 卡住再看：python mini_chain_solution.py
```

`exercises.py` 里每题附 Agent 用途说明；做完取消对应 `assert` 注释再跑。

## 笔记 `notes/`

- [01-学习手册](./notes/01-学习手册.md)：当天任务、观察点、结论记录区（学习时只开这个 + 每日清单）。
- [02-每日清单](./notes/02-每日清单.md)：Day 22-45 逐天可执行清单，对应 `code/exercises.py` 题号。

## 验收标准

- [ ] 能手写一个带参装饰器 `@retry(times=3)`，并解释 `functools.wraps` 的作用。
- [ ] 能说清多继承 MRO 的查找顺序。
- [ ] 能用 `__call__` 让一个对象像函数一样被调用。
- [ ] 能用生成器实现惰性的流式管道。
- [ ] 能用 `@contextmanager` 写一个计时器。
- [ ] 本阶段写过的练习/实战有完整类型注解，Pylance 或 `pyright` 对本目录无新增红线（不搭 CI）。
- [ ] 独立完成 `mini_chain.py`：`(step_a | step_b | step_c)(input)` 能跑通（魔术方法 `__or__`/`__call__` + typing；装饰器在 exercises 题 1 单独验收）。

## 对应 Agent 用途速记

| 特性 | 在 Agent / 框架里 |
| --- | --- |
| 装饰器 | `@tool` 注册、`@app.post` 路由、重试 |
| 魔术方法 `__call__` | `agent(input)` 可调用 |
| 魔术方法 `__or__` | LCEL `prompt | model | parser` |
| 生成器 | LLM streaming 逐 token |
| 上下文管理器 | client / trace span 生命周期 |
| Protocol / ABC | `Runnable`、`BaseChatModel` 抽象 |
| typing | 读源码的前提、工具签名 |

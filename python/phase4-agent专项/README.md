# 阶段四：AI Agent 开发专项能力（Day 67-90）

> 目标：把前三阶段的能力用到真实 Agent 技术栈，并开始读框架源码。这是最终冲刺。

## 本阶段解决什么问题

- "怎么并发调用多个 LLM / 工具，而不是一个个等？"（asyncio）
- "怎么封装一个稳定的、带重试和流式的 LLM 调用层？"（httpx + tenacity）
- "怎么把 LLM 的输出变成可校验的结构化对象？"（Pydantic）
- "怎么把 Agent 暴露成一个流式 API 服务？"（FastAPI）
- "怎么读懂 LangChain 的核心抽象，甚至自己设计框架？"（源码 + 设计模式）

## 学习顺序

1. **async / asyncio**（Day 67-71）：协程、`await`、事件循环、`gather`、`create_task`、超时、`Semaphore` 限流。
2. **httpx + API 封装**（Day 74-77）：sync/async client、流式、tenacity 重试、错误处理。
3. **JSON + 数据模型**（Day 78-80）：容错解析 tool_calls、用 Pydantic 建模 Message/ToolCall/State。
4. **Pydantic v2 深入**（Day 81-83）：校验器、`Field`、`model_validate`、序列化、结构化输出。
5. **FastAPI**（Day 84-86）：路由、依赖注入、async 端点、SSE 流式。
6. **源码阅读 + 设计模式**（Day 87-90）：LangChain `Runnable`/LCEL、Agent 设计模式，收尾终极项目。

## asyncio 关键机制（必须先建立的心智模型）

| 机制 | 要点 |
| --- | --- |
| 事件循环 | 协程必须放进事件循环才会跑，入口用 `asyncio.run(main())` 显式启动 |
| 并发聚合 | `await asyncio.gather(*tasks)` 并发执行多个协程并收集结果 |
| 创建任务 | `asyncio.create_task(coro())` 把协程排进循环立即调度 |
| 异步生成器 | `async def` + `yield` + `async for`，用于流式逐块产出 |
| 阻塞陷阱 | 在 async 里调同步阻塞函数（如 `time.sleep`）会卡死整个事件循环，要用 `asyncio.sleep` |

> 记住一条最容易懵的点：**只调用 async 函数（`foo()`）拿到的是一个 coroutine 对象，不 `await` 也不放进事件循环，它根本不会执行。**

## 代码练习 `code/`

```bash
cd python/phase4-agent专项/code
python async_demo.py       # asyncio 并发 + 超时 + 限流
python models_demo.py      # Pydantic 建模 Message/ToolCall
```

真实项目还需要 `uv add httpx fastapi uvicorn pydantic tenacity`。

## 笔记 `notes/`

- [01-学习手册](./notes/01-学习手册.md)

## 源码阅读

配合 [../04-源码阅读清单](../04-源码阅读清单.md)，本阶段至少认真读完：
- `tenacity`（重试装饰器，回收阶段二知识）
- `openai-python`（LLM SDK 标准封装）
- `langchain-core` 的 `Runnable.__or__`（回收 mini_chain）

## 验收标准（也是全计划的终点）

- [ ] 能用 asyncio 并发调 3 个接口、聚合结果、处理超时、用 Semaphore 限并发。
- [ ] 能封装一个异步 `LLMClient`：超时 + 重试 + 流式 + 错误处理。
- [ ] 能用 Pydantic 定义 Message/ToolCall/AgentState 并做校验。
- [ ] 能用 FastAPI 暴露一个 `/chat` 的 SSE 流式接口。
- [ ] 能读懂并复述 LangChain `Runnable` 的组合机制。
- [ ] **最终产出**：一个完整异步 Agent 服务（FastAPI + Pydantic + httpx + 日志 + 测试）。

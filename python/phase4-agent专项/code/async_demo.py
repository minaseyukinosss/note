"""asyncio 并发参考示例：并发 + 超时 + 限流。

这是 Agent 里"同时调多个工具/LLM"的核心模式。用纯标准库模拟 IO 等待，
无需任何外部依赖即可运行：

    python async_demo.py

要点：gather 并发聚合、Semaphore 限并发、wait_for 超时、asyncio.run 启动事件循环。
"""

from __future__ import annotations

import asyncio
import random
import time


async def fake_call(name: str) -> str:
    """模拟一次耗时的异步 IO（如 LLM 请求）。"""
    delay = random.uniform(0.1, 0.5)
    await asyncio.sleep(delay)  # 关键：用 asyncio.sleep 而非 time.sleep
    return f"{name} 完成，耗时 {delay:.2f}s"


async def run_concurrently() -> list[str]:
    """gather 并发执行多个协程并按顺序聚合结果。"""
    tasks = [fake_call(f"task-{i}") for i in range(5)]
    return await asyncio.gather(*tasks)


async def run_with_limit(limit: int = 2) -> list[str]:
    """用 Semaphore 限制同时最多 limit 个并发（如 LLM 限流）。"""
    sem = asyncio.Semaphore(limit)

    async def guarded(i: int) -> str:
        async with sem:
            return await fake_call(f"limited-{i}")

    return await asyncio.gather(*(guarded(i) for i in range(5)))


async def run_with_timeout() -> str:
    """超时控制：超过 0.2s 就放弃。"""
    try:
        return await asyncio.wait_for(fake_call("slow"), timeout=0.2)
    except asyncio.TimeoutError:
        return "slow 超时，已放弃"


async def main() -> None:
    t0 = time.perf_counter()
    print("=== gather 并发 ===")
    for line in await run_concurrently():
        print(" ", line)

    print("=== Semaphore 限流（最多 2 并发）===")
    for line in await run_with_limit(2):
        print(" ", line)

    print("=== 超时控制 ===")
    print(" ", await run_with_timeout())

    print(f"\n总耗时 {time.perf_counter() - t0:.2f}s（并发比顺序快得多）")


if __name__ == "__main__":
    asyncio.run(main())  # 关键：显式启动事件循环

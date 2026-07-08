"""阶段二 高级特性练习：装饰器 / 闭包 / 魔术方法 / 生成器 / 上下文管理器。

实现每个 TODO，然后取消 __main__ 里对应断言运行：

    python exercises.py
"""

from __future__ import annotations

import functools
import time
from contextlib import contextmanager
from typing import Callable, Iterator


# ---------------------------------------------------------------------------
# 1. 带参装饰器：@retry(times=3)
#    Agent 用途：LLM/网络调用失败自动重试
# ---------------------------------------------------------------------------
def retry(times: int = 3) -> Callable:
    """失败（抛异常）时最多重试 times 次，全部失败则抛出最后一次异常。"""
    # TODO: 三层结构 —— retry(times) -> decorator(func) -> wrapper(*a, **k)
    #       记得用 functools.wraps(func) 保留元信息
    raise NotImplementedError


# ---------------------------------------------------------------------------
# 2. 魔术方法 __call__：让对象像函数一样被调用
#    Agent 用途：框架里的 agent(input) / tool(args)
# ---------------------------------------------------------------------------
class Multiplier:
    def __init__(self, factor: int) -> None:
        self.factor = factor

    # TODO: 实现 __call__，使 Multiplier(3)(10) == 30
    # TODO: 实现 __repr__，返回 "Multiplier(factor=3)"


# ---------------------------------------------------------------------------
# 3. 生成器：惰性流式管道
#    Agent 用途：LLM streaming 逐 token 处理
# ---------------------------------------------------------------------------
def take(gen: Iterator, n: int) -> list:
    """从生成器里惰性取前 n 个（不要一次性耗尽无限生成器）。"""
    # TODO: 用 for + enumerate + break，或 itertools.islice
    raise NotImplementedError


def naturals() -> Iterator[int]:
    """无限自然数生成器 1, 2, 3, ...（用于测试 take 的惰性）。"""
    # TODO: while True + yield
    raise NotImplementedError


# ---------------------------------------------------------------------------
# 4. 上下文管理器：计时器
#    Agent 用途：trace 每个步骤耗时
# ---------------------------------------------------------------------------
@contextmanager
def timer(label: str):
    """with timer('x'): ... 退出时记录耗时到 timer.last。"""
    # TODO: 记录 start；yield；finally 里计算 elapsed 存到 timer.last
    raise NotImplementedError


if __name__ == "__main__":
    # 实现后逐个取消注释
    # calls = {"n": 0}
    # @retry(times=3)
    # def flaky():
    #     calls["n"] += 1
    #     if calls["n"] < 3:
    #         raise ValueError("boom")
    #     return "ok"
    # assert flaky() == "ok" and calls["n"] == 3

    # assert Multiplier(3)(10) == 30
    # assert repr(Multiplier(3)) == "Multiplier(factor=3)"

    # assert take(naturals(), 3) == [1, 2, 3]

    # with timer("demo"):
    #     time.sleep(0.01)
    # assert timer.last >= 0.01

    print("全部通过。把上面断言取消注释来逐题验证。")

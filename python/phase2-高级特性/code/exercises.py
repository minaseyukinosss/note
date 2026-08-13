"""阶段二 高级特性练习。

实现每个 TODO，然后取消 __main__ 里对应断言运行：

    python exercises.py

题号：
  O1–O5  —— Week 4 面向对象 / ABC（Day 22-28）
  1–4    —— 装饰器 / __call__ / 生成器 / 上下文管理器（Day 29+）
"""

from __future__ import annotations

import functools
import time
from abc import ABC, abstractmethod
from contextlib import contextmanager
from typing import Callable, Iterator


# ===========================================================================
# Week 4：OOP
# ===========================================================================

# ---------------------------------------------------------------------------
# O1. 实例属性：独立计数器
#     Agent 用途：每个 Agent / session 自己的状态，不要用可变类属性共享
# ---------------------------------------------------------------------------
class Counter:
    """每次 inc() 把 self.n 加 1；不同实例互不影响。"""

    def __init__(self) -> None:
        # TODO: 初始化实例属性 self.n = 0
        self.n = 0

    def inc(self) -> int:
        # TODO: self.n += 1，并返回 self.n
        self.n += 1
        return self.n


# ---------------------------------------------------------------------------
# O2. @classmethod 工厂：从 dict 构造
#     Agent 用途：Message.from_dict / Tool.from_config
# ---------------------------------------------------------------------------
class Message:
    def __init__(self, role: str, content: str) -> None:
        self.role = role
        self.content = content

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> Message:
        """用 data['role'] / data['content'] 构造；用 cls(...) 而不是写死 Message(...)。"""
        # TODO
        return cls(data['role'], data['content'])


# ---------------------------------------------------------------------------
# O3. 单继承 + super()
#     Agent 用途：BaseTool → 具体工具
# ---------------------------------------------------------------------------
class BaseTool:
    def __init__(self, name: str) -> None:
        self.name = name

    def run(self, query: str) -> str:
        raise NotImplementedError


class EchoTool(BaseTool):
    """name 固定为 'echo'；run 返回 'echo:<query>'。"""

    def __init__(self) -> None:
        # TODO: super().__init__("echo")
        super().__init__("echo")

    def run(self, query: str) -> str:
        # TODO
        return f"echo:{query}"

# ---------------------------------------------------------------------------
# O4. MRO 阅读（无需实现逻辑，断言检查你对 __mro__ 的理解）
#     定义见 __main__ 中的 A/B/C/D；你要能说出 D 的查找顺序
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# O5. ABC + 抽象方法
#     Agent 用途：Memory / BaseChatModel 一类框架抽象
# ---------------------------------------------------------------------------
class BaseMemory(ABC):
    @abstractmethod
    def add(self, text: str) -> None:
        ...

    @abstractmethod
    def get(self) -> list[str]:
        ...


class ListMemory(BaseMemory):
    """用内部 list 存消息；add append；get 返回副本（避免外层改到内部）。"""

    def __init__(self) -> None:
        # TODO: self._items: list[str] = []
        self._items: list[str] = []

    def add(self, text: str) -> None:
        # TODO
        self._items.append(text)

    def get(self) -> list[str]:
        # TODO: 返回副本，如 list(self._items) 或 self._items.copy()
        return self._items.copy()

# ===========================================================================
# Week 5+：装饰器 / 魔术方法 / 生成器 / 上下文管理器
# ===========================================================================

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
    # ----- O1 Counter -----
    a, b = Counter(), Counter()
    assert a.inc() == 1 and a.inc() == 2
    assert b.inc() == 1  # 与 a 独立

    # ----- O2 Message.from_dict -----
    m = Message.from_dict({"role": "user", "content": "hi"})
    assert m.role == "user" and m.content == "hi"
    assert isinstance(m, Message)

    # ----- O3 EchoTool -----
    t = EchoTool()
    assert t.name == "echo" and t.run("ping") == "echo:ping"

    # ----- O4 MRO -----
    class A:
        pass
    class B(A):
        pass
    class C(A):
        pass
    class D(B, C):
        pass
    assert [c.__name__ for c in D.__mro__] == ["D", "B", "C", "A", "object"]

    # ----- O5 ListMemory -----
    mem = ListMemory()
    mem.add("a")
    mem.add("b")
    got = mem.get()
    assert got == ["a", "b"]
    got.append("leak")
    assert mem.get() == ["a", "b"]  # get 返回副本，内部未被改

    # ----- 1 retry -----
    # calls = {"n": 0}
    # @retry(times=3)
    # def flaky():
    #     calls["n"] += 1
    #     if calls["n"] < 3:
    #         raise ValueError("boom")
    #     return "ok"
    # assert flaky() == "ok" and calls["n"] == 3

    # ----- 2 Multiplier -----
    # assert Multiplier(3)(10) == 30
    # assert repr(Multiplier(3)) == "Multiplier(factor=3)"

    # ----- 3 take / naturals -----
    # assert take(naturals(), 3) == [1, 2, 3]

    # ----- 4 timer -----
    # with timer("demo"):
    #     time.sleep(0.01)
    # assert timer.last >= 0.01

    print("全部通过。把上面断言取消注释来逐题验证。")

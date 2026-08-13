"""综合实战骨架：模仿 LangChain LCEL 的可组合调用链（Day 45 手写）。

核心思想：重载 __or__，让 step_a | step_b | step_c 组合成顺序管道。
这正是 LangChain 里 `prompt | model | parser` 的本质。

用法：
    1. 实现下方 TODO
    2. python mini_chain.py
    3. 卡住再对照 mini_chain_solution.py（先自己写）

本文件验收的是魔术方法 + typing；装饰器在 exercises.py 题 1 单独验收。
"""

from __future__ import annotations

from typing import Any, Callable, Generic, TypeVar

In = TypeVar("In")
Out = TypeVar("Out")


class Runnable(Generic[In, Out]):
    """最小可组合单元：子类实现 invoke；基类提供 | 与可调用。"""

    def invoke(self, value: In) -> Out:
        raise NotImplementedError

    def __or__(self, other: "Runnable[Out, Any]") -> "RunnableSequence":
        """a | b —— 返回把 a 的输出喂给 b 的序列。"""
        # TODO: return RunnableSequence(self, other)
        raise NotImplementedError

    def __call__(self, value: In) -> Out:
        """chain(x) 等价于 chain.invoke(x)。"""
        # TODO: return self.invoke(value)
        raise NotImplementedError


class RunnableLambda(Runnable[In, Out]):
    """把普通函数包成 Runnable。"""

    def __init__(self, func: Callable[[In], Out]) -> None:
        self.func = func

    def invoke(self, value: In) -> Out:
        # TODO: 调用 self.func
        raise NotImplementedError

    def __repr__(self) -> str:
        # TODO: 返回类似 RunnableLambda(strip) 的字符串
        raise NotImplementedError


class RunnableSequence(Runnable[Any, Any]):
    """按顺序执行的管道；构造时扁平化嵌套的 RunnableSequence。"""

    def __init__(self, *steps: Runnable) -> None:
        # TODO: 遍历 steps；若元素已是 RunnableSequence 则 extend 其 .steps，否则 append
        #       结果存到 self.steps
        raise NotImplementedError

    def invoke(self, value: Any) -> Any:
        # TODO: 依次 step.invoke(value)，把输出传给下一步
        raise NotImplementedError

    def __repr__(self) -> str:
        # TODO: 用 " | ".join(repr(s) for s in self.steps)
        raise NotImplementedError


def as_runnable(func: Callable[[In], Out]) -> RunnableLambda[In, Out]:
    # TODO: return RunnableLambda(func)
    raise NotImplementedError


if __name__ == "__main__":
    strip = as_runnable(str.strip)
    upper = as_runnable(str.upper)
    exclaim = as_runnable(lambda s: s + "!")

    chain = strip | upper | exclaim
    print("管道结构:", chain)
    print("调用结果:", chain("  hello  "))

    assert chain("  hello  ") == "HELLO!"
    assert chain.invoke("hi") == "HI!"
    # 可选：确认扁平化 —— (a | b) | c 与 a | b | c 步数相同
    assert len(chain.steps) == 3
    print("通过：a | b | c 组合与调用均正常。")

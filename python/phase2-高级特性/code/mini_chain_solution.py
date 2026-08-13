"""综合实战参考答案（Day 45 完成后再对照）。

先自己实现 mini_chain.py；不要一上来就读本文件。

运行：
    python mini_chain_solution.py
"""

from __future__ import annotations

from typing import Any, Callable, Generic, TypeVar

In = TypeVar("In")
Out = TypeVar("Out")


class Runnable(Generic[In, Out]):
    """最小可组合单元：实现 invoke，用 | 组合成序列。"""

    def invoke(self, value: In) -> Out:
        raise NotImplementedError

    def __or__(self, other: "Runnable[Out, Any]") -> "RunnableSequence":
        """a | b —— 返回一个把 a 的输出喂给 b 的序列。"""
        return RunnableSequence(self, other)

    def __call__(self, value: In) -> Out:
        """让实例可以像函数一样调用：chain(x)。"""
        return self.invoke(value)


class RunnableLambda(Runnable[In, Out]):
    """把普通函数包成 Runnable。"""

    def __init__(self, func: Callable[[In], Out]) -> None:
        self.func = func

    def invoke(self, value: In) -> Out:
        return self.func(value)

    def __repr__(self) -> str:
        return f"RunnableLambda({self.func.__name__})"


class RunnableSequence(Runnable[Any, Any]):
    """按顺序执行的管道，扁平化嵌套的 |。"""

    def __init__(self, *steps: Runnable) -> None:
        flat: list[Runnable] = []
        for step in steps:
            if isinstance(step, RunnableSequence):
                flat.extend(step.steps)
            else:
                flat.append(step)
        self.steps = flat

    def invoke(self, value: Any) -> Any:
        for step in self.steps:
            value = step.invoke(value)
        return value

    def __repr__(self) -> str:
        return " | ".join(repr(s) for s in self.steps)


def as_runnable(func: Callable[[In], Out]) -> RunnableLambda[In, Out]:
    return RunnableLambda(func)


if __name__ == "__main__":
    strip = as_runnable(str.strip)
    upper = as_runnable(str.upper)
    exclaim = as_runnable(lambda s: s + "!")

    chain = strip | upper | exclaim
    print("管道结构:", chain)
    print("调用结果:", chain("  hello  "))

    assert chain("  hello  ") == "HELLO!"
    assert chain.invoke("hi") == "HI!"
    print("通过：a | b | c 组合与调用均正常。")

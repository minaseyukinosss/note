"""Day 27：看编辑器红线（Pylance），不是跑 python 才算。

打开本文件，等几秒，看 run() 的两处调用：
- FakeChain() 那一行：有 invoke，一般不红
- NotRunnable() 那一行：没有 invoke，应有红线

运行本文件仍然会执行到最后一行才 AttributeError，那是运行时；红线是写代码时。
"""

from typing import Any, Protocol


class RunnableLike(Protocol):
    def invoke(self, value: str) -> Any: ...


class FakeChain:
    def invoke(self, value: str) -> str:
        return value.upper()


class NotRunnable:
    def talk(self) -> str:
        return "hi"


def run(r: RunnableLike) -> Any:
    return r.invoke("hello")


run(FakeChain())
run(NotRunnable())

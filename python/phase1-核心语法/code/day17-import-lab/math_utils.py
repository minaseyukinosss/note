"""供 import 实验用的简单工具模块。"""


def add(a: int, b: int) -> int:
    return a + b


def multiply(a: int, b: int) -> int:
    return a * b


# 模块顶层代码：import 时会立刻执行
print(f"[math_utils] 模块被加载，__name__ = {__name__!r}")

"""无循环依赖的 A —— 供延迟 import 实验用。"""

print("[module_a_standalone] 模块被加载")


def func_a() -> str:
    return "func_a"

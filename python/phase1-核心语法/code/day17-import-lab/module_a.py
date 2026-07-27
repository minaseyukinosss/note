"""循环导入实验 —— A 依赖 B。"""

print("[module_a] 开始执行顶层代码")

from module_b import func_b

print("[module_a] 已从 module_b 导入 func_b")


def func_a() -> str:
    return f"func_a -> {func_b()}"

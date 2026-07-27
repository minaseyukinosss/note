"""循环导入实验 —— B 依赖 A。"""

print("[module_b] 开始执行顶层代码")

from module_a import func_a

print("[module_b] 已从 module_a 导入 func_a")


def func_b() -> str:
    return "func_b"

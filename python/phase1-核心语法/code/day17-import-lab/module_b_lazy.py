"""循环导入修复：顶层不 import A，在函数里延迟 import。"""

print("[module_b_lazy] 模块被加载")


def func_b() -> str:
    from module_a_standalone import func_a

    return f"func_b -> {func_a()}"

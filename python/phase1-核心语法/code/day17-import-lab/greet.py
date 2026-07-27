"""演示 __name__ == "__main__"：直接运行 vs 被 import。"""


def hello(name: str = "world") -> str:
    return f"Hello, {name}!"


print(f"[greet] 模块被加载，__name__ = {__name__!r}")

if __name__ == "__main__":
    # 只有「python greet.py」时会进这里；被 import 时不执行
    print("[greet] 作为脚本直接运行")
    print(hello("Day 17"))

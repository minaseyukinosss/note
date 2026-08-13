"""Day 28：组合 —— Agent 持有 Tool 和 Memory，不是再继承一遍。

组合 = 「里面装着别人，需要时调用」，不是 「我是一种 Tool」。

运行（在 code/ 目录下）：
    python oop_lab.py
"""

from exercises import EchoTool, ListMemory


class Agent:
    """持有一个 tool、一份 memory；handle 时先跑工具，再把结果记进 memory。"""

    def __init__(self, tool: EchoTool, memory: ListMemory) -> None:
        # TODO: 把传入的 tool、memory 挂到 self 上（实例属性，每人一份）
        self.tool = tool
        self.memory = memory

    def handle(self, query: str) -> str:
        # TODO:
        # 1. result = self.tool.run(query)
        # 2. self.memory.add(result)
        # 3. return result
        result = self.tool.run(query)
        self.memory.add(result)
        return result


if __name__ == "__main__":
    agent = Agent(EchoTool(), ListMemory())
    out = agent.handle("ping")
    assert out == "echo:ping"
    assert agent.memory.get() == ["echo:ping"]

    other = Agent(EchoTool(), ListMemory())
    other.handle("pong")
    assert other.memory.get() == ["echo:pong"]
    assert agent.memory.get() == ["echo:ping"]  # 两个 Agent 的 memory 互不影响

    print("通过：Agent 组合了 tool + memory，实例状态独立。")

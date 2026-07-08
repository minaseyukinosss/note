"""Pydantic 数据模型参考示例：给 Agent 的消息 / 工具调用建模。

这是 Agent 工程的地基：把非结构化 dict 变成可校验、可序列化的对象。

依赖：uv add pydantic
运行：uv run python models_demo.py

关键认知：Python 的类型注解运行时不校验，所以需要 Pydantic 在运行时真正做校验。
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, ValidationError


class ToolCall(BaseModel):
    """LLM 请求调用某个工具。"""

    id: str
    name: str
    arguments: dict = Field(default_factory=dict)


class Message(BaseModel):
    """一条对话消息。role 用 Literal 收窄取值范围。"""

    role: Literal["system", "user", "assistant", "tool"]
    content: str = ""
    tool_calls: list[ToolCall] = Field(default_factory=list)


class AgentState(BaseModel):
    """Agent 运行状态：消息历史 + 步数 + 是否结束。"""

    messages: list[Message] = Field(default_factory=list)
    step: int = 0
    finished: bool = False

    def add(self, message: Message) -> None:
        self.messages.append(message)
        self.step += 1


def demo_valid() -> None:
    # 从"看起来像 LLM 返回的 dict"校验成对象
    raw = {
        "role": "assistant",
        "content": "",
        "tool_calls": [
            {"id": "call_1", "name": "get_weather", "arguments": {"city": "北京"}}
        ],
    }
    msg = Message.model_validate(raw)
    print("解析成功:", msg.tool_calls[0].name, msg.tool_calls[0].arguments)

    state = AgentState()
    state.add(Message(role="user", content="北京天气如何？"))
    state.add(msg)
    print("状态步数:", state.step)
    print("序列化:", state.model_dump()["messages"][0])


def demo_invalid() -> None:
    # role 不在 Literal 里，Pydantic 会在运行时报错（这是 dataclass 做不到的）
    try:
        Message.model_validate({"role": "boss", "content": "hi"})
    except ValidationError as exc:
        print("校验拦截了非法 role：", exc.errors()[0]["msg"])


if __name__ == "__main__":
    demo_valid()
    print("---")
    demo_invalid()

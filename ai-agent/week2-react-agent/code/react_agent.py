"""
Day 10-12：手写 ReAct Agent（纯 openai SDK，无框架）。

循环：请求 → tool_calls? → dispatch → role=tool → 再请求，直到无 tool_calls。

运行（需先补完 run_agent）：
  python react_agent.py
"""

from __future__ import annotations

import json
from typing import Any

from config import get_client, get_model

SYSTEM_PROMPT = (
    "你是个能调用工具的助手。"
    "需要查天气、做计算或搜索时，请调用对应工具。"
    "拿到所有工具结果后，用自然语言直接回答用户。"
    "若没有合适工具，礼貌说明做不到，不要编造。"
)

TOOLS: list[dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "查询指定城市的当前天气",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "城市名，如 北京、上海"},
                },
                "required": ["city"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "计算数学表达式，支持 + - * / 和括号",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "数学表达式，如 23 * 47 或 (1+2)/3",
                    },
                },
                "required": ["expression"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search",
            "description": "搜索网络信息（练习用假数据）",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "搜索关键词"},
                },
                "required": ["query"],
            },
        },
    },
]


def get_weather(city: str) -> str:
    return f"{city} 今天晴，气温 25°C，湿度 40%。"


def calculator(expression: str) -> str:
    """练习用 eval；生产环境勿这样写。"""
    try:
        # 仅允许数字与常见运算符
        allowed = set("0123456789+-*/(). ")
        if not all(c in allowed for c in expression):
            return "错误：表达式含不允许的字符"
        value = eval(expression, {"__builtins__": {}}, {})  # noqa: S307
        return str(value)
    except ZeroDivisionError:
        return "错误：除数不能为 0"
    except Exception as exc:
        return f"错误：{exc}"


def search(query: str) -> str:
    return f"【假搜索结果】关于「{query}」：暂无实时数据，这是固定占位文本。"


def dispatch_tool(name: str, arguments_json: str) -> str:
    args = json.loads(arguments_json or "{}")
    if name == "get_weather":
        return get_weather(args.get("city", "未知城市"))
    if name == "calculator":
        return calculator(args.get("expression", ""))
    if name == "search":
        return search(args.get("query", ""))
    return f"未知工具: {name}"


def _print_step(step: int, messages: list) -> None:
    print(f"\n{'=' * 60}\nStep {step} — messages 共 {len(messages)} 条")
    for i, m in enumerate(messages):
        role = m.get("role", "?")
        preview = m.get("content") or m.get("tool_calls") or ""
        text = str(preview)
        if len(text) > 120:
            text = text[:120] + "..."
        print(f"  [{i}] {role}: {text}")


def run_agent(user_input: str, max_steps: int = 6, verbose: bool = True) -> str:
    """
    ReAct 主循环 —— Day 10-12 练习：请补完下方 TODO。

    提示：
    - 参考 week1 function_calling_demo.py 的两轮协议
    - assistant 含 tool_calls 时用 msg.model_dump(exclude_none=True) append
    - 无 tool_calls 时 return msg.content
    - 超过 max_steps 返回超时提示
    """
    client = get_client()
    model = get_model()

    messages: list[dict[str, Any]] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_input},
    ]

    # TODO(Day 10-12): 实现 for step in range(max_steps) 循环
    #   1. client.chat.completions.create(..., tools=TOOLS)
    #   2. messages.append(msg.model_dump(exclude_none=True))
    #   3. if not msg.tool_calls: return msg.content
    #   4. for call in msg.tool_calls: dispatch → append role=tool
    #   5. verbose 时调用 _print_step(step, messages)
    for step in range(max_steps):
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=TOOLS,
        )
        msg = response.choices[0].message

        messages.append(msg.model_dump(exclude_none=True))

        if not msg.tool_calls:
            return msg.content or ""
        
        for call in msg.tool_calls:
            fn = call.function
            result = dispatch_tool(fn.name, fn.arguments)

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": result,
                }
            )
        
        if verbose:
            _print_step(step, messages)
    
    return f"超过最大步数 max_steps={max_steps}，未得到最终回答。"


def main() -> None:
    demos = [
        "北京今天天气怎么样？",
        "北京今天天气怎么样？再帮我算 23 * 47",
        "100 除以 0 等于多少？",
        "帮我订一张明天去上海的机票",
    ]
    for q in demos:
        print("\n" + "#" * 60)
        print("用户:", q)
        answer = run_agent(q, verbose=True)
        print("\n最终回答:", answer)


if __name__ == "__main__":
    main()

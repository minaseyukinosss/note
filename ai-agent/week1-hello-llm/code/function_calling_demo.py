"""
Day 5-7：Function Calling 完整链路。

LLM 输出 tool_calls → 我们执行假函数 → 把结果以 role=tool 塞回 → 再请求得到最终回答。

运行：python function_calling_demo.py
"""

import json

from config import get_client, get_model

# 工具定义：description 是 LLM 决定是否调用的主要依据
TOOLS = [
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
]


def get_weather(city: str) -> str:
    """假天气数据，练习用。"""
    return f"{city} 今天晴，气温 25°C，湿度 40%。"


def dispatch_tool(name: str, arguments_json: str) -> str:
    args = json.loads(arguments_json or "{}")
    if name == "get_weather":
        return get_weather(args.get("city", "未知城市"))
    return f"未知工具: {name}"


def run_with_tools(user_question: str, verbose: bool = True) -> str:
    client = get_client()
    model = get_model()

    messages: list = [
        {
            "role": "system",
            "content": "你是助手。需要查天气时请调用 get_weather，拿到结果后用自然语言回答用户。",
        },
        {"role": "user", "content": user_question},
    ]

    # 第一轮：LLM 可能返回 tool_calls，也可能直接回答
    resp = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=TOOLS,
    )
    msg = resp.choices[0].message

    if verbose:
        print("--- 第 1 轮响应 ---")
        print("content:", msg.content)
        print("tool_calls:", msg.tool_calls)

    if not msg.tool_calls:
        return msg.content or ""

    # 把 assistant 消息（含 tool_calls）写入历史
    messages.append(msg.model_dump(exclude_none=True))

    for call in msg.tool_calls:
        fn = call.function
        result = dispatch_tool(fn.name, fn.arguments)
        if verbose:
            print(f"\n--- 执行工具 {fn.name}({fn.arguments}) ---")
            print("observation:", result)

        messages.append(
            {
                "role": "tool",
                "tool_call_id": call.id,
                "content": result,
            }
        )

    # 第二轮：基于 observation 生成最终回答
    resp2 = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=TOOLS,
    )
    final = resp2.choices[0].message.content or ""

    if verbose:
        print("\n--- 第 2 轮（最终回答）---")
        print(final)
        if resp2.usage:
            print(f"\n（本轮 tokens: {resp2.usage.total_tokens}）")

    return final


def main() -> None:
    question = "北京今天天气怎么样？"
    print("用户问题:", question, "\n")
    run_with_tools(question)


if __name__ == "__main__":
    main()

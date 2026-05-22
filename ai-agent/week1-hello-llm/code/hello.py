"""
Day 1-2：第一次 LLM 调用。

运行：python hello.py
"""

from config import get_client, get_model


def main() -> None:
    client = get_client()
    model = get_model()

    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "你是一个简洁的中文助手。"},
            {"role": "user", "content": "用一句话解释什么是 LLM。"},
        ],
    )

    print("模型:", model)
    print("回答:", resp.choices[0].message.content)
    if resp.usage:
        print(
            "Token:",
            f"prompt={resp.usage.prompt_tokens},",
            f"completion={resp.usage.completion_tokens},",
            f"total={resp.usage.total_tokens}",
        )


if __name__ == "__main__":
    main()

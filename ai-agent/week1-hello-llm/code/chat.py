"""
Day 3-4：终端多轮对话。

命令：
  /exit   退出
  /clear  清空对话历史
  /temp 0.7  设置 temperature（0~2）

运行：python chat.py
"""

from config import get_client, get_model

SYSTEM_PROMPT = "你是一个简洁的中文助手。"


def main() -> None:
    client = get_client()
    model = get_model()
    temperature = 0.7

    messages: list[dict[str, str]] = [
        {"role": "system", "content": SYSTEM_PROMPT},
    ]

    print(f"多轮对话已启动（模型: {model}）")
    print("输入 /exit 退出，/clear 清空历史，/temp 0.7 改温度\n")

    while True:
        try:
            user_input = input("你: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n再见。")
            break

        if not user_input:
            continue
        if user_input == "/exit":
            print("再见。")
            break
        if user_input == "/clear":
            messages = [{"role": "system", "content": SYSTEM_PROMPT}]
            print("（历史已清空）\n")
            continue
        if user_input.startswith("/temp "):
            try:
                temperature = float(user_input.split(maxsplit=1)[1])
                print(f"（temperature = {temperature}）\n")
            except (IndexError, ValueError):
                print("用法: /temp 0.7\n")
            continue

        messages.append({"role": "user", "content": user_input})

        resp = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
        )
        assistant_msg = resp.choices[0].message.content or ""
        messages.append({"role": "assistant", "content": assistant_msg})

        print(f"助手: {assistant_msg}")
        print(f"messages: {messages}")
        if resp.usage:
            print(f"  （本轮 total tokens: {resp.usage.total_tokens}）\n")
        else:
            print()


if __name__ == "__main__":
    main()

"""共用配置：从 .env 读取 API Key、Base URL、模型名。"""

import os
import sys

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def get_model() -> str:
    return os.getenv("OPENAI_MODEL", "deepseek-chat")


def get_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print(
            "未找到 OPENAI_API_KEY。请执行：\n"
            "  cp .env.example .env\n"
            "  然后在 .env 中填入你的 Key。",
            file=sys.stderr,
        )
        sys.exit(1)

    base_url = os.getenv("OPENAI_BASE_URL")
    if base_url:
        return OpenAI(api_key=api_key, base_url=base_url)
    return OpenAI(api_key=api_key)

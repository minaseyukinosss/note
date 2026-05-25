"""共用配置：从 .env 读取 API Key、Base URL、模型名。"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


def _load_env() -> None:
    code_dir = Path(__file__).resolve().parent
    topic_dir = code_dir.parent.parent  # ai-agent/
    load_dotenv(topic_dir / ".env")
    load_dotenv(code_dir / ".env", override=True)


_load_env()


def get_model() -> str:
    return os.getenv("OPENAI_MODEL", "deepseek-chat")


def get_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print(
            "未找到 OPENAI_API_KEY。请任选其一：\n"
            "  cp ai-agent/.env.example ai-agent/.env   # 主题级共用（推荐）\n"
            "  cp .env.example .env                     # 仅本周 code 目录",
            file=sys.stderr,
        )
        sys.exit(1)

    base_url = os.getenv("OPENAI_BASE_URL")
    if base_url:
        return OpenAI(api_key=api_key, base_url=base_url)
    return OpenAI(api_key=api_key)

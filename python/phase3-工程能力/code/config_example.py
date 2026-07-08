"""配置管理参考示例：pydantic-settings。

这是 Agent 项目里管理 API Key / 模型名 / 超时的标准做法，
替代散落各处的 os.getenv，带类型校验和默认值。

依赖：uv add pydantic-settings
运行前在同目录放一个 .env（参考 .env.example），然后：
    uv run python config_example.py
"""

from __future__ import annotations

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """全局配置。字段名对应环境变量（大小写不敏感）。"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # 必填：没配就在启动时报错，而不是运行到一半才 KeyError
    openai_api_key: str = Field(..., description="LLM API Key")

    # 带默认值的可选项
    openai_base_url: str = "https://api.openai.com/v1"
    model: str = "gpt-4o-mini"
    request_timeout: float = 30.0
    max_retries: int = 3


@lru_cache
def get_settings() -> Settings:
    """单例：全应用共享一份配置，只解析一次。"""
    return Settings()  # type: ignore[call-arg]


if __name__ == "__main__":
    settings = get_settings()
    # 打印时注意不要泄露 key，这里只展示前缀
    print("model      :", settings.model)
    print("base_url   :", settings.openai_base_url)
    print("timeout    :", settings.request_timeout)
    print("key prefix :", settings.openai_api_key[:6], "...")

"""
Day 17-19：Agent 工具定义。

三工具与手写版 react_agent.py 行为一致，区别是 LangChain @tool 装饰器：
  - 函数 docstring → 工具的 description（模型靠它决定何时调用）
  - 参数类型注解 → JSON schema 的 parameters

search 已接入 Tavily 真搜索；get_weather 仍是 mock（练习用）。
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.tools import tool

# 与 config.py 相同：优先读 ai-agent/.env，再读 code/.env（后者可覆盖）
_code_dir = Path(__file__).resolve().parent
_topic_dir = _code_dir.parent.parent
load_dotenv(_topic_dir / ".env")
load_dotenv(_code_dir / ".env", override=True)


def tavily_search(query: str) -> str:
    # 核心三步：client.search → 取 answer + results → 拼成字符串 observation
    from tavily import TavilyClient

    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return "错误：未配置 TAVILY_API_KEY"

    response = TavilyClient(api_key=api_key).search(
        query=query,
        search_depth="basic",
        max_results=3,
        include_answer=True,
    )

    parts: list[str] = []
    if answer := response.get("answer"):
        parts.append(f"摘要：{answer}")
    for i, r in enumerate(response.get("results", []), 1):
        parts.append(f"[{i}] {r['title']}\n{r['content']}\n来源：{r['url']}")

    return "\n\n".join(parts) or "未找到相关结果"


@tool
def get_weather(city: str) -> str:
    """查询指定城市的当前天气。"""
    # mock：固定返回，不调用真实天气 API（学习阶段够用）
    return f"{city} 今天晴，气温 25°C，湿度 40%。"


@tool
def calculator(expression: str) -> str:
    """计算数学表达式，支持 + - * / 和括号。"""
    try:
        # 白名单字符，防止 eval 执行任意代码
        allowed = set("0123456789+-*/(). ")
        if not all(c in allowed for c in expression):
            return "错误：表达式含不允许的字符"
        value = eval(expression, {"__builtins__": {}}, {})  # noqa: S307
        return str(value)
    except ZeroDivisionError:
        return "错误：除数不能为 0"
    except Exception as exc:
        return f"错误：{exc}"


@tool
def search(query: str) -> str:
    """搜索互联网实时信息。"""
    return tavily_search(query)


# bind_tools / ToolNode 都从这里取工具列表
ALL_TOOLS = [get_weather, calculator, search]

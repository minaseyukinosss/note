"""与 Week2 react_agent.py 行为一致的三工具（LangChain @tool 形式）。"""

from langchain_core.tools import tool


@tool
def get_weather(city: str) -> str:
    """查询指定城市的当前天气。"""
    return f"{city} 今天晴，气温 25°C，湿度 40%。"


@tool
def calculator(expression: str) -> str:
    """计算数学表达式，支持 + - * / 和括号。"""
    try:
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
    """搜索网络信息（练习用假数据）。"""
    return f"【假搜索结果】关于「{query}」：暂无实时数据，这是固定占位文本。"


ALL_TOOLS = [get_weather, calculator, search]

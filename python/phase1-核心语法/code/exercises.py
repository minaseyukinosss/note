"""阶段一 核心语法练习。

用法：实现每个 TODO 函数，然后取消文件底部对应 assert 的注释，运行验证：

    python exercises.py

每题都附了 Python 意图说明和它在 Agent 项目里的用途。
"""

from __future__ import annotations


# ---------------------------------------------------------------------------
# 1. 真值规则：安全判断"空"
#    [] / {} / "" / 0 / None 都是假值，直接 if not items 即可
#    Agent 用途：判断 LLM 返回 / 检索结果是否为空
# ---------------------------------------------------------------------------
def is_empty(items: list | dict | str | None) -> bool:
    """空 list / dict / 空字符串 / None 都算空，返回 True。"""
    # TODO: 一行实现（利用 Python 真值规则）
    # raise NotImplementedError
    if not items:
        return True
    return False


# ---------------------------------------------------------------------------
# 2. 切片：取最近 N 条消息
#    xs[-n:] 取最后 n 个；Agent 用途：截断上下文、保留最近 N 轮对话
# ---------------------------------------------------------------------------
def last_n(messages: list, n: int) -> list:
    """返回最后 n 条；n 超过长度时返回全部。"""
    # TODO: 用切片实现
    # raise NotImplementedError
    return messages[-n:]


# ---------------------------------------------------------------------------
# 3. dict.get：安全取值 + 默认
#    d.get(k, default) 在 key 不存在时返回 default 而非报错
#    Agent 用途：解析可能缺字段的 API 响应 / 配置
# ---------------------------------------------------------------------------
def get_timeout(config: dict) -> int:
    """取 config['timeout']，没有则默认 30。"""
    # TODO: 用 .get 实现
    # raise NotImplementedError
    return config.get("timeout", 30)


# ---------------------------------------------------------------------------
# 4. 推导式：过滤 + 转换
#    [表达式 for x in xs if 条件]：一行完成过滤 + 转换
#    Agent 用途：从 messages 里挑出并转换需要的字段
# ---------------------------------------------------------------------------
def user_contents(messages: list[dict]) -> list[str]:
    """取出所有 role == 'user' 的 content。"""
    # TODO: 用列表推导式一行实现
    # raise NotImplementedError
    return [m["content"] for m in messages if m["role"] == "user"]


# ---------------------------------------------------------------------------
# 5. set：去重且保持"是否包含"的 O(1) 判断
# ---------------------------------------------------------------------------
def unique_tools(names: list[str]) -> set[str]:
    """返回去重后的工具名集合。"""
    # TODO
    # raise NotImplementedError
    return set(names)


# ---------------------------------------------------------------------------
# 6. 可变默认参数陷阱：写出"正确"版本
#    错误写法：def append_log(msg, logs=[]) —— logs 会跨调用共享！
# ---------------------------------------------------------------------------
def append_log(msg: str, logs: list[str] | None = None) -> list[str]:
    """把 msg 追加到 logs 并返回；不传 logs 时每次都应是全新的 list。"""
    # TODO: 用 None 作为哨兵，函数内再初始化
    # raise NotImplementedError
    if logs is None:
        logs = []
    logs.append(msg)
    return logs


# ---------------------------------------------------------------------------
# 7. *args / **kwargs 透传：模拟框架里的包装函数
# ---------------------------------------------------------------------------
def call_with_defaults(func, *args, **kwargs):
    """给 func 注入默认 temperature=0.7（若调用方未指定），再透传其余参数。"""
    # TODO: 若 kwargs 里没有 temperature，补上 0.7，再 return func(*args, **kwargs)
    # raise NotImplementedError
    if "temperature" not in kwargs:
        kwargs['temperature'] = 0.7
    return func(*args, **kwargs)


# ---------------------------------------------------------------------------
# 8. 闭包：计数器工厂
#    内层函数记住外层变量；Agent 用途：回调、工厂函数、装饰器的底层
# ---------------------------------------------------------------------------
def make_counter():
    """返回一个每次调用自增并返回当前值的函数。"""
    # TODO: 用 nonlocal 实现
    # raise NotImplementedError
    count = 0
    def counter():
        nonlocal count
        count += 1
        return count
    return counter


# ---------------------------------------------------------------------------
# 9. 综合：按 role 分组消息（Day 13 自加题）
#    dict 推导式 + .get；Agent 用途：按 role 拆分对话、统计各角色发言
# ---------------------------------------------------------------------------
def group_by_role(messages: list[dict]) -> dict[str, list[str]]:
    """返回 {role: [content, ...]}，同一 role 的 content 按出现顺序收集。"""
    # 步骤 1：收集 messages 里出现过的所有 role（去重）
    # 提示：集合推导式 { ... for m in messages }
    roles = {m.get("role") for m in messages}

    # 步骤 2：对每个 role，筛出属于它的 content，组成 dict
    # 提示：dict 推导式 { role: [...] for role in roles }
    #       内层列表可用列表推导式 + m.get("role") 做条件
    result = { role: [m.get("content") for m in messages if m.get("role") == role] for role in roles}

    return result


# ---------------------------------------------------------------------------
# 10. 综合：扁平化嵌套 dict（Day 13 自加题）
#    递归 + {**a, **b} 合并；Agent 用途：展平嵌套 JSON 配置 / tool 参数
# ---------------------------------------------------------------------------
def flatten_dict(d: dict, parent_key: str = "", sep: str = ".") -> dict:
    """把 {"a": {"b": 1}, "c": 2} 变成 {"a.b": 1, "c": 2}。"""
    result: dict = {}

    for key, value in d.items():
        # 步骤 1：拼出当前 key 的完整路径
        # 提示：顶层 parent_key 为空时直接用 key；否则 f"{parent_key}{sep}{key}"
        full_key = parent_key + sep + key if parent_key else key

        if isinstance(value, dict):
            # 步骤 2a：嵌套 dict → 递归，把子结果合并进 result
            # 提示：{**result, **flatten_dict(...)}
            result = {**result, **flatten_dict(value, full_key, sep)} 
        else:
            # 步骤 2b：叶子值 → 直接写入 result[full_key] = value
            result[full_key] = value

    return result


# ---------------------------------------------------------------------------
# 11. 异常处理：安全转换（Day 15）
#    try/except 捕获具体异常；Agent 用途：解析 LLM 输出 / API 字段时容错
# ---------------------------------------------------------------------------
def safe_int(s: str, default: int = 0) -> int:
    """把 s 转成 int；无法转换时返回 default，不抛异常。"""
    # TODO: try int(s)，捕获 ValueError 返回 default
    try:
        return int(s)
    except ValueError:
        return default


# ---------------------------------------------------------------------------
# 12. 自定义异常 + EAFP（Day 16）
#    EAFP = 先做了再说，错了再 except（Easier to Ask Forgiveness than Permission）
#    LBYL = 先 if 检查再操作（Look Before You Leap）
#    本题用 EAFP：直接 int(s)，失败 raise MalformedLineError（为 Day 21 JSONL CLI 铺垫）
# ---------------------------------------------------------------------------
class MalformedLineError(Exception):
    """字符串无法按预期格式解析。"""


def parse_int(s: str) -> int:
    """把 s 转成 int；失败时 raise MalformedLineError（带 s 的信息）。"""
    # TODO: EAFP 写法 —— 直接 try int(s)，失败再 raise MalformedLineError
    # 提示：raise MalformedLineError(f"...") from e  保留原始原因链
    # raise NotImplementedError
    try:
        return int(s)
    except ValueError as e:
        raise MalformedLineError(f"无法解析字符串: {s}") from e


if __name__ == "__main__":
    # 实现后逐个取消注释验证
    assert is_empty([]) and is_empty("") and is_empty(None) and not is_empty([1])
    assert last_n([1, 2, 3, 4], 2) == [3, 4]
    assert last_n([1], 5) == [1]
    assert get_timeout({}) == 30 and get_timeout({"timeout": 5}) == 5
    assert user_contents([{"role": "user", "content": "hi"}, {"role": "system", "content": "x"}]) == ["hi"]
    assert unique_tools(["a", "b", "a"]) == {"a", "b"}
    assert append_log("x") == ["x"] and append_log("y") == ["y"]  # 不共享！
    assert call_with_defaults(lambda **k: k["temperature"]) == 0.7
    c = make_counter(); assert (c(), c(), c()) == (1, 2, 3)
    assert group_by_role([
        {"role": "user", "content": "hi"},
        {"role": "assistant", "content": "hello"},
        {"role": "user", "content": "bye"},
    ]) == {"user": ["hi", "bye"], "assistant": ["hello"]}
    assert flatten_dict({"a": {"b": 1, "c": {"d": 2}}, "e": 3}) == {
        "a.b": 1, "a.c.d": 2, "e": 3,
    }
    assert safe_int("42") == 42 and safe_int("abc", default=-1) == -1
    assert parse_int("99") == 99
    try:
        parse_int("abc")
        assert False, "应抛出 MalformedLineError"
    except MalformedLineError as e:
        assert "abc" in str(e)
    print("全部通过。把上面 assert 取消注释来逐题验证。")

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
    raise NotImplementedError


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
    # c = make_counter(); assert (c(), c(), c()) == (1, 2, 3)
    print("全部通过。把上面 assert 取消注释来逐题验证。")

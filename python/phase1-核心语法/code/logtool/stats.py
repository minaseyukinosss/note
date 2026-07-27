"""统计解析后的记录（Day 20 实现 count_by_level）。"""

from .parser import MalformedLineError  # 包内相对导入：`.` = 当前包 logtool


def count_by_level(records: list[dict]) -> dict[str, int]:
    """按 level 字段计数，缺 level 的记为 unknown。"""
    raise NotImplementedError("Day 20：在此实现 count_by_level")

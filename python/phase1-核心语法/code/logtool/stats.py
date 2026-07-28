"""统计解析后的记录（Day 20 实现 count_by_level）。"""

from collections import defaultdict


def count_by_level(records: list[dict]) -> dict[str, int]:
    """按 level 字段计数，缺 level 的记为 unknown。"""
    counts: defaultdict[str, int] = defaultdict(int)
    for record in records:
        level = record.get("level", "unknown")
        counts[level] += 1
    return dict(counts)

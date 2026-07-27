"""解析 JSONL 单行与整文件（Day 19 实现逻辑）。"""


class MalformedLineError(Exception):
    """单行内容无法解析为合法 JSON 对象。"""


def parse_line(line: str) -> dict:
    """把一行 JSON 解析为 dict；失败抛 MalformedLineError。"""
    raise NotImplementedError("Day 19：在此实现 parse_line")


def read_lines(path: str) -> tuple[list[dict], int]:
    """读文件，返回 (好行 records, 坏行计数)。"""
    raise NotImplementedError("Day 19：在此实现 read_lines")

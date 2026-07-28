"""解析 JSONL 单行与整文件（Day 19 实现逻辑）。"""

import json


class MalformedLineError(Exception):
    """单行内容无法解析为合法 JSON 对象。"""


def parse_line(line: str) -> dict:
    """把一行 JSON 解析为 dict；失败抛 MalformedLineError。"""
    text = line.strip()
    if not text:
        raise MalformedLineError("empty line")
    try:
        obj = json.loads(text)
    except json.JSONDecodeError as e:
        raise MalformedLineError(f"invalid JSON: {text!r}") from e
    if not isinstance(obj, dict):
        raise MalformedLineError(
            f"expected JSON object, got {type(obj).__name__}: {text!r}"
        )
    return obj


def read_lines(path: str) -> tuple[list[dict], int]:
    """读文件，返回 (好行 records, 坏行计数)。"""
    records: list[dict] = []
    bad_count = 0
    with open(path, encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()
            if not stripped:
                continue
            try:
                records.append(parse_line(stripped))
            except MalformedLineError:
                bad_count += 1
    return records, bad_count

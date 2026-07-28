"""CLI 入口：在 code/ 目录下执行 `python -m logtool`。"""

from __future__ import annotations

import sys

from . import __version__
from .parser import read_lines
from .stats import count_by_level


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    if not args:
        print(f"logtool {__version__}")
        print("用法: python -m logtool <file.jsonl>")
        return 0

    path = args[0]
    try:
        records, bad_count = read_lines(path)
    except FileNotFoundError:
        print(f"文件不存在: {path!r}", file=sys.stderr)
        return 1

    counts = count_by_level(records)
    print(f"good: {len(records)}")
    print(f"bad: {bad_count}")
    print("level:")
    for level in sorted(counts):
        print(f"  {level}: {counts[level]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

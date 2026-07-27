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
        print("Day 18：包与相对导入已就绪；Day 19–20 补解析与统计。")
        return 0

    path = args[0]
    # Day 20 会真正调用下面两行；现在 import 成功即说明相对导入没问题
    _ = read_lines, count_by_level, path
    print(f"logtool {__version__}: 收到文件 {path!r}，完整流程 Day 20 接通。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

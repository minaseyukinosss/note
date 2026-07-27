"""JSONL 日志分析 CLI（阶段一 Day 18–21 验收项目）。

从包外使用（把 `code/` 加入路径或 `python -m` 运行）：

    from logtool import MalformedLineError, parse_line

包内模块之间用相对导入，例如 `from .parser import MalformedLineError`。
"""

__version__ = "0.1.0"

from .parser import MalformedLineError, parse_line, read_lines
from .stats import count_by_level

__all__ = [
    "MalformedLineError",
    "__version__",
    "count_by_level",
    "parse_line",
    "read_lines",
]

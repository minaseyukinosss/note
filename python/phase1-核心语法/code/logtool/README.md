# logtool：JSONL 日志分析 CLI

阶段一 Day 18–21 的验收项目。Day 18 只搭包结构；Day 19–20 填实现。

## 目录即「包」

```
logtool/
├── __init__.py    # 包标识；可汇总对外 API
├── parser.py      # 模块：解析
├── stats.py       # 模块：统计（包内 from .parser import ...）
└── __main__.py    # python -m logtool 的入口
```

- **模块**：一个 `.py` 文件（如 `parser.py`）。
- **包**：含 `__init__.py` 的目录（如 `logtool/`），里面可以再嵌套子包。

## 怎么跑

必须在 **`code/`** 目录下用 **`-m`**，让 Python 把 `logtool` 当成包加载（相对导入才合法）：

```bash
cd python/phase1-核心语法/code
python -m logtool
python -m logtool sample.jsonl   # Day 20 起会真正分析
```

## 相对导入 vs 绝对导入

| 写法 | 谁用 | 含义 |
| --- | --- | --- |
| `from logtool.parser import parse_line` | 包**外**的脚本（`code/` 在路径上） | 绝对导入 |
| `from .parser import parse_line` | **包内** `stats.py`、`__main__.py` | 相对导入，`.` = 当前包 `logtool` |

⚠️ 不要这样跑入口（相对导入会炸）：

```bash
python logtool/__main__.py   # ❌
```

## Day 18 自测

```bash
python -m logtool
python -c "from logtool import MalformedLineError; print(MalformedLineError)"
```

# 阶段三：Python 工程能力（Day 46-66）

> 目标：从"会写脚本"到"会做项目"。让 Agent 代码有结构、可配置、可测试、可维护。

## 本阶段解决什么问题

- "我的 Agent 代码全堆在一个文件里，怎么分层？"
- "API Key、模型名硬编码在代码里，怎么做配置管理？"
- "调试全靠 print，怎么上真正的日志？"
- "怎么给工具函数写测试？LLM 调用怎么 mock？"

## 现代 Python 工程栈（记住这四个）

| 工具 | 作用 |
| --- | --- |
| **uv** | 包管理 + 虚拟环境 + 运行（一个命令搞定依赖和执行） |
| **ruff** | lint + format（一个顶 flake8 + black + isort） |
| **pyright** | 类型检查（配合类型注解静态查错） |
| **pytest** | 测试（fixture / 参数化 / mock） |

## 学习顺序

1. **项目结构 + uv**（Day 46-50）：`src/` 布局、`uv init/add/run/sync`、`pyproject.toml`、`uv.lock`。
2. **配置管理**（Day 53-55）：`pydantic-settings`、`.env`、分环境。
3. **日志系统**（Day 56-59）：`logging` 层级、结构化日志、`rich`。
4. **测试**（Day 60-63）：pytest、fixture、参数化、mock / monkeypatch。
5. **代码质量**（Day 64-65）：ruff、pyright、pre-commit。
6. **综合实战**（Day 66）：把阶段二代码重构成标准工程。

## 建议的项目结构

```text
my-agent/
├── pyproject.toml          # 依赖 + 工具配置（ruff/pyright/pytest）
├── uv.lock                 # 锁定版本
├── .env.example            # 配置示例（不放真 key）
├── src/
│   └── my_agent/
│       ├── __init__.py
│       ├── config.py       # pydantic-settings 配置
│       ├── logging.py      # 日志初始化
│       ├── core/           # Agent 核心逻辑
│       └── tools/          # 工具
└── tests/
    └── test_core.py
```

## 快速上手命令

```bash
# 安装 uv（macOS）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 新建工程
uv init my-agent && cd my-agent
uv add pydantic pydantic-settings httpx rich
uv add --dev pytest ruff pyright

# 日常
uv run python -m my_agent      # 运行
uv run pytest                  # 测试
uv run ruff check . && uv run ruff format .
uv run pyright
```

## 笔记 `notes/`

- [01-学习手册](./notes/01-学习手册.md)

## 验收标准

- [ ] 能用 uv 从零建一个标准工程，说清 `pyproject.toml` 各段作用。
- [ ] 能用 `pydantic-settings` 从 `.env` 读配置，并做分环境。
- [ ] 能配置分级日志（DEBUG/INFO/WARNING），并用 `rich` 美化输出。
- [ ] 能给函数写 pytest 测试，并用 `monkeypatch` mock 掉一个网络调用。
- [ ] ruff check、ruff format、pyright 三者零报错。
- [ ] 完成：把阶段二的 mini_chain 重构进标准工程并补测试。

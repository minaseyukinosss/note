# Week4 代码占位

实跑到对应天数时再创建脚本。建议骨架（与 [`../README.md`](../README.md) 一致）：

| 文件 | 对应天数 | 说明 |
| --- | --- | --- |
| `build_index.py` | Day 22-23 | 读取 `knowledge/*.md`，切分 + embedding + 写入向量库（幂等） |
| `retrieve.py` | Day 22-23 | 独立检索脚本，给定 query 返回 top-k chunk + 来源 |
| `rag_agent.py` | Day 24-26 | 基于 Week3 [`langgraph_agent.py`](../../week3-langgraph/code/langgraph_agent.py)，新增 `retrieve` 工具 |
| `eval_rag.py` | Day 27-28 | 跑 golden cases，输出召回 / 引用 / 幻觉指标 |
| `knowledge/` | — | 本地 markdown 知识库（可放 `ai-agent/` 其他笔记的副本或软链） |

环境变量与依赖沿用主题根目录的 `ai-agent/.venv` 与 `requirements.txt`，新增包等实际选型确定后再加。

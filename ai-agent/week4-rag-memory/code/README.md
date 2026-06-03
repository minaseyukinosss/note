# Week4 代码

| 文件 | 对应天数 | 状态 |
| --- | --- | --- |
| `build_index.py` | Day 22-23 | ✅ 已实现 |
| `retrieve.py` | Day 22-23 | ✅ 已实现 |
| `rag_agent.py` | Day 24-26 必做 | ✅ 已实现 |
| `eval_rag.py` | Day 27-28 进阶 | 待实现 |
| `knowledge/` | — | 3 篇本地 markdown 知识库 |

Week4 的代码优先级：先跑通 `rag_agent.py` 与 W4-001 ~ W4-003；再做 `eval_rag.py`、W4-004 ~ W4-005。

## Day 24-26 跑法

```bash
.venv/bin/python week4-rag-memory/code/rag_agent.py
```

内置 W4-001 ~ W4-003 三条 demo，verbose 模式会打印 trace 与引用校验结果。

## Day 22-23 跑法

```bash
cd ai-agent
source .venv/bin/activate
pip install -r requirements.txt

python week4-rag-memory/code/build_index.py
python week4-rag-memory/code/retrieve.py "ReAct 是什么"
python week4-rag-memory/code/retrieve.py "强化学习 PPO 算法"   # W4-003：应未命中
python week4-rag-memory/code/retrieve.py "今天股票涨了吗" --raw   # 观察原始分数
```

技术选型：Chroma 本地持久化 + 默认 onnx embedding（`all-MiniLM-L6-v2`）+ `MarkdownHeaderTextSplitter`。

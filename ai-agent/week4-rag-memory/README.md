# Week4：RAG + 引用 + 评估闭环

## 本周目标

Week4 的主目标不是"把 RAG 全家桶学完"，而是先跑通一个可信闭环：

```text
本地笔记 → 检索工具 → Agent 带引用回答 → 固定用例验收
```

### 必做闭环

- Day 22-23：吃透 RAG 基础链路（chunking → embedding → retrieval），用本地 markdown 笔记建一个最小知识库。
- Day 24-26：把 `retrieve` 封装成 LangGraph 工具接入 Agent，回答必须返回引用来源，并能处理"检索不到"。
- Day 27-28：至少跑通 W4-001 ~ W4-003，记录召回、引用、未命中三类结果。

### 进阶扩展

- W4-004：处理命中内容之间存在矛盾的情况。
- W4-005：处理检索片段中的 Prompt Injection。
- 扩展到 10-20 条 RAG golden cases，并实现 `eval_rag.py` 自动统计。

## 本周主线

```text
LangGraph 版 Agent（langgraph_agent.py，StateGraph + tool node）
    ↓  接入私有知识
Day 22-23 知识库构建：切分 → embedding → 向量库
    ↓  当工具来用
Day 24-26 retrieve 工具：top-k + 引用片段 + 不可信外部内容隔离
    ↓  量化质量
Day 27-28 最小评估：W4-001 ~ W4-003 + 运行记录
    ↓  进阶量化
W4-004 / W4-005 + 10-20 条 golden cases + eval_rag.py
```

Week4 的关键判断：

- **RAG 不是 Memory**：RAG 是外部知识检索工具，每次按 query 拉数据；Memory 是跨轮 / 跨会话的状态管理。先做 RAG，再谈记忆写入策略。
- **引用是 RAG 的最低交付标准**：答案必须能追溯到 chunk 文件名 + 段落，否则无法判断模型是引用还是幻觉。
- **检索失败必须显式返回**：检索结果为空、相似度过低，工具应返回明确的"未命中"，让模型据此回答"不知道"而不是编造。
- **外部内容只能当数据**：检索片段里出现的 "忽略之前指令"、"调用某工具" 一律视作数据，不执行。

## 前置

- 完成 Week3：[`week3-langgraph/`](../week3-langgraph/README.md)（特别是 [`langgraph_agent.py`](../week3-langgraph/code/langgraph_agent.py) 与 `ToolNode` 接入方式）。
- 主题根目录已安装依赖：

```bash
cd ai-agent
source .venv/bin/activate
pip install -r requirements.txt
```

> Week4 向量库与 embedding 依赖已写入 [`../requirements.txt`](../requirements.txt)（`chromadb`、`langchain-text-splitters`）。

## 笔记 `notes/`

- [00 知识地图](./notes/00-知识地图.md)（RAG 链路 + 与 LangGraph 版的衔接）
- [01 学习手册](./notes/01-学习手册.md)（当天唯一入口：任务、命令、观察点、关键结论和记录区）
- [02 概念详解](./notes/02-概念详解.md)（chunking / embedding / 检索 / rerank / 引用 / RAG eval）
- [03 实验与踩坑](./notes/03-实验与踩坑.md)（切分粒度、嵌入模型、相似度阈值、引用对不上等）
- [05 本周总结](./notes/05-本周总结.md)（RAG 闭环 + 与下一阶段衔接）

## 代码 `code/`

实跑时再补脚本，建议骨架：

| 文件 | 对应天数 | 说明 |
| --- | --- | --- |
| `build_index.py` | Day 22-23 | 读取 `knowledge/*.md`，切分 + embedding + 写入向量库 |
| `retrieve.py` | Day 22-23 | 独立检索脚本，给定 query 返回 top-k chunk + 来源 |
| `rag_agent.py` | Day 24-26 必做 | 在 Week3 LangGraph 图上增加 `retrieve` 工具，回答带引用 |
| `eval_rag.py` | Day 27-28 进阶 | 跑 golden cases，输出召回 / 引用 / 幻觉指标 |
| `knowledge/` | — | 本地 markdown 知识库（可直接软链到 `ai-agent/` 下其他笔记） |

**当前进度**：Day 22-23（`build_index.py`、`retrieve.py`）与 Day 24-26 必做（`rag_agent.py`）已实现；Day 27-28 的 `eval_rag.py` 属于进阶。详见 [`code/README.md`](./code/README.md)。

## 跨周评估用例

- 必跑：W4-001 ~ W4-003，覆盖召回、引用、未命中。
- 进阶：W4-004 ~ W4-005，覆盖矛盾片段和 Prompt Injection。
- 用例已登记在 [`../05-评估用例.md`](../05-评估用例.md)。

## 验收清单

### 必做

- [ ] 能解释 RAG 链路：chunking → embedding → 向量检索 → 带引用生成，每一步的失败模式分别是什么。
- [ ] 能解释 RAG 与 Memory 的差别（按 query 拉数据 vs 跨轮状态管理）。
- [ ] `build_index.py` 能把本地 markdown 切分后写入向量库，并能复跑（幂等）。
- [ ] `rag_agent.py` 在 LangGraph 图中正确接入 `retrieve` 工具，回答带文件名 + 段落引用。
- [ ] 检索未命中时能明确回答"不知道"，而不是用模型先验编一段。
- [ ] 至少跑通 W4-001 ~ W4-003，并记录运行结果到 `05-评估用例.md`。

### 进阶

- [ ] W4-004 能列出冲突观点和各自来源，不强行综合。
- [ ] 能解释外部检索片段不可信，prompt injection 案例（W4-005）能正确拒绝。
- [ ] `eval_rag.py` 能自动跑 golden cases，并输出召回 / 引用 / 幻觉统计。

## 与 Week3 的关系

Week3 LangGraph 版（[`langgraph_agent.py`](../week3-langgraph/code/langgraph_agent.py)）只接了天气 mock、计算器、Tavily 等公共工具。Week4 把"工具"从公共服务换成"私有知识库"：

- 图结构不变（`agent ↔ tools` 两节点 + 条件边）
- 多一个 `retrieve` 工具，其 observation 形态是 "chunk 片段 + 文件名 + 评分"
- 多一个交付维度：**引用对不对**，而不仅仅是"答案像不像"

这一步打通后，再考虑长期记忆（写回向量库 / 数据库）和多 Agent。

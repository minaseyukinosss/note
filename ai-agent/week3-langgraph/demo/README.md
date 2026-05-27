# Week3 Demo 交付

## 场景

每日科技新闻摘要：Tavily 搜索 + LangGraph StateGraph + checkpoint 多轮续聊。

## 目录

| 文件 | 用途 | 状态 |
| --- | --- | --- |
| [示例对话.md](./示例对话.md) | 3 条示例对话 | 已填 |
| [trace.md](./trace.md) | 1 条 messages / trace 日志 | 已填 |
| [边界用例.md](./边界用例.md) | 1 条失败或边界用例 | 已填 |
| [评估记录.md](./评估记录.md) | W3-001 / W3-004 评估用例运行记录 | 已填 |
| [../code/news_demo.py](../code/news_demo.py) | Demo 脚本 | 已跑通 |

## 运行

```bash
cd ai-agent
source .venv/bin/activate
python week3-langgraph/code/news_demo.py
```

## 验收清单

- [x] Demo 脚本能跑通
- [x] 3 条示例对话已记录
- [x] 至少 1 条 trace / messages 日志
- [x] 至少 1 条边界用例
- [x] 至少 2 条评估用例运行记录（W3-001 + W3-004）

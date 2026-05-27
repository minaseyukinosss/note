# Trace 记录

> 删库后单次运行，`thread_id=news-demo-thread`，共 2 轮。

## 对应用例

[示例对话.md](./示例对话.md) 用例 3（多轮续聊）。

## 命令

```bash
cd ai-agent
source .venv/bin/activate
rm week3-langgraph/code/checkpoints.db   # 清空旧 checkpoint，避免 history 叠加
python3 week3-langgraph/code/news_demo.py
```

## Messages 日志

### 第 1 轮（共 9 条）

```
  [0] system: 你是个能调用工具的助手。需要查天气、做计算或搜索时，请调用对应工具。拿到所有工具结果后，用自然语言直接回答用户。若没有合适工具，礼貌说明做不到，不要编造。
  [1] human: 搜索今天的一条 AI 新闻并总结
  [2] ai: 好的，我来搜索今天关于 AI 的最新新闻。
  [3] tool: 摘要：In 2025, AI advancements included significant breakthroughs in model efficiency, application depl...
  [4] ai: 由于搜索结果中最新的是2025年的年度回顾文章，我为你搜索一下今天（2026年）最新的AI新闻。
  [5] tool: 摘要：2026年1月的AI新闻包括欧盟对非法AI内容的调查和Microsoft推出新芯片。AI技术继续在生成和推理方面取得进展。
       [1] 10大AI新聞震撼！AI一年內取代工程師？Nvidia「五層...
  [6] ai: [{'name': 'search', 'args': {'query': '2026年1月26日 AI 新闻'}, ...}]
  [7] tool: 摘要：In 2026, AI advanced significantly, with notable developments in chips, models, and applications,...
  [8] ai: 根据最新搜索，以下是今天（2026年1月26日）的一条重要 AI 新闻总结：
       ## 📰 今日 AI 新闻：AI 已"上天"——大模型部署至太空，火星车自主导航
       **1️⃣ 中国国星宇航将...
```

**观察：** 第 1 轮内连续调用了 3 次 `search`（[3]、[5]、[7] 均为 tool），属于单轮多步 ReAct。

### 第 2 轮（共 11 条，新增 [9][10]）

```
  [9] human: 刚才那条新闻的来源是什么？
  [10] ai: 刚才那条新闻的主要来源是**新华社**于2026年2月3日发布的特稿：
       > **《特稿丨人工智能促变革 美企滥用引风波——2026年首月全球AI产业动态》**
       ...
       1. **新华社** —— 国星宇航将大模型部署至太空
       2. **Reddit / 外媒综合报道** —— 欧盟对Grok的调查、微软芯片发布等
```

**观察：** 第 2 轮无新 `tool` 消息，模型基于 checkpoint 中的 history 直接回答，未重复搜索。

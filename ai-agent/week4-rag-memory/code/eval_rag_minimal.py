"""
极简评估脚本 — 只测 W4-003（未命中），约 40 行。

完整版 eval_rag.py 是在这个模式上：
  1. 定义「问题 + 期望」
  2. 调 invoke_agent 拿结果
  3. 几个 if 判断 → Pass / Fail

你能读懂并改这个文件，就算「会写 eval」的入门。

运行：
  .venv/bin/python week4-rag-memory/code/eval_rag_minimal.py
"""

from rag_agent import invoke_agent

# --- 第 1 步：固定用例（和 05-评估用例.md 里 W4-003 一样）---
QUESTION = "我的笔记里有没有关于强化学习 PPO 算法的介绍？"

# --- 第 2 步：跑 Agent ---
print("问题:", QUESTION)
result = invoke_agent(QUESTION)
print("回答:", result.answer[:200], "...\n")

# --- 第 3 步：用 if 检查期望（失败原因存列表里）---
failures = []

# 期望 1：必须调了 retrieve
if not result.retrieve_called:
    failures.append("没调 retrieve")

# 期望 2：知识库没有 PPO，检索应该未命中
if result.retrieve_had_hits:
    failures.append("应该未命中，但 retrieve 返回了 hits")

# 期望 3：要说「知识库没有相关内容」一类的话
if "知识库" not in result.answer:
    failures.append("未命中时没说「知识库…」")

# 期望 4：不能凭通识编 PPO 内容
if "PPO 是" in result.answer or "Proximal Policy" in result.answer:
    failures.append("在未命中时编造了 PPO 内容")

# --- 第 4 步：汇总 ---
if failures:
    print("判定: Fail")
    for f in failures:
        print(" -", f)
else:
    print("判定: Pass")

# 想扩展到 W4-001？复制上面 4 步，换 QUESTION 和 if 条件即可。
# 想扩展到 5 条？把 QUESTION + checks 放进一个 list，用 for 循环 —— 那就是 eval_rag.py 的 CASES。

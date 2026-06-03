# ReAct 与 Function Calling

## Function Calling 是什么

Function Calling 是 LLM 与外部世界交互的**协议层**：模型输出结构化的 tool call（函数名 + JSON 参数），调用方负责执行真实函数，并把结果作为 observation 写回上下文。

它本身不是 Agent。单次调用 + 一次工具执行，仍然是 Augmented LLM，不是循环。

## ReAct 是什么

ReAct（Reason + Act）是把 Function Calling 放入**控制循环**后的结构：

```text
Thought → Action（tool call）→ Observation → Thought → … → Final Answer
```

手写版 [`react_agent.py`](../../../week2-react-agent/code/react_agent.py) 用 `for` 循环实现；LangGraph 版用 `agent ↔ tools` 两节点 + 条件边实现。行为接近，组织方式不同。

## 二者关系

| 维度 | Function Calling | ReAct |
| --- | --- | --- |
| 层级 | 协议 / 接口 | 控制结构 |
| 是否循环 | 否（单次） | 是（多轮直到停止） |
| 谁决定下一步 | 外层代码 | 模型根据 observation 决定 |
| 典型产物 | 一次 tool call + 结果 | 多轮 tool call + 最终自然语言回答 |

## 常见踩坑

- 把 Function Calling 当成 Agent：只调一次工具不算 Agent。
- 工具 docstring 写得太模糊：模型选错工具或根本不调用。
- observation 格式不一致：模型难以从失败中恢复。

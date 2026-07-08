# 学习笔记仓库

> 个人技术学习的沉淀地。坚持每日输出 → 形成可复用的知识库。

## 目录导航

| 主题 | 简介 | 入口 |
| --- | --- | --- |
| JavaScript | JS 语言核心机制（闭包、原型、异步…） | [`javascript/`](./javascript/README.md) |
| Webpack | 6 周系统学习：从最小配置到源码阅读 | [`webpack/`](./webpack/README.md) |
| AI Agent | LLM Agent 学习路线：工具协议 / ReAct / LangGraph / RAG / 评估 | [`ai-agent/`](./ai-agent/README.md) |
| Python | 面向 TS 背景的 90 天 Python 提升计划（Agent 工程 + 源码阅读） | [`python/`](./python/README.md) |

## 仓库约定

- 每个主题目录下都有自己的 `README.md` 作为索引。
- 含代码的实践项目，统一拆分为：
  - `notes/`：学习笔记、复盘、Quiz
  - `code/`：可运行的最小示例工程
- 仓库不提交 `node_modules/`、`dist/`、`*.lock`，需要本地自行 `npm install`。

## 本地阅读

```bash
git clone <this-repo>
cd note
# 直接阅读 markdown，或用 VSCode / Obsidian / Typora 打开
```

## 跑示例代码

```bash
cd webpack/week1-minimal/code
npm install
npm run build   # 或 npm start，详见各 week 的 README
```

## License

[MIT](./LICENSE)

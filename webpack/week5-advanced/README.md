# Week5：高级场景与架构扩展

## 本周内容
- 多入口（MPA）配置示例。
- Module Federation host/remote 最小示例。
- 中型团队构建方案设计文档（含 Monorepo 与 Polyfill 策略）。

## 笔记 `notes/`
- [团队构建方案设计文档](./notes/design-doc.md)

## 代码 `code/`
- [`code/mpa-demo/`](./code/mpa-demo)：多入口（home/admin）示例
- [`code/federation-demo/`](./code/federation-demo)：Module Federation host + remote

```bash
# MPA
cd code/mpa-demo && npm install && npm run build

# Module Federation（分别启动 remote 与 host）
cd code/federation-demo/remote && npm install && npm start
cd code/federation-demo/host   && npm install && npm start
```

## 建议实践顺序
1. 先跑 `mpa-demo`，理解多入口与多 HTML 输出。
2. 再跑 `federation-demo`，理解 host/remote 的运行方式。
3. 对照 `design-doc.md`，按你团队现状做一次定制化重写。

## 验收清单
- 能解释 MPA 与 SPA 在构建层的核心差异。
- 能说清 Module Federation 的"构建时解耦、运行时组合"特点。
- 能输出一份可落地的团队构建方案文档。

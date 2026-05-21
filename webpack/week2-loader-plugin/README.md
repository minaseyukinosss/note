# Week2：Loader 与 Plugin 机制

## 本周目标
- 理解 loader 的职责与执行位置。
- 理解 plugin 在 compiler 生命周期中的介入方式。
- 手写并验证一个 loader 与一个 plugin。

## 笔记 `notes/`
- [Day 1 笔记](./notes/week2-day1-notes.md)
- [Day 2 笔记](./notes/week2-day2-notes.md)
- [Day 3 笔记](./notes/week2-day3-notes.md)
- [Day 4 笔记](./notes/week2-day4-notes.md)
- [Week2 总结](./notes/week2-summary.md)

## 代码 `code/`
```bash
cd code
npm install
npm run build
npm run build:prod
npm run typecheck
```

关键实现：
- `code/src/index.ts`：TypeScript 入口，经 `ts-loader` + 自定义 loader 处理。
- `code/loaders/banner-loader.js`：给每个 TS/JS 模块注入注释头。
- `code/plugins/build-report-plugin.js`：在 `done` hook 输出构建报告（耗时、产物大小）。

## 验收清单
- 构建后在 `dist/bundle.js` 顶部可见注入注释。
- 命令行能看到 plugin 输出的 build report。
- 能解释 loader 与 plugin 的边界：
  - loader：转换模块源码。
  - plugin：监听并扩展构建生命周期。

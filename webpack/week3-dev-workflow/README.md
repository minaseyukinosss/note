# Week3：开发体验工程化

## 本周目标
- 完成配置拆分：`webpack.common.js` / `webpack.dev.js` / `webpack.prod.js`。
- 在开发环境启用 HMR。
- 明确开发与生产 Source Map 策略。
- 使用 `DefinePlugin` 注入环境变量。
- 将 ESLint / Stylelint / TypeScript 串联到检查流程。

## 笔记 `notes/`
- [Day 1 笔记](./notes/week3-day1-notes.md)
- [Day 2 笔记](./notes/week3-day2-notes.md)

## 代码 `code/`
```bash
cd code
npm install
npm run check
npm run build
npm run dev
```

关键点说明：
- `code/webpack.common.js`：公共 entry、TS 规则、HTML 模板、环境变量注入。
- `code/webpack.dev.js`：`eval-cheap-module-source-map` + `devServer.hot`。
- `code/webpack.prod.js`：`source-map` + CSS 抽离与压缩。

## 验收清单
- `npm run check` 全部通过。
- `npm run dev` 可热更新 `src/message.ts`。
- 构建后可在产物中看到注入的 `APP_TITLE` 值。

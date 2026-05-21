# Week1：最小可用 Webpack 配置

## 本周目标
- 理解 Entry / Output / Module / Bundle 的关系。
- 在同一项目中同时处理 ESM 与 CommonJS。
- 处理 CSS 与静态资源（`asset/resource`）。
- 通过 `webpack-dev-server` 启动本地开发服务。

## 笔记 `notes/`
- [Day 1 学习笔记](./notes/day1-learning-notes.md)
- [Day 2 学习笔记](./notes/day2-learning-notes.md)
- [Day 3 学习笔记](./notes/day3-learning-notes.md)
- [Week1 复盘 Quiz](./notes/week1-review-quiz.md)
- [Week1 总结](./notes/week1-summary.md)

## 代码 `code/`
```bash
cd code
npm install
npm run build
npm run dev
npm run typecheck
```

目录说明：
- `code/src/index.ts`：入口文件（TypeScript），演示 ESM + CommonJS + CSS + 资源引用。
- `code/src/esm-util.ts`：ESM 示例模块。
- `code/src/commonjs-util.cjs`：CommonJS 示例模块。
- `code/src/styles.css`：样式处理示例。
- `code/src/assets/logo.svg`：资源模块示例。
- `code/webpack.config.js`：最小 Webpack 配置。

## 验收清单
- 能说明"入口文件如何生成最终 `bundle.js`"。
- 能解释为什么 `css-loader` 与 `style-loader` 需要组合使用。
- 能解释 `asset/resource` 的输出规则与文件命名行为。

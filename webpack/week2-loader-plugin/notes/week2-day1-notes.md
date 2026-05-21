# Webpack Week2 Day1 学习笔记

## 今日完成
- 跑通 `week2-loader-plugin` 项目并完成构建验证。
- 阅读并理解 `loaders/banner-loader.js` 的实现逻辑。
- 阅读并理解 `plugins/build-report-plugin.js` 的实现逻辑。
- 修改 banner 文案并在 `dist/bundle.js` 中确认生效。
- 能用代码证据解释 loader/plugin 的职责边界。

## 核心理解

### 1) Loader 是源码转换器
- 输入：模块源码字符串（`source`）。
- 输出：转换后的源码字符串（返回值会作为该模块后续打包输入）。
- 入口为 `src/index.ts`，处理链为 `ts-loader` → `banner-loader`（先编译 TS，再注入注释）。
- 本项目证据：`banner-loader` 返回 ``/* banner */ + source``，最终体现在 `dist/bundle.js` 顶部注释。

### 2) Plugin 是生命周期扩展器
- 通过 `apply(compiler)` 进入 webpack 生命周期。
- 通过 `compiler.hooks.xxx.tap(...)` 在指定阶段挂入自定义逻辑。
- 本项目证据：`BuildReportPlugin` 在 `done` 阶段读取 `stats` 并输出构建报告。

### 3) `done` hook 的触发时机
- 一次构建流程结束时触发（可读到 `assets/time/errors/warnings`）。
- 适合做收尾逻辑：构建汇总、日志上报、通知输出。

## 代码证据速记
- `loaders/banner-loader.js`：
  - `module.exports = function bannerLoader(source) { ... return ... }`
- `plugins/build-report-plugin.js`：
  - `apply(compiler) { compiler.hooks.done.tap(...)}`
- `webpack.config.js`：
  - `module.rules[].use.loader` 注册 loader
  - `plugins: [new BuildReportPlugin()]` 注册 plugin

## 口述标准答案（可直接复述）
- Loader 是源码转换器，因为它接收模块源码并返回转换后的新源码，作用在单模块层面。
- Plugin 是生命周期扩展器，因为它通过 hooks 介入编译流程，在特定阶段执行扩展逻辑。
- `done` hook 在构建结束后触发，适合输出构建统计和收尾报告。

## 当前薄弱点（待补）
- 生命周期全景仍不完整（目前只重点掌握 `done`）。
- 还未做“故意构建失败”来验证 hook 输出差异。

## Day2 计划
- 在插件中增加 `stats.hasErrors()` 分支，验证成功/失败差异。
- 再增加一个 hook（如 `compile` 或 `emit`）做阶段对照。
- 补充一页“hook 时机速查表”。

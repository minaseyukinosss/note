# Webpack Week2 Day2 学习笔记

## 今日目标
- 验证 `compile` 与 `done` 的触发先后关系。
- 验证成功/失败构建时 `done` 的表现差异（`stats.hasErrors()`）。
- 形成“如何判断 hook 时机”的可复用方法。

## 本次改动
- 文件：`plugins/build-report-plugin.js`
- 已新增：
  - `compiler.hooks.compile.tap(...)`
  - `stats.hasErrors()` 输出逻辑

---

## 实验 1：成功构建路径

### 操作
- 执行：`npm run build`

### 观察（填写）
- 日志中是否出现 `[hook] compile: start`：出现了
- 日志中是否出现 `[hook] done: success=true`：出现了
- `Build Report` 是否有 `assets/time/output`：有
- 日志顺序（写成箭头）：`[hook] compile: start -> webpack 编译输出 -> [hook] done: success=true -> Build Report`

### 结论（填写）
- `compile` 的触发时机：编译启动阶段，模块构建前后很早的阶段就会触发。
- `done` 的触发时机：本次编译结束阶段（可读取 stats、assets、errors/warnings）。
- 两者关系：`compile` 先于 `done`，分别代表“开始”与“结束”。

---

## 实验 2：失败构建路径

### 操作
- 在 `src/index.ts` 人为制造语法错误（例如少 `}`）。
- 执行：`npm run build`
- 验证完成后恢复正确代码。

### 观察（填写）
- `compile` 是否仍触发：触发了
- `done` 是否仍触发：触发了
- `done` 中 success 是否为 `false`：是的
- 报错信息是否出现在报告中：出现了（摘要：`Module parse failed: Unexpected token` 或 TS 编译错误，处理链含 `ts-loader` 与 `./loaders/banner-loader.js`）。

### 结论（填写）
- 构建失败时 `done` 是否还会执行：会
- `stats.hasErrors()` 在失败场景下的价值：可在同一插件内快速区分成功/失败路径，用于输出不同日志、触发告警或中断后续流程。

---

## 核心概念（填写你自己的一句话解释）
- `compile hook`：webpack 编译开始时触发的生命周期钩子，适合做初始化日志与预处理。
- `done hook`：webpack 编译结束时触发的生命周期钩子，适合做汇总报告与收尾动作。
- `stats.hasErrors()`：用于判断本次构建是否存在错误的布尔判断方法。
- `plugin`：通过 `apply + hooks` 介入 webpack 生命周期，扩展构建流程能力的机制。

---

## 今日口述标准答案（可直接背）
- `compile` 是编译开始阶段的 hook，适合做启动日志或预处理。
- `done` 是本次编译结束阶段的 hook，适合做构建汇总与收尾输出。
- `stats.hasErrors()` 能快速判断本次构建是否成功，便于在同一插件中区分成功/失败处理逻辑。
- 我通过 `success=true/false` 与错误输出验证了：`done` 在成功与失败构建都会触发，只是 `stats` 内容不同。

---

## 验收清单（纯文本）
- 已完成：我能解释 `compile` 与 `done` 的触发先后。
- 已完成：我能解释失败构建下 `done` 的行为。
- 已完成：我能解释 `stats.hasErrors()` 的用途。
- 已完成：我能用“代码证据”说明 plugin 是生命周期扩展器。

---

## 明日计划（Week2 Day3）
- 尝试再加一个 hook（如 `emit`）与 `done` 对照。
- 补一页“常见 hook 速查表（开始/处理中/收尾）”。

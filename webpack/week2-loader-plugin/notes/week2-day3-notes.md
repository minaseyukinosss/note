# Webpack Week2 Day3 学习笔记

## 今日目标
- 通过新增 `emit` hook 建立生命周期阶段感知。
- 对照成功/失败构建日志，验证 `compile -> emit -> done` 顺序。
- 形成 hook 时机速查表，便于后续扩展 plugin。

## 本次改动
- 文件：`plugins/build-report-plugin.js`
- 已新增：
  - `compiler.hooks.emit.tap(...)`
  - 输出 `[hook] emit: assetCount=...`

---

## 实验 1：成功构建日志对照

### 观察
- 关键日志顺序：`[hook] compile: start -> [hook] emit: assetCount=1 -> [hook] done: success=true`
- 构建结果：`compiled successfully`
- 报告内容：可读取 `mode/time/output/assets`

### 结论
- `compile` 是开始阶段。
- `emit` 在产物准备输出阶段（可拿到 `compilation.assets`）。
- `done` 是编译结束阶段（可拿到最终 `stats`）。

---

## 实验 2：失败构建日志对照

### 观察
- 关键日志顺序仍为：`compile -> emit -> done`
- `done` 结果：`success=false`
- 报告中出现 `errors: 1` 与具体错误：
  - `Module parse failed: Unexpected token`
  - 并提示处理链包含 `./loaders/banner-loader.js`

### 结论
- 构建失败时，`done` 仍会触发，只是 `stats` 中错误信息不同。
- `stats.hasErrors()` 可稳定区分成功/失败路径，用于差异化处理。
- 报错中出现 loader 链提示，表示该文件在解析失败前经过了对应 loader，不代表 loader 本身必然有问题。

---

## hook 时机速查表（当前已验证）
- `compile`：编译开始阶段；适合初始化日志、预处理。
- `emit`：准备输出资源阶段；适合读取/修改 `compilation.assets`。
- `done`：编译结束阶段；适合汇总报告、通知、收尾动作。

---

## 口述标准答案（可直接背）
- 本项目通过 `compile`、`emit`、`done` 三个 hook 建立了生命周期对照：先开始编译，再进入资源输出阶段，最后编译结束。
- 在成功和失败构建下，hook 顺序保持一致，但 `done` 的 `stats` 内容不同。
- `stats.hasErrors()` 是插件里区分成功/失败逻辑的关键判断条件。

---

## 今日验收清单（纯文本）
- 已完成：我能解释 `compile -> emit -> done` 的顺序与职责。
- 已完成：我能解释失败构建时 `done` 仍会执行。
- 已完成：我能解释 `emit` 为什么能读取 `assetCount`。
- 已完成：我能用日志证据说明 plugin 是生命周期扩展器。

---

## 下一步建议（Week2 Day4 / 收官）
- 再补一个 `tapAsync/tapPromise` 小实验，理解异步 hook 写法差异。
- 汇总 Week2 Day1~Day3 为一页总复盘，准备进入 Week3。

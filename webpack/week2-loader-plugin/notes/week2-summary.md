# Webpack Week2 收官总结（Loader & Plugin）

## 一、Week2 完成情况
- Day1：跑通自定义 `loader` 与 `plugin`，完成 banner 注入与构建报告验证。
- Day2：验证 `compile` / `done` 先后关系，验证成功/失败构建下 `done` 行为与 `stats.hasErrors()` 用法。
- Day3：新增 `emit` hook，对照 `compile -> emit -> done` 生命周期顺序，形成 hook 速查结论。
- Day4：补齐异步 hook 认知（`tap` / `tapAsync` / `tapPromise`）与常见踩坑（`callback/resolve`）。

---

## 二、核心能力达成

### 1) Loader 能力
- 能解释 loader 本质：输入模块源码，输出转换后的新源码。
- 能通过 `banner-loader` 证明“返回值即新源码”的机制。
- 能从构建产物中定位 loader 改造结果（banner 注释）。

### 2) Plugin 能力
- 能解释 plugin 本质：通过 `apply + hooks` 介入 webpack 生命周期。
- 能在 `BuildReportPlugin` 中读取 `stats` 输出构建报告。
- 能理解并验证：报错信息中出现 loader 链不代表 loader 本身错误，而是处理链上下文。

### 3) 生命周期能力
- 已验证顺序：`compile -> emit -> done`。
- 能解释阶段职责：
  - `compile`：编译开始
  - `emit`：资源输出准备阶段
  - `done`：编译结束收尾阶段

### 4) 成功/失败构建判断
- 已掌握 `stats.hasErrors()` 用于区分成功/失败路径。
- 已验证失败构建时 `done` 仍会触发，只是 `stats` 内容不同。

### 5) 异步 Hook 能力
- `tap`：同步
- `tapAsync`：异步回调，必须调用 `callback()`
- `tapPromise`：Promise 异步，必须 `resolve()`
- 已理解常见卡住原因：忘记 `callback/resolve`。

---

## 三、Week2 口述标准答案（面试可复述）
> Week2 我重点掌握了 webpack 的 loader 与 plugin 机制。Loader 作用在模块源码层面，输入源码并返回转换后的新源码；Plugin 作用在构建流程层面，通过 `apply + hooks` 介入生命周期。我在自定义插件中验证了 `compile -> emit -> done` 的顺序，并通过 `stats.hasErrors()` 区分成功与失败构建。同时补齐了异步 hook 写法差异：`tapAsync` 需要 `callback`，`tapPromise` 需要 Promise 正确 `resolve`，否则构建会卡住。

---

## 四、现阶段薄弱点（已识别）
- 对 webpack 全量 hooks 图谱还不熟（目前掌握常用核心阶段）。
- 对更复杂 plugin 场景（改写 assets、多插件协作）还缺实战。

---

## 五、进入 Week3 前检查清单
- 已完成：能清晰区分 loader 与 plugin 的边界。
- 已完成：能口述 `compile -> emit -> done` 顺序及职责。
- 已完成：能解释 `stats.hasErrors()` 的作用。
- 已完成：能解释 `tap/tapAsync/tapPromise` 差异与结束信号要求。
- 已完成：有 Day1~Day4 笔记沉淀，具备复习资料闭环。

---

## 六、Week3 建议起步
- 从配置分层入手：`webpack.common.js / webpack.dev.js / webpack.prod.js`
- 聚焦开发流：HMR、SourceMap、环境变量注入
- 串联质量保障：TypeScript + ESLint + Stylelint


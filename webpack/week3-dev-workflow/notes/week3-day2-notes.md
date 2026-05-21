# Webpack Week3 Day2 复习笔记

## 今日目标
1. 验证 `DefinePlugin` 注入的值，是否会被业务代码正确消费并渲染到页面。
2. 理解开发/生产下 `devtool` 的差异，以及它对 `source map` 产物（例如 `*.map`）和调试体验的影响。

---

## 1. `DefinePlugin`：从注入到消费的完整链路

### 1.1 `DefinePlugin` 做了什么（原理）
`DefinePlugin` 不是运行时读取环境变量，它发生在 **构建期**：
- 把代码里的某个表达式（本项目是 `process.env.APP_TITLE`）替换成 **字面量常量**
- 最终你看到的其实是“替换后的代码”，而不是运行时再去查真实环境变量。

### 1.2 本项目对应在哪里（映射）
注入位置：`webpack.common.js`
- 注入目标：`process.env.APP_TITLE`
- 注入方式：`JSON.stringify(env.APP_TITLE || "Webpack Week3")`

消费位置：`src/index.ts`
- 通过模板字符串渲染到页面：
  - `<h2>${process.env.APP_TITLE}</h2>`

### 1.3 如何验证（复现）
1. 启动开发服务：`npm run dev`
2. 打开页面，检查标题 `h2` 是否等于脚本传入的 `APP_TITLE`（你当前 dev 脚本是 `WebpackWeek3`）

补充要点（避免混淆）：
- 如果你只改了业务代码但没触发重新编译，可能看不到效果；注入值来自构建期替换，通常需要重新构建/刷新页面后才会改变。

### 1.4 一句话背诵
`DefinePlugin` 在构建期把 `process.env.APP_TITLE` 替换成字符串常量，所以业务代码运行时直接拿到替换后的值。

---

## 2. `devtool`：开发 vs 生产的取舍（以及 `source-map` 产物）

### 2.1 `devtool` 控制什么（原理）
`devtool` 决定了 webpack 生成 `source map` 的方式与粒度，核心取舍是：
- **开发**：更快的构建/重编译与基本可用的调试定位
- **生产**：更稳定、可追踪的错误定位（通常会更强调 map 的可用性）

### 2.2 本项目配置对应哪里（映射）
开发：`webpack.dev.js`
- `devtool: "eval-cheap-module-source-map"`

生产：`webpack.prod.js`
- `devtool: "source-map"`

### 2.3 如何验证产物差异（复现）
1. 开发模式：
   - `npm run dev` 一般不会在磁盘 `dist/` 里持续生成 `*.map`
   - 原因：开发服务器通常用内存提供资源；并且 `eval-*` 方案的 sourcemap 形态与输出落盘行为不完全等同于 `source-map`
2. 生产模式：
   - `npm run build` 后，`dist/` 目录里通常能看到 `*.map` 文件

### 2.4 一句话背诵
开发用 `eval-cheap-module-source-map` 偏速度；生产用 `source-map` 往往会输出独立 `*.map`，方便线上排错定位。

---

## 常见误区澄清（你今天问到的点）
- `npm run dev` 不等于生成 `dist/`：`webpack-dev-server` 通常不把每次构建结果写回磁盘 `dist/`（资源更多是在内存里提供）。
- `output.clean: true` 只有在真正写盘产物时才更容易观察到效果；纯 `serve` 场景下你可能看不到它清理/更新 `dist` 的痕迹。

---

## 今日口述标准答案（可直接背）
> 今天验证了两件事：第一，`DefinePlugin` 在构建期把 `process.env.APP_TITLE` 替换为字符串常量，并在 `src/index.ts` 的 `<h2>` 中被消费渲染，说明注入链路可用。第二，开发与生产的 `devtool` 不同：生产使用 `source-map` 通常会生成 `*.map` 产物便于线上定位，而开发使用 `eval-cheap-module-source-map` 更偏构建速度与调试体验。

---

## 明天方向（Day3）
1. 更深入理解 `source map` 产物与浏览器调试体验之间的关系（断点、堆栈定位、映射质量等）。
2. 若时间充足：对比一次“修改注入值/修改 message”后在 dev/prod 的构建输出与调试效果差异。


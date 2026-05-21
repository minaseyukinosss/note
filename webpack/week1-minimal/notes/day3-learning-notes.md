# Webpack 第1周 Day3 学习笔记

## 配置项口述（优化版）
- `entry`：指定构建起点文件。Webpack 从这里递归收集依赖，形成依赖图，再结合 loader/plugin 处理后输出产物。
- `output.path`：指定构建产物输出的绝对目录。不配置时会用默认目录（通常是 `dist`）。
- `output.filename`：定义输出 JS 文件名模板（如 `bundle.js`、`[name].[contenthash].js`）。其中 `[name]` 是 chunk 名，`[contenthash]` 是基于文件内容生成的哈希，内容不变哈希不变、内容变化哈希变化，便于长期缓存。
- `output.clean`：每次构建前清空输出目录，避免旧产物残留导致引用混乱。
- `module.rules`：定义“哪些文件命中哪些规则，并经过哪些 loader 处理”，本质是模块转换策略。
- `plugins`：在构建生命周期中扩展能力（如生成 HTML、注入环境变量、产物分析等），不直接做源码链式转换。
- `devServer.static`：开发服务器静态资源根目录，浏览器请求静态文件时从该目录提供。
- `devServer.port`：开发服务器监听端口，决定本地访问地址（如 `http://localhost:9001`）。
- `mode`：指定构建模式（`development` / `production`），影响默认优化策略与调试体验。

## 配置项验收（不配会怎样）
- `entry` 不配：Webpack 无法确定从哪里开始构建，打包无法按预期进行。
- `output.path` 不配：输出路径不可控，难以管理产物目录。
- `output.filename` 不配：输出文件命名不可控，长期缓存策略难实施。
- `output.clean` 不配：旧文件可能残留，导致页面错误引用旧资源。
- `module.rules` 不配：非 JS 资源（如 CSS/图片）可能无法正确处理。
- `plugins` 不配（以 HtmlWebpackPlugin 为例）：不会自动生成/注入 HTML，手动维护成本高。
- `devServer.static` 不配：静态资源访问路径可能异常。
- `devServer.port` 不配：端口不可控，可能与本地其他服务冲突。

## Day3 实验记录

### 实验 1：修改 `output.filename`
- 操作：
  - 从 `bundle.js` 改为 `app.js`
- 观察：
  - `dist` 产物变化：主 JS 产物从 `bundle.js` 变为 `app.js`。
  - `index.html` 注入脚本变化：`HtmlWebpackPlugin` 自动将脚本引用从 `bundle.js` 更新为 `app.js`。
- 结论：
  - `output.filename` 决定主产物命名，修改后会直接反映到输出文件名。
  - 在使用 `HtmlWebpackPlugin` 时，HTML 注入跟随最新构建产物自动更新，无需手动改 `<script>` 标签。

### 实验 2：资源输出目录定制
- 操作：
  - `asset/resource` 添加 `generator.filename: "assets/[name].[hash][ext]"`
- 观察：
  - 图片输出路径变化：图片文件进入 `dist/assets/` 目录。
  - JS 中资源 URL 变化：`app.js` 中资源路径带有 `assets/...` 前缀。
- 结论：
  - `generator.filename` 可精细控制资源输出目录与命名规则，便于按类型分目录管理产物。
  - 资源模块输出路径变化会同步反映到 JS 中的资源 URL 引用。

### 实验 3：修改 `devServer.port`
- 操作：
  - 端口从 `9001` 改为 `9002`
- 观察：
  - 启动地址变化：变为 `http://localhost:9002`。
  - 是否与现有端口冲突：无冲突，服务正常启动。
- 结论：
  - `devServer.port` 直接决定本地开发服务监听端口，适合按团队规范或本机环境调整。
  - 端口冲突时可快速切换端口恢复开发链路，无需改业务代码。

## 今日收获
- 我已掌握的 5 个点：
  1. 能解释并验证 `output.filename` 对产物命名和 HTML 注入的影响。
  2. 能通过 `generator.filename` 控制资源模块输出目录和命名规则。
  3. 能通过修改 `devServer.port` 调整本地服务地址并排查端口冲突。
  4. 能说清配置项作用，并回答“不配会怎样”。
  5. 能把“改配置 -> 看产物 -> 解释原因”做成闭环。
- 我仍模糊的 2 个点：
  1. `mode`、`devtool` 与最终产物可读性/体积的更细粒度关系。
  2. `plugin` 生命周期钩子的执行顺序与典型使用时机（计划在 Week2 深入）。
- 我进入 Week2 前要补的 1 个点：
  - 补完“仅保留 `style-loader`”实验，形成 loader 边界的完整验证闭环。

## Runtime 补强总结（Week1 收官补充）
- `dist/app.js` 中的 runtime 辅助函数不是固定全量注入，而是 webpack 根据“当前项目代码与配置”按需生成。
- `d/r/n/o` 主要用于模块语义与兼容：
  - `d`：定义导出 getter（ESM 命名导出映射）。
  - `r`：标记模块为 ESM（`__esModule` 等）。
  - `n`：兼容默认导出读取（常见于 ESM/CJS 互操作）。
  - `o`：`hasOwnProperty` 的 runtime 工具函数。
- `p`（`__webpack_require__.p`）用于资源路径前缀（publicPath），与模块语义函数职责不同。
- 结论：runtime 不是固定模板拷贝，而是“按场景拼装的最小能力集合”。

## Runtime 定位模板（读 `dist/app.js` 的固定顺序）
- 第 1 步：定位 `var __webpack_modules__ = ({`  
  - 作用：模块定义区（每个源码模块被包装成函数）。
- 第 2 步：定位 `var __webpack_module_cache__ = {};`  
  - 作用：模块缓存区（避免重复执行同一模块）。
- 第 3 步：定位 `function __webpack_require__(moduleId)`  
  - 作用：核心加载函数（加载、执行、返回模块导出）。
- 第 4 步：定位 runtime 辅助函数（`d/r/n/o`）与 `__webpack_require__.p`  
  - 作用：模块语义兼容 + 资源路径前缀（publicPath）。
- 第 5 步：定位 startup（`__webpack_require__("./src/index.ts")`）  
  - 作用：入口启动执行。

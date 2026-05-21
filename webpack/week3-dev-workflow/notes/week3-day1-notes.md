# Webpack Week3 Day1 学习知识笔记

## 今日主题
- 配置分层与开发体验工程化
- HMR 实际生效路径
- Source Map 策略理解
- 环境变量注入与消费链路

---

## 1) 配置分层核心
- `webpack.common.js`：公共配置层
  - 放共用配置（`entry`、`resolve`、通用 `module.rules`、公共插件等）
  - 目的：减少重复、统一行为、降低维护成本
- `webpack.dev.js`：开发配置层
  - 强调开发速度与调试体验（如 `devtool`、`devServer`、`hot`）
- `webpack.prod.js`：生产配置层
  - 强调产物质量与可发布性（压缩、抽离、稳定追踪）

---

## 2) Source Map 认知
- `eval-cheap-module-source-map`（开发）
  - 目标：更快增量编译与调试反馈
  - 特点：速度优先，映射精度偏“够用”
- `source-map`（生产）
  - 目标：更完整、可追踪的错误定位
  - 特点：构建成本更高，通常会生成独立 map 文件

---

## 3) DefinePlugin 注入链路
- 注入位置：`webpack.common.js`
- 注入方式：`DefinePlugin` 在构建阶段做常量替换
- 消费位置：`src/index.ts` 中通过 `process.env.APP_TITLE` 使用
- 本质：构建期注入 -> 运行期可读常量

---

## 4) HMR 实战结论
- 仅开启 `devServer.hot: true` 还不够
- 模块更新后若页面不变，常见原因是：
  - `accept` 回调里只打印日志，没有触发业务重渲染
- 正确做法：
  - 抽出 `render()` 函数
  - 首次加载执行 `render()`
  - 在 `module.hot.accept(...)` 回调中再次执行 `render()`
- 关键辨别：
  - “有 HMR 日志”不等于“页面已更新”
  - 只有“不刷新也能看到 UI 变化”才算业务层热更新生效

---

## 5) `npm run dev` vs `npm run build`
- `npm run dev`
  - 启动开发服务器
  - 修改代码后自动重编译并推送更新（HMR/Live Reload）
  - 通常不用于发布产物
- `npm run build`
  - 生成正式构建产物（用于部署）
  - 侧重产物质量与可发布性

---

## 6) 今日排错方法论
- 看日志是否出现 HMR 相关信息（如 `App hot update`）
- 看 `accept` 回调是否真正更新了页面状态/DOM
- 如果“日志更新但页面不变”，优先检查“业务重渲染逻辑是否缺失”

---

## 7) 今日达成
- 能解释 `common/dev/prod` 分层的必要性
- 能说明 `devtool` 在开发与生产中的策略差异
- 能说清 `DefinePlugin` 的注入与消费路径
- 能定位并修复“有 HMR 日志但页面不更新”的问题
- 能区分 `dev` 与 `build` 的职责边界

---

## 8) 一分钟复述模板
> Week3 Day1 我重点掌握了配置分层和开发流闭环：`common` 放共用能力，`dev` 面向开发效率，`prod` 面向发布质量。`devtool` 选择上，开发用 `eval-cheap-module-source-map` 追求反馈速度，生产用 `source-map` 追求定位精度。`DefinePlugin` 在构建期注入常量，并在业务代码里消费。HMR 方面，我验证了“有日志不等于页面更新”，必须在 `module.hot.accept` 回调里触发业务重渲染，才能实现真正的无刷新更新。

## 9) 明日衔接点（Day2）
- 做一次 `APP_TITLE` 注入值切换并对比生产产物差异
- 记录 `dev/prod` 构建产物在可读性和体积上的差异
- 形成 Week3 Day2 的“配置取舍”表


# Webpack 第1周 Day1 学习笔记

## 今日目标与完成情况
- 已完成项目启动与构建：`npm install`、`npm run build`、`npm run dev`。
- 已修复 `index.html` 缺失问题：使用 `HtmlWebpackPlugin` 自动生成 `dist/index.html`。
- 业务源码使用 TypeScript（`src/*.ts` + `ts-loader`），`commonjs-util.cjs` 仍保留用于 CommonJS 对照。
- 已读懂 `dist/app.js` 的核心结构：`模块表 + Runtime + 入口执行`。
- 已完成模块导出实验：`命名导出` 与 `默认导出` 的产物差异定位。
- 已完成新增模块追踪：`extra.ts` 能在模块定义区和入口执行区都定位到。

## 核心主线（Entry -> 依赖图 -> Loader -> Runtime -> Output）
1. `Entry`（入口）  
   - 概念：Webpack 开始构建的起点文件。  
   - 本项目：`src/index.ts`。
2. `Dependency Graph`（依赖图）  
   - 概念：从入口递归收集所有依赖形成的关系图。  
   - 本项目依赖示例：`styles.css`、`esm-util.ts`、`commonjs-util.cjs`、`logo.svg`、`extra.ts`。
3. `Loader`（转换器）  
   - 概念：把不同类型模块转换成 Webpack 可继续处理的模块代码。  
   - 本项目重点：`css-loader` 与 `style-loader` 组合处理 CSS。
4. `Runtime`（运行时代码）  
   - 概念：Webpack 注入的模块加载机制。  
   - 关键对象：`__webpack_modules__`（模块表）、`__webpack_require__`（加载函数）、`__webpack_module_cache__`（缓存）。
5. `Output`（输出）  
   - 概念：决定产物目录与命名规则。  
   - 本项目产物：`dist/bundle.js`、`dist/index.html`、`dist/<hash>.svg`。

## 难点 1：为什么 CSS 最后变成了 JS 逻辑
- `use: ["style-loader", "css-loader"]` 的执行顺序是 **从右到左**。  
- `css-loader` 先执行：把 CSS 文本转换为 JS 模块数据。  
- `style-loader` 后执行：运行时创建 `<style>` 并把 CSS 注入页面。  
- 结论：`bundle.js` 里看到的是“注入样式的 JS 逻辑”，不是把原始 CSS 直接拼接进去。

## 难点 2：ESM 与 CommonJS 的语义差异
- `ESM`（`import/export`）  
  - 静态结构，打包阶段更容易分析依赖。  
  - 导出是 `live binding`（活绑定）。  
  - `Tree Shaking` 友好度更高。
- `CommonJS`（`require/module.exports`）  
  - 更偏运行时加载，动态性更强。  
  - 常见场景下不是 ESM 那种活绑定体验。  
  - `Tree Shaking` 相对弱。
- 本项目混用验证：  
  - `esm-util.ts` 用 ESM。  
  - `commonjs-util.cjs` 用 CommonJS。  
  - 最终都被 Webpack 统一到 `__webpack_require__` 体系中执行。

## 难点 3：Tree Shaking 是什么
- 概念：删除“没有被实际使用”的代码，减小包体积。  
- 成立条件（常见）：  
  - 使用 ESM；  
  - `mode: "production"`；  
  - 模块副作用可判断（或 `sideEffects` 配置合理）。  
- 结论：ESM 的静态结构让 Tree Shaking 更容易准确生效。

## 关键概念清单（用到即解释）
- `Webpack`：前端模块打包器。  
- `Entry`：打包入口。  
- `Dependency Graph`：依赖关系图。  
- `Module`：Webpack 处理单元。  
- `Chunk`：模块分组单位。  
- `Bundle`：输出文件之一。  
- `Loader`：模块转换器。  
- `css-loader`：把 CSS 转为 JS 可处理数据。  
- `style-loader`：把 CSS 注入到 `<style>`。  
- `Asset Modules`：Webpack 5 资源模块能力。  
- `asset/resource`：输出独立文件并返回 URL。  
- `Runtime`：Webpack 注入的加载逻辑。  
- `Module Cache`：模块缓存，避免重复执行。  
- `ESM`：标准模块系统。  
- `CommonJS`：Node 常见模块系统。  
- `Named Export`：命名导出。  
- `Default Export`：默认导出。  
- `Tree Shaking`：移除未使用代码。  
- `HtmlWebpackPlugin`：自动生成 HTML 并注入脚本。  
- `output.clean`：构建前清空输出目录。  
- `Dev Server`：本地开发服务器。

## 今日问题与修复
- 问题：`dist/index.html` 缺失。  
- 原因：`output.clean` 会清空目录，但未自动生成 HTML。  
- 修复：新增 `HtmlWebpackPlugin` + `public/index.html` 模板。

## 今日验收结论
- 我能解释完整主链路：`Entry -> 依赖图 -> Loader -> Runtime -> Output`。  
- 我能在 `bundle.js` 中定位模块定义区和入口执行区。  
- 我能区分 `命名导出` 与 `默认导出` 的产物表现。  
- 我能解释 `ESM/CommonJS` 与 `Tree Shaking` 的关系。

## Day2 计划
- 做 `css-loader` 与 `style-loader` 去留实验，验证职责边界。  
- 对比 `asset/resource` 与 `asset/inline` 的产物差异。  
- 继续练习“从源码定位到产物，从产物反推配置”。

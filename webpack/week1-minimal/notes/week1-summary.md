# Webpack Week1 总结（从零到能解释验证）

## 1. Week1 你完成了什么
- 目录：`webpack-system-study/week1-minimal`
- 已完成的学习与实验：
  - Day1：最小可用 Webpack 配置、产物结构阅读、ESM/CommonJS 与命名/默认导出差异验证、在 `bundle.js` 中定位新增模块
  - Day2：`module.rules[].use` 的执行顺序（右到左）、`css-loader`/`style-loader` 职责边界、`asset/resource` vs `asset/inline` 取舍
  - Day3：配置项理解与“改配置 -> 看产物 -> 解释原因”闭环（`output.filename`、资源输出目录、`devServer.port`）

## 2. 核心主线（你能口述清楚）
Webpack 的完整链路可以概括为：
1. `Entry`（入口）
   - 概念：Webpack 构建的起点文件。
   - 本项目：`src/index.js`
2. `Dependency Graph`（依赖图）
   - 概念：从入口递归解析依赖得到的关系图（模块之间依赖边）。
3. `Loader`（转换器）
   - 概念：当模块类型/语法不是原生可处理形式时，把“模块源码”转换成 webpack 后续可打包形式。
   - 典型：CSS 通过 `css-loader`/`style-loader` 链处理。
4. `Runtime`（运行时代码）
   - 概念：Webpack 注入的模块加载与执行机制（模块表、`__webpack_require__`、模块缓存等），以及必要的语义/资源路径兼容工具（如 `d/r/n/o`、`__webpack_require__.p`）。
5. `Output`（输出）
   - 概念：把最终产物写到磁盘，并由插件补全 HTML 等交付层能力。
   - 本项目：`dist/app.js`（或 `bundle.js` 取决于你对 `output.filename` 的实验）、`dist/index.html`、以及资源文件或内联结果。

## 3. 你在产物里“能定位”的点
- `__webpack_modules__`
  - 作用：模块定义区（每个源码模块被包装成函数映射表）
- `__webpack_module_cache__`
  - 作用：模块执行缓存（避免重复执行）
- `__webpack_require__`
  - 作用：模块加载/执行函数（按 moduleId 执行并返回导出）
- `startup`（如 `__webpack_require__("./src/index.js")`）
  - 作用：入口模块启动执行
- 资源导出
  - `asset/resource`：JS 中通常得到“资源 URL”
  - `asset/inline`：JS 中通常得到“data URL/base64”，不再生成独立文件

## 4. Week1 关键理解（高频面试点）
- `use` 是 loader 链的通用配置项，不是 CSS 专用；`use` 的执行顺序是“右到左”。
- `css-loader` vs `style-loader`：
  - `css-loader`：把 CSS 转成 JS 模块数据（转换）
  - `style-loader`：把 CSS 数据注入 `<style>`（注入）
  - 缺失会导致“构建可能通过但样式不生效”（你已用实验验证）
- `ESM`（`import/export`）与 `CommonJS`（`require/module.exports`）在语义上存在差异；Webpack 会在 runtime 里做兼容与导出读取处理。
- 命名导出与默认导出：
  - 命名导出更明确、易按名字引用
  - 默认导出更适合“一个模块一个主导出”
- Tree Shaking（概念）：
  - 作用：移除未使用代码以减小包体积
  - 常见更依赖 ESM 的静态结构与 production 优化条件

## 5. 你的口述标准答案（简版，可 1 分钟复述）
> 我用 `week1-minimal` 从零理解了 Webpack 的主线：Webpack 从 `Entry`（入口）递归收集 `Dependency Graph`，对不同类型模块使用 `module.rules` 指定的 `Loader` 做转换，然后注入 `Runtime` 实现模块加载与缓存，最后由 `Output` 写出产物并由插件（如 `HtmlWebpackPlugin`）完成交付层生成。  
> 在实验中，我验证了 `use` 的右到左执行顺序，以及 `css-loader` 负责转换、`style-loader` 负责把样式注入 `<style>`；同时对比了 `asset/resource` 输出独立文件 URL 与 `asset/inline` 内联 data URL。  
> 我还能在 `dist` 产物里定位 `__webpack_modules__`、`__webpack_require__` 和入口 `__webpack_require__("./src/index.js")` 来解释产物与源码的对应关系。

## 6. 复习自测建议
- 做 `week1-minimal/week1-review-quiz.md`（你已生成）
- 快速回看：
  - `week1-minimal/day1-learning-notes.md`
  - `week1-minimal/day2-learning-notes.md`
  - `week1-minimal/day3-learning-notes.md`
- 再做一次“改配置 -> 看产物 -> 解释”的快速口述（不必改太多，保证能讲清原因即可）


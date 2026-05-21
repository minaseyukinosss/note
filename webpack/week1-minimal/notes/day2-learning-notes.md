# Webpack 第1周 Day2 学习笔记

## 今日目标
- 理解 `use` 的执行顺序（右到左）。
- 明确 `css-loader` 与 `style-loader` 的职责边界。
- 掌握 `asset/resource` 与 `asset/inline` 的差异与适用场景。

## 先澄清：`use` 到底是什么
- `use` 是 `webpack.config.js` 中 `module.rules` 的配置项，用来声明“命中该规则的文件要经过哪些 loader”。
- `use` 不是样式专用，凡是通过 loader 处理的文件类型都适用（JS/TS/CSS 等）。
- `use` 数组写法是从左到右，但 loader 执行顺序是从右到左。
- 示例：`use: ["style-loader", "css-loader"]` 的真实执行顺序是 `css-loader -> style-loader`。

## 基线信息
- 实验目录：`webpack-system-study/week1-minimal`
- 基线命令：`npm run build`
- 基线结果：
  - 是否构建成功：成功。
  - `dist` 产物文件：`bundle.js`、`index.html`、`<hash>.svg`。
  - 页面样式是否正常：正常。

---

## 实验 1：仅保留 `css-loader`

### 操作
- 修改 `webpack.config.js` 中 CSS 规则为：
  - `use: ["css-loader"]`
- 执行：`npm run build`

### 观察
- 构建是否成功：成功。
- 浏览器页面样式是否生效：不生效（页面样式明显退回默认样式）。
- `bundle.js` 中与 CSS 相关的关键变化：缺少 `style-loader` 注入链路，只有 CSS 被转换为模块数据。

### 结论
- `css-loader` 的职责：把 CSS 文本转换成 JS 模块可消费的数据结构。
- 为什么样式可能不生效：没有 `style-loader` 执行“把 CSS 写入 `<style>` 并插入 DOM”这一步。

---

## 实验 2：仅保留 `style-loader`

### 操作
- 修改 `webpack.config.js` 中 CSS 规则为：
  - `use: ["style-loader"]`
- 执行：`npm run build`

### 观察（待完成）
- 构建是否成功：
- 若报错，核心报错信息：
- `bundle.js` 变化：

### 结论（待完成）
- `style-loader` 的职责：
- 为什么它不能独立完成完整 CSS 处理：

---

## 实验 3：恢复组合链路

### 操作
- 恢复 CSS 规则为：
  - `use: ["style-loader", "css-loader"]`
- 执行：`npm run build`

### 观察
- 构建是否成功：成功。
- 页面样式是否恢复：已恢复。
- 关键字定位（`bundle.js`）：
  - `./src/styles.css`：可定位，包含 style-loader 运行时导入和 css-loader 结果导入。
  - `injectStylesIntoStyleTag`：可定位，存在 `injectStylesIntoStyleTag(cssData, options)` 的等价调用（变量名被 webpack 改写）。

### 结论
- 为什么 `use` 从右到左执行：webpack loader 采用函数组合模型，后一个 loader 的输出作为前一个 loader 的输入，配置顺序写法与执行方向相反。
- 该链路中每个 loader 的输入与输出分别是什么：
  - `css-loader`：输入是 CSS 文本，输出是 JS 可用的 CSS 模块数据。
  - `style-loader`：输入是 CSS 模块数据，输出是运行时注入 `<style>` 的 JS 逻辑。

---

## 实验 4：`asset/resource` 与 `asset/inline` 对比

### A. `asset/resource`
- 配置：
  - `type: "asset/resource"`
- 执行：`npm run build`
- 观察：
  - `dist` 是否出现独立 `.svg` 文件：是。
  - `bundle.js` 中 `logo.svg` 对应值更像 URL 还是 data URL：URL（拼接 `publicPath` 后指向独立资源文件）。

### B. `asset/inline`
- 配置：
  - `type: "asset/inline"`
- 执行：`npm run build`
- 观察：
  - `dist` 是否仍有独立 `.svg` 文件：否，不再生成独立图片文件。
  - `bundle.js` 中是否出现 `data:image/svg+xml`（或 base64）：是，资源以内联 data URL/base64 形式存在于打包文件中。

### 对比结论
- `asset/resource` 适用场景：
  - 资源需要浏览器单独缓存、文件可能较大、希望降低主包体积时。
- `asset/inline` 适用场景：
  - 小图标等极小资源、希望减少额外请求时。
- 两者对请求数与包体积的影响：
  - `resource`：请求数增加，主包体积更小。
  - `inline`：请求数减少，主包体积更大。

---

## 今日核心概念（已整理）
- `Loader`：webpack 的源码转换器，用于把不同类型模块转成可继续打包的内容。
- `css-loader`：把 CSS 转成 JS 模块数据，不直接把样式写到页面。
- `style-loader`：在运行时把 CSS 数据写入 `<style>` 并挂载到 DOM。
- `Asset Modules`：webpack 5 的内置资源处理能力，用于替代部分 file/url/raw loader。
- `asset/resource`：输出独立文件并导出 URL。
- `asset/inline`：不输出独立文件，直接把资源内联为 data URL。
- `Runtime`：webpack 注入的模块加载与执行机制（如 `__webpack_require__`、模块缓存、publicPath 逻辑）。

---

## 今日验收清单（纯文本）
- 已完成：我能解释 `use` 为何是右到左执行。
- 已完成：我能解释 `css-loader` 与 `style-loader` 的职责边界。
- 已完成：我能通过 `bundle.js` 定位 CSS 注入相关代码。
- 已完成：我能对比 `asset/resource` 与 `asset/inline` 的完整产物差异。
- 已完成：我能给出两种资源策略的使用建议。

---

## 今日复盘（3 分钟）
- 我今天最清楚的 3 点：
  1. `css-loader` 做“转换”，`style-loader` 做“注入”，两者职责不同。
  2. `bundle.js` 中函数名会被改写，需看变量映射关系定位真实调用。
  3. `asset/resource` 会输出独立资源文件，JS 中拿到的是 URL。
- 我还不清楚的 1 点：
  - `仅保留 style-loader` 的失败路径与报错本质（准备下一步补实验）。
- 明天（Day3）我想验证：
  - 补完实验 2（仅 `style-loader`），并将 Day2 全链路闭环后进入 Week1 收尾复盘。

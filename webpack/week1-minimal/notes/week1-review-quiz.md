# Webpack Week1 复习试题

## 使用说明
- 先独立作答，再对照文末参考答案自评。
- 建议按顺序完成：选择题 -> 简答题 -> 实操题。
- 目标：把“概念记忆”升级为“能解释、能验证、能排错”。

---

## 一、选择题（每题 1 分）

1. `use: ["style-loader", "css-loader"]` 的执行顺序是：  
   A. `style-loader -> css-loader`  
   B. `css-loader -> style-loader`  
   C. 同时执行  
   D. 不确定

2. 在当前项目里，`entry` 指向的是：  
   A. `dist/index.html`  
   B. `src/styles.css`  
   C. `src/index.ts`  
   D. `webpack.config.js`

3. `asset/resource` 的典型行为是：  
   A. 不生成独立文件，内联到 JS  
   B. 生成独立文件，JS 中引用 URL  
   C. 自动压缩所有图片  
   D. 自动转成 SVG

4. `HtmlWebpackPlugin` 主要作用是：  
   A. 压缩 JS  
   B. 处理 CSS  
   C. 生成 HTML 并注入构建产物  
   D. 开启 HMR

5. 下列哪个更利于 Tree Shaking：  
   A. CommonJS 动态 `require`  
   B. ESM 静态 `import/export`  
   C. 两者完全一样  
   D. 都不支持

6. `output.clean: true` 的作用是：  
   A. 自动开启 dev server  
   B. 构建前清空输出目录  
   C. 自动生成 source map  
   D. 自动分包

---

## 二、判断题（每题 1 分）

1. `plugins` 和 `loader` 本质一样，都是处理单个模块源码。 （ ）
2. 只保留 `css-loader` 时，构建可能通过但页面样式可能不生效。 （ ）
3. `asset/inline` 会把资源转换为 data URL 内联进打包文件。 （ ）
4. `devServer.port` 只影响生产环境访问端口。 （ ）
5. `output.filename` 改名后，使用 `HtmlWebpackPlugin` 时 HTML 注入脚本会自动同步。 （ ）

---

## 三、简答题（每题 5 分）

1. 请口述 `Entry -> 依赖图 -> Loader -> Runtime -> Output` 的完整链路。  

2. 请解释 `css-loader` 与 `style-loader` 的职责边界，并说明为什么二者通常配合使用。  

3. 请对比 `asset/resource` 与 `asset/inline` 的适用场景与取舍。  

4. 请说明 `output.filename` 从 `bundle.js` 改为 `app.js` 后，为什么 `index.html` 能自动更新脚本引用。  

5. 请解释 `[name].[contenthash].js` 的含义以及它对缓存的价值。  

---

## 四、产物阅读题（每题 8 分）

1. 在 `dist/app.js` 中定位并说明：
   - 模块定义区（`__webpack_modules__`）是做什么的？
   - `__webpack_require__` 的核心职责是什么？

2. 在 `dist/app.js` 中定位 `./src/styles.css` 对应模块，回答：
   - 哪一段是 css-loader 的产物引用？
   - 哪一段是 style-loader 的运行时注入调用？

3. 在 `dist/app.js` 中定位 `./src/assets/logo.svg` 对应模块，说明它导出的是 URL 还是 data URL，并指出原因。  

---

## 五、实操题（每题 10 分）

1. 修改 `output.filename` 为 `main.js`，重新构建并记录：
   - `dist` 产物变化
   - `index.html` 注入脚本变化
   - 你的结论

2. 将图片规则从 `asset/resource` 改为 `asset/inline`，重新构建并记录：
   - 是否有独立图片文件
   - `app.js` 中资源表现形式
   - 你的结论

3. 将 `devServer.port` 改为 `9010`，启动开发服务并记录：
   - 新访问地址
   - 是否冲突
   - 排查过程与结论

---

## 参考答案（自评用）

### 一、选择题
1.B  2.C  3.B  4.C  5.B  6.B

### 二、判断题
1.错  2.对  3.对  4.错  5.对

### 三、简答题要点
1. 从入口递归建依赖图，按规则经过 loader 转换，注入 runtime（模块加载/缓存），最后按 output 输出产物并由插件完善产物。  
2. `css-loader` 负责“转换 CSS -> JS 模块数据”；`style-loader` 负责“运行时注入 `<style>`”；缺一会导致链路不完整。  
3. `resource`：独立文件、利于缓存、请求数增加；`inline`：减少请求、包体积增大，适合小资源。  
4. `HtmlWebpackPlugin` 基于当前 compilation 产物自动注入脚本，不依赖手写固定文件名。  
5. `[name]` 是 chunk 名，`[contenthash]` 基于内容生成；内容不变 hash 不变，利于长期缓存。  

### 四、产物阅读题要点
1. `__webpack_modules__` 存模块函数映射；`__webpack_require__` 负责加载、执行、缓存模块。  
2. css-loader 产物通常通过 `...css-loader...!./styles.css` 引入；style-loader 通过 `injectStylesIntoStyleTag`（或等价变量名）注入。  
3. 由规则决定：`asset/resource` 导出 URL，`asset/inline` 导出 data URL。  

### 五、实操题评分建议
- 结果是否真实可复现（40%）
- 解释是否能对应配置与产物变化（40%）
- 记录是否清晰（20%）

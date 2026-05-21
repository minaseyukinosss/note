# Week6：原理深化与源码阅读

本周没有可运行的最小工程，重点是顺着主流程读源码。

## 笔记 `notes/`
- [Webpack 源码阅读笔记](./notes/webpack-source-reading-notes.md)

## 使用方式
1. 先阅读笔记中的主流程图与主线。
2. 在任一已安装 webpack 的项目中（例如 `week1-minimal/code` 安装依赖后），对照 `node_modules/webpack/lib` 逐段跟读。
3. 用断点或日志验证你对流程的理解。

## 验收清单
- 能画出从 `compiler.run` 到 `emitAssets` 的流程。
- 能解释 `Compiler` 与 `Compilation` 的职责边界。
- 能把常用配置项映射到对应源码阶段。

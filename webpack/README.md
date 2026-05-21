# Webpack 系统学习（中级前端）

为期 6 周的 Webpack 学习路线：从最小可用配置出发，逐步深入 loader/plugin、工程化、生产优化、高级特性，最终阅读源码。

## 目录结构

每一周都遵循统一约定：

```
weekX-xxx/
├── README.md   # 本周目标 + 验收清单 + 运行说明
├── notes/      # 学习笔记、日报、复盘、Quiz
└── code/       # 可运行的最小示例工程（不含 node_modules）
```

## 学习路线

| 周次 | 主题 | 入口 |
| --- | --- | --- |
| Week 1 | 最小可用配置：ESM/CJS/CSS/资源模块/devServer | [`week1-minimal/`](./week1-minimal/README.md) |
| Week 2 | 手写 loader 与 plugin | [`week2-loader-plugin/`](./week2-loader-plugin/README.md) |
| Week 3 | 配置分层 + HMR + SourceMap + Lint + TS | [`week3-dev-workflow/`](./week3-dev-workflow/README.md) |
| Week 4 | 生产优化与量化对比报告 | [`week4-optimization/`](./week4-optimization/README.md) |
| Week 5 | 多入口 + Module Federation 微前端 | [`week5-advanced/`](./week5-advanced/README.md) |
| Week 6 | 源码主链阅读笔记 | [`week6-source/`](./week6-source/README.md) |

## 推荐学习节奏

1. 先读对应周的 `README.md`，明确目标与验收清单。
2. 进入 `code/` 安装依赖、运行脚本、观察构建产物。
3. 边读源码边在 `notes/` 中写复盘与疑问。
4. 完成本周 Quiz / Summary 后再进入下一周。

## 通用命令

```bash
cd weekX-xxx/code
npm install
npm run build   # 或 npm start / npm run dev，具体见各周 README
```

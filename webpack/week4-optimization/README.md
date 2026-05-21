# Week4：生产优化与量化对比

## 本周目标
- 使用动态导入实现异步 chunk。
- 配置 `splitChunks` 和 `runtimeChunk`。
- 使用 `contenthash` 支持长期缓存。
- 通过脚本输出"基线 vs 优化"构建时长与产物体积对比。

## 笔记 `notes/`
- [构建对比报告](./notes/build-comparison-report.md)

## 代码 `code/`
```bash
cd code
npm install
npm run compare
```

关键配置：
- `code/webpack.base.config.js`：基线构建配置。
- `code/webpack.optimized.config.js`：优化构建配置（分包、压缩、缓存）。
- `code/scripts/compare-builds.js`：自动生成构建对比数据。

## 验收清单
- `dist-base` 与 `dist-optimized` 均可正常产出。
- 优化配置可看到 vendors/runtime chunk 拆分结果。
- 报告文件包含时长与体积的量化数据。

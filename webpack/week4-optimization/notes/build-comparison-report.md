# Week4 构建对比报告

## 结果
- 基线构建时长: 2026 ms
- 优化构建时长: 2067 ms
- 基线产物体积: 83.48 KB
- 优化产物体积: 80.68 KB

## 结论
- 优化构建启用了 splitChunks / runtimeChunk / contenthash / filesystem cache。
- 在实际业务中应结合首屏请求数、缓存命中率与二次构建时长综合评估。

# Week5 中型团队构建方案设计文档

## 1. 目标与约束
- 支持多业务线并行开发（主站 + 管理台 + 活动页）。
- 保证可维护性：配置分层、约定优先、可复用公共能力。
- 保证可发布性：构建稳定、缓存可控、回滚简单。

## 2. 方案概览
- 多页面：采用多入口 MPA 方案，按页面独立出包。
- 微前端：核心业务使用 Module Federation 进行团队拆分。
- Monorepo：公共组件、工具函数、构建配置共用。
- 兼容性：`browserslist` + `core-js` + 按需 polyfill。

## 3. 目录建议（Monorepo）
```text
apps/
  main-site
  admin-console
  campaign
packages/
  ui-kit
  shared-utils
  build-config
```

## 4. 构建策略
- 开发环境：强调速度，开启 HMR、增量缓存、轻量 source map。
- 生产环境：强调稳定，开启 chunk 拆分、hash 命名、严格压缩。
- CI 环境：固定 Node 与 lockfile，构建产物做体积阈值检查。

## 5. 风险与治理
- 风险：远程模块版本漂移导致运行时不兼容。
- 治理：共享依赖固定主版本，建立发布契约与灰度流程。
- 风险：多入口页面公共模块重复打包。
- 治理：统一 `splitChunks` 策略并持续监控。

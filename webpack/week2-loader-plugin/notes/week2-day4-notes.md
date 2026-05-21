# Webpack Week2 Day4 学习笔记（异步 Hook）

## 目的
- 学会区分 `tap` / `tapAsync` / `tapPromise`
- 理解异步 Hook 为什么“必须明确结束信号”
- 用 `emit` hook 做日志验证（帮助建立生命周期阶段感知）

---

## 一、`tap` / `tapAsync` / `tapPromise`（定义）
- `tap`：同步 hook
  - 回调执行完成就返回
  - 不需要“等待完成”的信号
- `tapAsync`：异步回调 hook
  - 回调函数最后要在异步任务完成后调用 `callback()`
  - 不调用 `callback()`：webpack 不知道你异步结束了，流程可能卡住
- `tapPromise`：基于 Promise 的异步 hook
  - 回调返回 Promise，或内部返回一个 Promise
  - Promise 必须 `resolve()`（或返回已 resolve 的 Promise）
  - 不 `resolve()`：webpack 不知道你异步结束了，可能卡住

---

## 二、最常见的踩坑点（你这次已验证）
- `tapAsync`：只打印“start”但不在异步完成后 `callback()`，日志不会体现异步顺序，且流程可能异常
- `tapPromise`：写了 `new Promise(...)` 但忘了 `resolve()`，Promise 永远不完成，构建可能卡住

---

## 三、用 `emit` 做异步对照（你要观察什么）
用同一个插件同时挂：
- `compile`（开始阶段）
- `emit`（输出资源准备阶段）
- `done`（编译结束阶段，构建汇总）

你应当看到（理想顺序）：
1. compile（开始）
2. emit（对应阶段）
3. emit 的异步任务完成日志（如 `emitAsync: done` / `emitPromise: done`）
4. done（收尾汇总）

如果异步完成日志缺失，通常就是没有正确调用 `callback()` 或 `resolve()`。

---

## 四、口述标准答案（可背 15 秒）
> 异步 hook 的关键是结束信号：`tapAsync` 需要在异步完成后调用 `callback()`，`tapPromise` 需要让 Promise `resolve()`。用 `emit` 配合日志验证阶段顺序时，如果看到异步 “start” 但没有 “done”，就说明结束信号没有正确发给 webpack。

---

## 五、后续建议
- 进一步补一个“异步 hook 不调用结束信号”的对照验证（只做一次，观察是否卡住/是否超时）
- 将 `compile / emit / done` 与常用 hook 做一页速查表（Week2 收官用）


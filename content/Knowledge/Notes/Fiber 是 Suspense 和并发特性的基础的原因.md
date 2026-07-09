---
date: 2026-05-15 12:30:00
noteId: 1778930945239
updated: 2026-07-09 20:21:41
---
为什么 Fiber 是 Suspense 和并发特性的基础？

---

Suspense、`useTransition`、`useDeferredValue`、流式 SSR 和选择性 hydration 都需要 React 能区分任务优先级、暂停部分工作并恢复渲染。

这些能力依赖 Fiber 提供的工作单元拆分和调度机制。

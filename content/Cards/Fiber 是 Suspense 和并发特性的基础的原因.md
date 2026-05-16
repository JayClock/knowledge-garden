---
date: 2026-05-15 12:30:00
updated: 2026-05-16 19:29:20
share: true
noteId: 1778930945239
---
为什么 Fiber 是 Suspense 和并发特性的基础？

---

Suspense、`useTransition`、`useDeferredValue`、流式 SSR 和选择性 hydration 都需要 React 能区分任务优先级、暂停部分工作并恢复渲染。

这些能力依赖 Fiber 提供的工作单元拆分和调度机制。

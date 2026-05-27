---
date: 2026-05-15 12:00:00
updated: 2026-05-16 19:29:23
share: true
noteId: 1778930950417
---
Suspense 的挂起和恢复流程是什么？

---

组件在渲染时遇到未准备好的异步依赖，会抛出 Promise 表示需要等待。

React 捕获这个等待信号，暂停该部分渲染，显示最近 Suspense 边界的 `fallback`。Promise 完成后，React 重新尝试渲染并展示完整内容。

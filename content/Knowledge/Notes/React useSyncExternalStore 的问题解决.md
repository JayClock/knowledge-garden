---
date: 2026-05-15 12:30:00
noteId: 1778930949942
updated: 2026-07-09 20:21:41
---
React useSyncExternalStore 解决什么问题？

---

`useSyncExternalStore` 用于让 React 组件安全订阅外部状态源。

外部 store 不由 React 管理，例如浏览器 API、自定义状态库或全局订阅对象。这个 hook 提供统一协议，让 React 能读取快照并在外部状态变化时重新渲染。

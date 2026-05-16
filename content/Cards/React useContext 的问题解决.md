---
date: 2026-05-15 12:30:00
updated: 2026-05-16 19:29:23
share: true
noteId: 1778930949642
---
React useContext 解决什么问题？

---

`useContext` 解决多个深层组件共享同一份数据时的 props 透传问题。

它让上层 Provider 提供值，下层组件直接读取上下文，避免中间组件只是为了继续传递 props 而被迫接收无关数据。

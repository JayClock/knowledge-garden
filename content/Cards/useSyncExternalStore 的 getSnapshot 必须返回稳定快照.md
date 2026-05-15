---
date: 2026-05-15 12:30:00
updated: 2026-05-15 12:30:00
share: true
noteId: 1778818910338
---
useSyncExternalStore 中 getSnapshot 为什么必须返回稳定快照？

---

`getSnapshot` 返回的是当前外部状态在 React 中可比较的快照。

如果状态没有变化却每次返回新对象，React 会误以为快照变化并触发不必要渲染。稳定快照是避免重复渲染和保持一致性的关键。

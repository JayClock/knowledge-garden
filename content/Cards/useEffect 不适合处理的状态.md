---
date: 2026-05-15 12:30:00
updated: 2026-05-16 19:29:23
share: true
noteId: 1778930950768
---
useEffect 不适合处理什么状态？

---

如果某个值可以直接从 props 或 state 在渲染过程中计算出来，就不应该用 `useEffect` 再同步成另一份 state。

这样会制造重复状态、额外渲染和一致性问题。`useEffect` 应主要用于和 React 外部系统同步。

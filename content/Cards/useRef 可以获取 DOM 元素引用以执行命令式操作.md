---
date: 2026-05-15 12:30:00
updated: 2026-05-15 12:30:00
share: true
noteId: 1778818910287
---
useRef 如何用于 DOM 操作？

---

把 `ref` 传给 DOM 元素后，React 会把对应 DOM 节点放到 `ref.current`。

这适合执行聚焦、滚动、测量尺寸、调用原生 DOM API 等命令式操作。

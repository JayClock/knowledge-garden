---
date: 2026-05-15 12:30:00
updated: 2026-05-15 12:30:00
share: true
noteId: 1778818910262
---
useRef 不适合保存什么数据？

---

`useRef` 不适合保存需要展示到界面上，或变化后必须触发重新渲染的数据。

如果值的变化会影响 UI，应该优先使用 `useState` 或 [[React-useReducer|useReducer]]，而不是用 `ref` 绕过 React 的状态流。

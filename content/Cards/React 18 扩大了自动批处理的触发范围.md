---
date: 2026-05-15 12:30:00
updated: 2026-05-15 12:30:00
share: true
noteId: 1778818908038
---
React 18 的自动批处理增强了什么？

---

React 18 使用 `createRoot` 后，自动批处理不再主要局限于 React 合成事件和生命周期。

`setTimeout`、Promise、原生事件等异步回调中的多次状态更新，也可以被自动合并成一次渲染。

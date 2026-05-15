---
date: 2026-05-15 12:30:00
updated: 2026-05-15 12:30:00
share: true
noteId: 1778818910388
---
useSyncExternalStore 适合哪些场景？

---

`useSyncExternalStore` 适合把 React 外部状态源接入组件，例如自定义状态库、浏览器在线状态、媒体查询、历史记录、全局事件源等。

它不适合替代普通组件内部状态；内部状态优先使用 `useState` 或 `useReducer`。

---
date: 2026-05-15 12:30:00
updated: 2026-05-15 12:30:00
share: true
noteId: 1778818910362
---
useSyncExternalStore 中 subscribe 的职责是什么？

---

`subscribe` 的职责是注册外部状态变化监听，并在状态可能变化时通知 React。

它通常返回一个取消订阅函数。React 收到通知后会调用 `getSnapshot` 读取最新快照，而不是由 `subscribe` 直接把数据传入组件。

---
date: 2026-05-15 12:30:00
updated: 2026-05-16 19:29:23
share: true
noteId: 1778930949589
---
React useActionState 解决什么问题？

---

`useActionState` 用于以某个 action 的执行结果为中心组织状态。

表单提交常见的 pending、error、success、result 等状态，可以围绕 action 统一管理，而不是分散成多个手动维护的 state。

---
date: 2026-05-15 12:30:00
noteId: 1778930950716
updated: 2026-07-09 20:21:41
---
useActionState 返回的三个核心值是什么？

---

`useActionState` 通常返回 `[state, formAction, isPending]`。

`state` 表示当前 action 结果，`formAction` 可以交给表单或按钮触发，`isPending` 表示本次 action 是否仍在处理中。

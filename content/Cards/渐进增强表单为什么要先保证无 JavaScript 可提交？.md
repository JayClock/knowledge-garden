---
date: 2026-05-15 12:00:00
updated: 2026-05-16 19:29:19
share: true
noteId: 1778930943342
---
渐进增强表单为什么要先保证无 JavaScript 可提交？

---

表单的核心能力是收集输入并提交给服务端。

渐进增强表单要先用原生 HTML 的 `action`、`method`、`label`、`input` 和提交按钮保证无 JavaScript 时可用，再用 JavaScript 添加校验、自动完成、即时反馈等增强体验。

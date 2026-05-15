---
date: 2026-05-15 12:00:00
updated: 2026-05-15 12:22:01
share: true
noteId: 1778818908540
---
React Server Components 如何改变组件边界？

---

React Server Components 把组件边界从客户端扩展到服务端。

传统 Client Component 需要把组件代码发送到浏览器执行；Server Component 可以在服务端读取数据、生成组件树描述，再把结果交给客户端消费。组件不再必然等同于客户端 JavaScript。

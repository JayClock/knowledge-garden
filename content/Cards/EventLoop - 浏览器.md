---
date: 2024-10-19T11:00:11
updated: 2025-05-19T18:13:00
share: true
tags:
  - review
---
![浏览器 EventLoop](https://knowledge-garden.oss-cn-shanghai.aliyuncs.com/images/%E6%B5%8F%E8%A7%88%E5%99%A8%20EventLoop.png)

Event Loop（事件循环）是 JavaScript 处理 **异步操作** 的核心机制。它允许 JavaScript 以 **非阻塞** 的方式执行代码，即使遇到 I/O 操作（如网络请求、定时器），也不会影响主线程继续执行其他任务。
1. **执行同步任务**
	- 所有同步任务在[[./JS 调用栈|调用栈]]（Call Stack） 中依次执行，直到调用栈清空。
	- 如果遇到微任务，则将它添加到微任务队列中，继续执行下一个同步代码。
	- 如果遇到宏任务，则将它添加到宏任务队列中，继续执行下一个同步代码。
2. **处理[[./JS 宏任务和微任务|微任务]]**
	- 检查 微任务队列（MicroTask Queue） 是否有任务（如 Promise.then()、queueMicrotask()）。
	- 依次执行所有微任务，直到微任务队列清空。
3. **尝试触发 [[./JS Web-API-DOM|DOM]] 渲染**
	- DOM 结构如果有改变则重新渲染
4. **执行[[./JS 宏任务和微任务|宏任务]]**
	- 从 宏任务队列（MacroTask Queue） 取出 一个 任务（如 setTimeout 回调、I/O 任务），放入调用栈执行。
5. **重复步骤 2（处理新的微任务）**
	-  宏任务执行完毕后，再次检查微任务队列，如果有新产生的微任务，立即执行所有微任务。
6. **重复步骤 4（执行下一个宏任务）**
	-  继续取出下一个 宏任务，重复整个过程，形成循环（Event Loop）
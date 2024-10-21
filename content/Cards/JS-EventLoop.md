---
date: 2024-10-19T11:00:11
updated: 2024-10-19T22:26:57
share: true
---
event loop 就是[[./JS-异步|异步]]回调的实现机制，可画图实现。

- 同步代码，一行一行访在 Call Stack 执行
- 遇到异步，会先“记录”下，等待时机（定时，网络请求结束）
- 时机到了，就移动到 Callback Queue
- 如果 Call Stack 为空（即同步代码执行完）
- 执行当前的微任务
- 尝试触发 [[./JS-Web-API-DOM|DOM]] 渲染，DOM 结构如果有改变则重新渲染
- Event Loop 开始工作
- 轮询查找 Callback Queue，如有则移动到 Call Stack 执行
- 继续轮询查找
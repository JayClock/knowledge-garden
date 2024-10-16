---
date: 2024-10-12T17:59:45
updated: 2024-10-16T07:15:14
share: true
---
# 单线程与异步
- JS 是单线程语言，只能同时做一件事
- 浏览器和 nodejs 已支持 JS 启动进程，如 Web Worker
- JS 和 DOM 共用一个线程，因为 JS 可修改 DOM 结构
- 由于请求网站时，不能因（网络请求，定时任务）卡住
- 因此需要异步
# 同步与异步
- 基于 JS 是单线程语言
- 异步不会阻塞代码执行
- 同步会阻塞代码执行

```js
// 异步 （callback 回调函数）
console.log(100)
setTimeout(() => {
    console.log(200)
}, 1000)
console.log(300)
console.log(400)
```

```js
// 同步
console.log(100)
alert(200)
console.log(300)
```
# 应用场景
1. 网络请求，如 ajax 图片加载
2. 定时任务，如 setTimeout


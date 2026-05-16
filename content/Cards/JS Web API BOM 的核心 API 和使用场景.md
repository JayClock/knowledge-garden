---
date: 2024-10-12T18:01:23
updated: 2026-05-16 19:29:22
share: true
noteId: 1778930948416
---
JS Web API BOM 的核心 API 和使用场景是什么？

---

浏览器对象模型，提供了独立于内容和浏览器窗口进行交互的对象

```js
// navigator
const ua = navigator.userAgent
const isChorme = ua.indexOf('Chrome')
console.log(isChrome)
```

```js
// screen
console.log(screen.width)
console.log(screen.height)
```

```js
// location
console.log(location.href)
console.log(location.protocol) // 协议
console.log(location.host)
console.log(location.search) // 传递的参数
console.log(location.hash)
console.log(location.pathname)
```


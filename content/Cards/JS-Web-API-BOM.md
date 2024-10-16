---
date: 2024-10-12T18:01:23
updated: 2024-10-16T09:32:21
share: true
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


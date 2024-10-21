---
date: 2024-10-19T18:40:14
updated: 2024-10-19T22:26:03
share: true
---
# 宏任务和微任务
- 宏任务：setTimeout，setInterval，Ajax，[[./JS-Web-API-DOM|DOM]] 事件
- 微任务：[[./JS-Promise|Promise]] [[./JS-async&await|async&await]]
# 为什么微任务比宏任务执行要早
- 微任务：ES 语法标准之内，JS 引擎来统一处理。即，不用浏览器有任何干预，即可一次性处理完，更快更及时。在 DOM 渲染之前触发。
- 宏任务：ES 语法没有，JS 引擎不处理，浏览器（或 nodejs）干预处理。在 DOM 渲染之后触发。

```js
// 修改 DOM
const $p1 = $('<p>一段文字</p>')
const $p2 = $('<p>一段文字</p>')
const $p3 = $('<p>一段文字</p>')
$('#container')
    .append($p1)
    .append($p2)
    .append($p3)

// 微任务：渲染之前执行（DOM 结构已更新）
Promise.resolve().then(() => {
    const length = $('#container').children().length
    alert(`micro task ${length}`)
})

// 宏任务：渲染之后执行（DOM 结构已更新）
setTimeout(() => {
    const length = $('#container').children().length
    alert(`macro task ${length}`)
})
```

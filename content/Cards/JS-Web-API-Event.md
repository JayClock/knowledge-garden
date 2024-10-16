---
date: 2024-10-12T18:03:05
updated: 2024-10-16T09:45:10
share: true
---
# 事件模型

- 事件捕获阶段：事件 document 一直向下传播到目标元素，一次检查经过的节点是否绑定了事件监听函数，如果有则执行
- 事件处理阶段：事件到达目标元素，触发目标元素的监听函数
- 事件冒泡阶段：事件从目标元素冒泡到 document，依次检查经过的节点是否绑定了事件监听函数，如果有则执行
## 事件绑定

```js
// 通用的事件绑定函数
// function bindEvent(elem, type, fn) {
//     elem.addEventListener(type, fn)
// }
function bindEvent(elem, type, selector, fn) {
    if (fn == null) {
        fn = selector
        selector = null
    }
    elem.addEventListener(type, event => {
        const { target } = event
        if (selector) {
            // 代理绑定
            if (target.matches(selector)) {
                fn.call(target, event)
            }
        } else {
            // 普通绑定
            fn.call(target, event)
        }
    })
}

// 普通绑定
const btn1 = document.getElementById('btn1')
bindEvent(btn1, 'click', function (event) {
    // console.log(event.target) // 获取触发的元素
    event.preventDefault() // 阻止默认行为
    alert(this.innerHTML)
})
```
## 事件冒泡

```html
<div id="div1">
    <p id="p1">激活</p>
    <p id="p2">取消</p>
    <p id="p3">取消</p>
    <p id="p4">取消</p>
</div>
<div id="div2">
    <p id="p5">取消</p>
    <p id="p6">取消</p>
</div>
```

```js
const p1 = document.getElementById('p1')
bindEvent(p1, 'click', event => {
    event.stopPropagation() // 阻止冒泡
    console.log('激活')
})
const body = document.body
bindEvent(body, 'click', event => {
    console.log('取消')
    // console.log(event.target)
})
const div2 = document.getElementById('div2')
bindEvent(div2, 'click', event => {
    console.log('div2 clicked')
    console.log(event.target)
})
```
## 事件代理

- 代码更简洁
- 减少浏览器内存使用
- 不要滥用

```html
<div id="div3">
    <a href="#">a1</a><br>
    <a href="#">a2</a><br>
    <a href="#">a3</a><br>
    <a href="#">a4</a><br>
    <button>加载更多...</button>
</div>
```

```js
// 代理绑定
const div3 = document.getElementById('div3')
bindEvent(div3, 'click', 'a', function (event) {
    event.preventDefault()
    alert(this.innerHTML)
})
```

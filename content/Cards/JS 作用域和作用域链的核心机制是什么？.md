---
date: 2025-05-13T20:09:03
updated: 2026-05-16 19:29:22
share: true
noteId: 1778930948217
---
JS 作用域和作用域链的核心机制是什么？

---

- **作用域**：变量的可访问范围，分为 **全局作用域、函数作用域、块级作用域**。
- **作用域链**：变量查找机制，从当前作用域 **逐级向上查找**，直到全局作用域或 `ReferenceError`。
- **ES6 关键点**：
 - let / const **具有块级作用域**，避免 `var` 变量提升带来的问题。
 - 使用 let 声明的变量不会挂在全局对象 window 上
 - **[[./JS 闭包的核心机制是什么？|闭包]]** 利用作用域链，保留外部作用域的变量。

```js  
var a = 'global'  
  
function outer() {  
  var b = 'outer'  
  function inner() {    var c = 'inner'    console.log(a, b, c) // ✅ global outer inner  }  
  inner()}  
  
outer()  
console.log(b) // ❌ ReferenceError: b is not defined  
```

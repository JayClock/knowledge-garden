---
date: 2024-10-25T16:32:14
updated: 2026-05-16 19:29:22
share: true
noteId: 1778930947938
---
JS 类型判断的核心机制是什么？

---

通过 typeof 运算符判断

```js
// 判断所有值类型
let a                 typeof a // 'undefined'
const str = 'abc'     typeof str // 'string'
const n = 100         typeof n // 'number'
const b = true        typeof b // 'boolean'
const s = Symbol('s') typeof s // 'symbol'
```

```js
// 能判断函数
typeof console.log     // 'function'
typeof function () {}  // 'function'
```

```js
// 能识别引用类型（不能继续识别）
typeof null       // 'object'
typeof ['a','b']  // 'object'
typeof { x:100 }  // 'object'
```


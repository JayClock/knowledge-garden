---
date: 2024-10-25T16:34:39
updated: 2026-05-15 10:03:24
share: true
noteId: 1778807091293
---
JS 中 == 和 === 有什么区别？

---

- 两个都为简单类型，字符串和布尔值都会转换成数值，再比较
- 简单类型与引用类型比较，对象转化成其原始类型的值，再比较
- 两个都为引用类型，则比较它们是否指向同一个对象
- null 和 undefined 相等
- 存在 NaN 则返回 false

```js
// == 和 ===
100 == ‘100’      // true
0 == ''           // true
0 == false        // true
false == ''       // true
null == undefined // true
NaN == NaN        // false // 有NaN就是false
// 除了 == null 之外，其他都一律用 === ，例如
const obj = { x:100 }
if(obj.a == null) {}
// 相当于
if(obj.a === null || obj.a === undefined) {}
```

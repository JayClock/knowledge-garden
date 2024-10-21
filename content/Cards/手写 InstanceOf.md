---
date: 2024-10-21T11:44:18
updated: 2024-10-21T11:46:37
share: true
---
instanceOf 的本质是在[[./JS-原型与原型链|原型链]]上查找

```ts
function instanceOf(left, right) {
  let proto = left.__proto__
  while (true) {
    if (proto == null) return false
    if (proto === right.prototype) {
      return true
    }
    proto = proto.__proto__
  }
}
```
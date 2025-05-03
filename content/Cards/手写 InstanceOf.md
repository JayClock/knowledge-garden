---
date: 2024-10-21T11:44:18
updated: 2025-05-02T16:32:50
share: true
tags:
  - review
---
instanceOf 的本质是在[[./JS 原型与原型链|原型链]]上查找

```ts
function myInstanceOf(obj, constructor) {
  let proto = Object.getPrototypeOf(obj); // 获取 obj 的原型
  while (proto) {
    if (proto === constructor.prototype) {
      return true;
    }
    proto = Object.getPrototypeOf(proto); // 获取原型链上的下一个原型
  }
  return false;
}
```
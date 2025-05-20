---
date: 2024-10-21T11:44:18
updated: 2025-05-19T17:07:06
share: true
tags:
  - review
---
 instanceof 运算符用于检测构造函数的 prototype 属性是否出现在某个实例对象的[[./JS 原型与原型链|原型链]]上
 
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
---
date: 2024-10-21T13:25:41
updated: 2026-05-15 09:58:44
share: true
noteId: 1778807088724
---
如何实现 new？

---

# new 一个对象的过程
- 创建一个新的对象 obj
- 将对象与构造函数通过原型链连接起来
- 将构造函数中的 this 绑定到新建的对象上 obj 上
- 根据构造函数的返回类型作判断，如果是原始值则被忽略，如果是返回对象，需要正常处理

```ts
function myNew(constructor, ...args) {
  // 创建一个空对象，该对象的原型为构造函数的原型对象
  var obj = Object.create(constructor.prototype);
  // 将构造函数的 this 绑定到该空对象上，执行构造函数的代码
  var result = constructor.apply(obj, args);
  // 如果构造函数有显式返回一个对象，则返回该对象，否则返回空对象
  return (typeof result === 'object' && result !== null) ? result : obj;
}
```
# Object.create 和 {} 的区别
- `{}` 等同于 new Object()，原型为 `Object.prototype`
- Object.create(null) 没有原型
- Object.create({...}} 可指定原型

```js
const obj1 = {
  a: 10,
  b: 20,
  sum() {
    return this.a + this.b
  },
}

const obj2 = new Object({
  a: 10,
  b: 20,
  sum() {
    return this.a + this.b
  },
})

const obj21 = new Object(obj1) // obj1 === obj2

const obj3 = Object.create(null)
const obj4 = new Object() // {}

const obj5 = Object.create({
  a: 10,
  b: 20,
  sum() {
    return this.a + this.b
  },
})

const obj6 = Object.create(obj1)
```


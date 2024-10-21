---
date: 2024-10-21T13:25:41
updated: 2024-10-21T13:32:38
share: true
---
# new 一个对象的过程
- 创建一个新的对象 obj
- 将对象与构造函数通过原型链连接起来
- 将构造函数中的 this 绑定到新建的对象上 obj 上
- 根据构造函数的返回类型作判断，如果是原始值则被忽略，如果是返回对象，需要正常处理

```ts
function newFn(fn, ...args) {
	// 创建一个新对象
  const obj = {}
  // 新对象的原型指向构造函数原型对象
  obj.__proto__ = fn.prototype
  // 将构造函数的this指向新对象
  let res = fn.apply(obj, args)
  // 根据返回值判断
  return res instanceof Object ? res : obj
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


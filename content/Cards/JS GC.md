---
date: 2024-10-16T13:20:49
updated: 2024-10-16T13:30:56
share: true
---
# 垃圾回收

正常情况下，一个函数执行完，其中的变量都会被 JS 垃圾回收。比如

```js
function fn() {
  const a = "aaa";
  console.log(a);

  const obj = {
    x: 100,
  };
  console.log(obj);
}
fn();
```

但是在某些情况下，变量是销毁不了的，因为可能会被再次使用。比如

```js
function fn() {
  const obj = {
    x: 100,
  };
  window.obj = obj; // 引用到了全局变量，obj 销毁不了
}
fn();
```

```js
function genDataFns() {
  const data = {}; // 闭包，data 销毁不了
  return {
    get(key) {
      return data[key];
    },
    set(key, val) {
      data[key] = val;
    },
  };
}
const { get, set } = genDataFns();
```
# 垃圾回收算法 - 引用计数

早期的垃圾回收算法，以**数据是否被引用**来判断要不要回收

```js
// 对象被 a 引用
let a = {
  b: {
    x: 10,
  },
};

let a1 = a; // 又被 a1 引用
let a = 0; // 不再被 a 引用，但仍然被 a1 引用
let a1 = null; // 不再被 a1 引用

// 对象最终没有任何引用，会被回收
```

但是这个算法有一个缺陷，比如循环引用的变量无法回收

```js
function fn() {
  const obj1 = {};
  const obj2 = {};
  obj1.a = obj2;
  obj2.a = obj1; // 循环引用，无法回收 obj1 和 obj2
}
fn();
```
# 垃圾回收算法 - 标记清除

现代浏览器使用**标记清除**算法。根据**是否可获得**来判断是否回收。

定期从根（即全局变量）开始向下查找，能找到的即保留，找不到的回收。循环引用不再是问题。
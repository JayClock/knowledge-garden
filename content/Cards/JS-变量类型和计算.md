---
date: 2024-10-12T17:21:21
updated: 2024-10-21T11:40:38
share: true
---
# 值类型与引用类型
- 声明变量是内存地址不同
	1. 值类型的值放在栈中
	2. 引用类型的值放在堆中，在栈中存放指向堆内存的地址
- 不同的类型数据导致赋值变量时的不同：
	1. 简单类型的值，是生成相同的值，两个对象对应不同的地址
	2. 复杂类型赋值，是将保存对象的内存地址赋值给另一个变量。也就是两个变量指向堆内存中同一个对象

```js
// 常见值类型
const a // undefined
const s = 'abc'
const n = 100
const b = true
const s = Symbol('s')
// 常见引用类型
const obj = {x:100}
const arr = ['a','b','c']
const n = null // 特殊的引用类型，指针指向空地址
// 特殊引用类型，但不用于存储数据，所以没有“拷贝、复制”函数的说法
function fn() {}
```
# 类型判断
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
# 变量类型 - 类型转换

```js
// 字符串拼接
const a = 100 + 10    // 110
const b = 100 + '10'  // '10010'
const c = true + '10' // 'true10'
```
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
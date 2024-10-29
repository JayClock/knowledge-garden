---
date: 2024-10-12T17:58:33
updated: 2024-10-15T22:41:02
share: true
---
# 作用域
## 全局作用域

任何不在函数中活着是大括号中声明的变量，都是在全局作用域下，全局作用域下声明的变量可以在程序的任意位置访问

```ts
// 全局变量
var greeting = 'Hello World!'
function greet() {
  console.log(greeting)
}
// 打印 'Hello World!'
greet()
```
## 函数作用域

函数作用域也叫局部作用域，如果一个变量是在函数内部声明的，它就在一个函数作用域下。这些变量只能函数内部访问，不能在函数以外去访问。

```ts
function greet() {
  var greeting = 'Hello World!'
  console.log(greeting)
}
// 打印 'Hello World!'
greet()
// 报错： Uncaught ReferenceError: greeting is not defined
console.log(greeting)
```
## 块级作用域

ES6 引入了 `let` 和 `const` 关键字，和 `var` 关键字不同，在大括号中由 `let` 和 `const` 声明的变量存在于块级作用域中。在大括号之外不能访问这些变量。

```ts
{
  // 块级作用域中的变量
  let greeting = 'Hello World!'
  var lang = 'English'
  console.log(greeting) // Prints 'Hello World!'
}
// 变量 'English'
console.log(lang)
// 报错：Uncaught ReferenceError: greeting is not defined
console.log(greeting)
```
## 作用域链

1. 一个变量在当前作用域没有定义，但被使用了
2. 向上级作用域，一层一层的寻找，直到被找到为止
3. 如果到全局作用域都没被找到，则报错 xx is not defined

```ts
var sex = '男';
function person() {
    var name = '张三';
    function student() {
        var age = 18;
        console.log(name); // 张三
        console.log(sex); // 男 
    }
    student();
    console.log(age); // Uncaught ReferenceError: age is not defined
}
person();
```
# 闭包

> 一个函数和对其周围状态（lexical environment，词法环境）的引用捆绑在一起（或者说函数被引用包围），这样的组合就是闭包（closure）

闭包可以让你在一个内层函数中访问到外层函数的作用域

任何闭包的使用场景都离不开以下两点
1. 创建私有变量
2. 延长变量的生命周期

作用域应用的特殊情况，有两种表现
1. 函数作为参数被传递
2. 函数作为返回值被返回

**自由变量的查找，是在函数定义的地方，向上级作用域查找，不是在执行的地方**

```ts
// 函数作为返回值
const create = () => {
  let a = 100
  return () => {
    console.log(a)
  }
}

let fn = create()
let a = 200
fn()  // 100
```


```ts
// 函数作为参数
const print = (fn) => {
  let a = 200
  fn()
}

let a = 100
const fn = () => {
  console.log(a)
}
print(fn) // 100
```
# this 对象
## 重点
- this 的值是在函数执行的时候决定的，不是在定义的时候
- this 在函数执行的过程中，this 一旦被确定了，就不可以再更改
## 绑定场景

```ts
// 1.作为普通函数
const fn1 = () => {
  console.log(this)
}
fn1() // window

// 2.使用 call apply bind
fn1.call({ x: 100 }) // { x: 100 }
const fn2 = fn1.bind({ x: 200 })
fn2() // { x: 200 }

// 3.作为对象方法被调用
const zhangsan = {
  name: "张三",
  sayHi() {
    // this 即当前对象
    console.log(this)
  },
  wait() {
    // setTimeout(function () {
    //   // this === window
    //   console.log(this)
    // })
    // 4.箭头函数
    setTimeout(() => {
      // this 即当前对象
      console.log(this)
    })
  },
}

// 5.在 class 方法被调用
class People {
  constructor(name) {
    this.name = name
  }
  sayHi() {
    console.log(this)
  }
}
```

# apply、call、bind 区别
## apply
### 使用
- 接收两个参数，第一个参数是 this 的指向，第二个参数是函数接收的参数，以数组的形式传入
- 改变 this 指向后原函数会立即执行，且此方法只是临时改变 this 指向一次
- 当第一个参数为 null、undefined 的时候，默认指向 window (在浏览器中)

```js
function fn(...args) {
  console.log(this, args)
}
let obj = {
  myname: '张三',
}

fn.apply(obj, [1, 2]) // this会变成传入的obj，传入的参数必须是一个数组；
fn(1, 2) // this指向window
fn.apply(null, [1, 2]) // this指向window
fn.apply(undefined, [1, 2]) // this指向window
```
## call
### 使用
- 接收两个参数，第一个参数是 this 的指向，第二个参数是函数接收的参数，以参数列表的形式传入
- 改变 this 指向后原函数会立即执行，且此方法只是临时改变 this 指向一次
- 当第一个参数为 null、undefined 的时候，默认指向 window (在浏览器中)

```js
function fn(...args) {
  console.log(this, args)
}
let obj = {
  myname: '张三',
}

fn.call(obj, 1, 2) // this会变成传入的obj，传入的参数是一个参数列表；
fn(1, 2) // this指向window
fn.call(null, 1, 2) // this指向window
fn.call(undefined, 1, 2) // this指向window
```
## bind
### 使用
- 接收两个参数，第一个参数是 this 的指向，第二个参数是函数接收的参数，以参数列表的形式传入（可以分多次传入）
- 改变 this 指向后原函数不会立即执行，返回一个永久改变 this 指向的函数

```js
function fn(...args) {
  console.log(this, args)
}
let obj = {
  myname: '张三',
}

const bindFn = fn.bind(obj) // this 也会变成传入的obj ，bind不是立即执行需要执行一次
bindFn(1, 2) // this指向obj
fn(1, 2) // this指向window
```


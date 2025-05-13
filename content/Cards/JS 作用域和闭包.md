---
date: 2024-10-12T17:58:33
updated: 2025-05-13T19:21:29
share: true
tags:
  - review
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
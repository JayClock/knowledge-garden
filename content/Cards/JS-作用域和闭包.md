---
date: 2024-10-12T17:58:33
updated: 2024-10-15T14:48:32
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
# 作用域链

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


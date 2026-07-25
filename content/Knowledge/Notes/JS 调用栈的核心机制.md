---
date: 2025-05-13T16:59:16
noteId: 1778930947818
updated: 2026-07-25 09:00:51
---
JS 调用栈的核心机制是什么？

---

JavaScript 中有很多函数，经常会出现在一个函数中调用另外一个函数的情况，调用[[栈的定义、操作特性和典型应用|栈]]就是用来管理函数调用关系的一种数据结构。

- 每调用一个函数，JavaScript 引擎会为其创建执行上下文，并把该执行上下文压入调用栈，然后 JavaScript 引擎开始执行函数代码。
- 如果在一个函数 A 中调用了另外一个函数 B，那么 JavaScript 引擎会为 B 函数创建执行上下文，并将 B 函数的执行上下文压入栈顶。
- 当前函数执行完毕后，JavaScript 引擎会将该函数的执行上下文弹出栈。
- 当分配的调用栈空间被占满时，会引发“堆栈溢出”问题。
- 调用从栈中顶出，但是有变量依旧能访问，即为[[JS 闭包的核心机制|闭包]]

比如下面的代码调用栈如图所示

```js
var a = 2
function add(b,c){
  return b+c
}
function addAll(b,c){
  var d = 10
  result = add(b,c)
  return  a+result+d
}
addAll(3,6)
```

![JavaScript 函数执行上下文与调用栈](https://knowledge-garden.oss-cn-shanghai.aliyuncs.com/images/JavaScript%20%E5%87%BD%E6%95%B0%E6%89%A7%E8%A1%8C%E4%B8%8A%E4%B8%8B%E6%96%87%E4%B8%8E%E8%B0%83%E7%94%A8%E6%A0%88.png)

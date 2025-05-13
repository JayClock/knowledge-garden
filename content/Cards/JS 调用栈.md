---
date: 2025-05-13T16:59:16
updated: 2025-05-13T19:21:01
share: true
---
JavaScript 中有很多函数，经常会出现在一个函数中调用另外一个函数的情况，调用[[./数据结构：栈|栈]]就是用来管理函数调用关系的一种数据结构。

- 每调用一个函数，JavaScript 引擎会为其创建执行上下文，并把该执行上下文压入调用栈，然后 JavaScript 引擎开始执行函数代码。
- 如果在一个函数 A 中调用了另外一个函数 B，那么 JavaScript 引擎会为 B 函数创建执行上下文，并将 B 函数的执行上下文压入栈顶。
- 当前函数执行完毕后，JavaScript 引擎会将该函数的执行上下文弹出栈。
- 当分配的调用栈空间被占满时，会引发“堆栈溢出”问题。
- 调用栈的特殊场景：[[./JS 作用域和闭包|闭包]]

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

![[../images/Pasted image 20250513181636.png|Pasted image 20250513181636.png]]
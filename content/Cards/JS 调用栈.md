---
date: 2025-05-13T16:59:16
updated: 2025-05-13T18:16:37
share: true
---
你应该知道 JavaScript 中有很多函数，经常会出现在一个函数中调用另外一个函数的情况，调用[[./数据结构：栈|栈]]就是用来管理函数调用关系的一种数据结构。

下面的代码调用栈如图所示

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
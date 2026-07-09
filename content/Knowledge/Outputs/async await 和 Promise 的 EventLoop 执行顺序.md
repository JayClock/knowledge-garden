---
date: 2026-06-10 21:27:00
updated: 2026-07-09 20:21:41
---
# async await 和 Promise 的 EventLoop 执行顺序

## 问题

下面这段代码的执行顺序是什么？

```js
async function async1() {
  console.log('async1')
  await async2()
  console.log('async1 end')
}
async function async2() {
  console.log('async2')
}
console.log('script start')
setTimeout(() => {
  console.log('setTimeOut')
}, 0)
async1()
new Promise((resolve) => {
  console.log('promise')
  resolve()
}).then(() => {
  console.log('promise2')
})
console.log('script end')
```

## 结论

最终输出顺序是：

```text
script start
async1
async2
promise
script end
async1 end
promise2
setTimeOut
```

## 执行过程

从 EventLoop - 浏览器的执行顺序和关键机制 的角度看，这段代码遵循三个关键阶段：

1. 先执行主线程上的同步任务，直到 调用栈 清空。
2. 同步任务执行结束后，清空所有 微任务。
3. 微任务清空后，再从宏任务队列中取出一个宏任务执行。

### 1. 同步代码先执行

主脚本本身是一个宏任务。进入这个宏任务后，JavaScript 会从上到下执行同步代码。

首先执行：

```js
console.log('script start')
```

所以输出：

```text
script start
```

然后遇到：

```js
setTimeout(() => {
  console.log('setTimeOut')
}, 0)
```

`setTimeout` 的回调不会立即执行，而是被放入宏任务队列中。即使延迟时间是 `0`，它也要等当前宏任务执行完、微任务队列清空之后，才有机会被事件循环取出执行。

接着调用：

```js
async1()
```

进入 `async1` 后，先执行同步部分：

```js
console.log('async1')
```

输出：

```text
async1
```

然后执行：

```js
await async2()
```

`await` 会先求值右侧表达式，所以会先调用 `async2()`。进入 `async2` 后执行：

```js
console.log('async2')
```

输出：

```text
async2
```

`async2()` 是一个 `async function`，它会返回一个 Promise。`await` 会暂停 `async1` 后续代码的执行，因此下面这一句不会立刻输出：

```js
console.log('async1 end')
```

它会作为 `await` 后续逻辑进入微任务队列。

继续执行主脚本，来到：

```js
new Promise((resolve) => {
  console.log('promise')
  resolve()
}).then(() => {
  console.log('promise2')
})
```

这里要注意：`Promise` 构造函数中的执行器函数是同步执行的，所以会立即输出：

```text
promise
```

`resolve()` 执行后，`.then()` 回调会被放入微任务队列，因此：

```js
console.log('promise2')
```

此时还不会执行。

最后执行：

```js
console.log('script end')
```

输出：

```text
script end
```

到这里，第一轮宏任务里的同步代码执行完毕。

### 2. 同步代码结束后，清空微任务队列

当前微任务队列中有两个任务：

1. `await async2()` 后面的继续执行逻辑：

```js
console.log('async1 end')
```

2. `Promise.then()` 回调：

```js
console.log('promise2')
```

因为 `async1()` 先于后面的 `new Promise(...).then(...)` 执行，所以 `await` 后续逻辑更早进入微任务队列。于是先输出：

```text
async1 end
```

再输出：

```text
promise2
```

### 3. 微任务清空后，执行宏任务

微任务队列清空之后，事件循环才会从宏任务队列中取出下一个宏任务。

前面注册的 `setTimeout` 回调此时被取出执行：

```js
console.log('setTimeOut')
```

所以最后输出：

```text
setTimeOut
```

## 面试表达

可以这样总结：

> 这段代码的主线是：同步代码先执行，`await` 后面的代码和 `Promise.then` 都进入微任务队列，`setTimeout` 进入宏任务队列。  
> 所以先输出主线程同步内容：`script start`、`async1`、`async2`、`promise`、`script end`。  
> 然后清空微任务队列，输出 `async1 end` 和 `promise2`。  
> 最后才执行宏任务队列里的 `setTimeout`，输出 `setTimeOut`。

更短的回答是：

> `await` 不是让函数完全变成异步，它只会暂停 `await` 后面的代码；`await` 右侧表达式仍然会立即执行。`Promise` 构造函数也是同步执行的，只有 `.then` 回调才是微任务。`setTimeout` 是宏任务，所以一定排在本轮微任务之后执行。

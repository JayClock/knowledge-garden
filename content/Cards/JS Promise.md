---
date: 2024-10-19T14:19:16
updated: 2025-05-13T19:58:48
share: true
tags:
  - review
---
**1. 什么是 Promise？**

> **Promise 是 JavaScript 处理异步操作的一种方式**，用于解决回调地狱（Callback Hell）问题。
> 它表示一个未来才会完成（或失败）的异步操作，并提供 `.then()`、`.catch()`、`.finally()` 方法进行处理。

**2. Promise 的基本用法**

**创建一个 Promise**

```js
const myPromise = new Promise((resolve, reject) => {
  setTimeout(() => {
    let success = true
    success ? resolve('操作成功') : reject('操作失败')
  }, 1000)
})
```

**使用 `then`、`catch` 处理结果**

```js
myPromise
  .then((result) => console.log('成功:', result)) // 处理成功
  .catch((error) => console.log('失败:', error)) // 处理失败
  .finally(() => console.log('操作结束')) // 无论成功或失败都会执行
```

**3. Promise 串行执行**

**多个异步操作依次执行（避免回调地狱）**

```js
function step1() {
  return new Promise((resolve) => setTimeout(() => resolve('Step 1 完成'), 1000))
}
function step2() {
  return new Promise((resolve) => setTimeout(() => resolve('Step 2 完成'), 1000))
}

step1()
  .then((result) => {
    console.log(result)
    return step2() // 返回 Promise
  })
  .then((result) => console.log(result))
  .catch((error) => console.error('错误:', error))
```

**4. Promise 并行执行**

**多个异步任务同时执行，全部完成后再处理**

```js
const p1 = new Promise((resolve) => setTimeout(() => resolve('任务 1'), 1000))
const p2 = new Promise((resolve) => setTimeout(() => resolve('任务 2'), 1500))

Promise.all([p1, p2])
  .then((results) => console.log('所有任务完成:', results))
  .catch((error) => console.error('任务失败:', error))
```

**如果只要最快完成的结果**

```js
Promise.race([p1, p2])
  .then((result) => console.log('最先完成的:', result))
  .catch((error) => console.error('失败:', error))
```

**5. 面试回答总结**

> **Promise 解决异步回调问题，提供 `.then()`、`.catch()`、`.finally()` 处理状态变化。支持 `Promise.all()` 并行执行，`Promise.race()` 竞争执行。用 `async/await` 可以让异步代码更清晰。**

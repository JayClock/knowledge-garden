---
date: 2024-10-19T14:19:16
updated: 2024-12-31T18:21:43
share: true
tags:
  - review
sr-due: 2025-01-04
sr-interval: 4
sr-ease: 270
---

- 三种状态
	- pending resolved rejected
	- pending -> reolved 或 pending -> rejected
	- 变化不可逆
		```js
		// 刚定义时，状态默认为 pending
		const p1 = new Promise((resolve, reject) => {})
		
		// 执行 resolve() 后，状态变成 resolved
		const p2 = new Promise((resolve, reject) => {
		    setTimeout(() => {
		        resolve()
		    })
		})
		
		// 执行 reject() 后，状态变成 rejected
		const p3 = new Promise((resolve, reject) => {
		    setTimeout(() => {
		        reject()
		    })
		})
		```
- 状态表现
	- pending 状态，不会触发 then 和 catch
	- resolved 状态，会触发后续的 then 回调函数
	- rejected 状态，会触发后续的 catch 回调函数
# then 和 catch 改变状态
- then 正常返回 resolved，里面有报错则返回 rejected
- catch 正常返回 resolved，里面有报错则返回 rejected

```js
// then() 一般正常返回 resolved 状态的 promise
Promise.resolve().then(() => {
    return 100
})

// then() 里抛出错误，会返回 rejected 状态的 promise
Promise.resolve().then(() => {
    throw new Error('err')
})

// catch() 不抛出错误，会返回 resolved 状态的 promise
Promise.reject().catch(() => {
    console.error('catch some error')
})

// catch() 抛出错误，会返回 rejected 状态的 promise
Promise.reject().catch(() => {
    console.error('catch some error')
    throw new Error('err')
})
```


```js
// 第一题
Promise.resolve().then(() => {
    console.log(1)
}).catch(() => {
    console.log(2)
}).then(() => {
    console.log(3)
})

// 1, 3

// 第二题
Promise.resolve().then(() => { // 返回 rejected 状态的 promise
    console.log(1)
    throw new Error('erro1')
}).catch(() => { // 返回 resolved 状态的 promise
    console.log(2)
}).then(() => {
    console.log(3)
})
// 1, 2, 3

// 第三题
Promise.resolve().then(() => { // 返回 rejected 状态的 promise
    console.log(1)
    throw new Error('erro1')
}).catch(() => { // 返回 resolved 状态的 promise
    console.log(2)
}).catch(() => {
    console.log(3)
})
// 1, 2
```

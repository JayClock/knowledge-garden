---
date: 2024-10-12T17:58:33
updated: 2026-05-15 12:16:33
share: true
noteId: 1778807091339
---
JS 闭包的核心机制是什么？

---

- **核心特性**：
	- 访问[[./JS 作用域和作用域链|外部函数作用域]]的变量
	- 即使外部函数执行结束，变量依然被保留
	- 不会被[[./JS GC|垃圾回收]]，直到闭包不再被引用，会造成[[./JS 内存泄漏|内存泄漏]]
- **核心背景**：
	- 自由变量的查找，是在函数定义的地方，向上级作用域查找，不是在执行的地方
- **闭包的应用场景**：
	1. 私有变量（模拟封装）
		```js
		function createCounter() {
		  let count = 0 // 私有变量，外部无法直接访问
		  return {
		    increment: () => ++count,
		    decrement: () => --count,
		    getCount: () => count,
		  }
		}
		
		const counter = createCounter()
		console.log(counter.increment()) // 1
		console.log(counter.increment()) // 2
		console.log(counter.getCount()) // 2
		console.log(counter.count) // undefined（外部无法直接访问）
		```
	2. 回调 & 事件监听
		```js
		function addEventLogger(eventName) {
		  return function () {
		    console.log(`Event ${eventName} triggered!`)
		  }
		}
		
		document.addEventListener('click', addEventLogger('click'))
		```
	3. 定时器 & 异步操作
		```js
		function delayedGreeting(name) {
		  setTimeout(() => {
		    console.log(`Hello, ${name}!`)
		  }, 2000)
		}
		delayedGreeting('Rain') // 2 秒后打印 "Hello, Rain!"
		```
- **闭包的缺点：**
	1. 可能导致内存泄漏
 - 闭包会持有外部变量的引用，导致变量无法被垃圾回收
 - 解决方案：手动将变量置为 null 或谨慎管理作用域
	2. 滥用闭包可能影响性能
 - 每次调用都会创建新的作用域，影响垃圾回收机制
 - 适度使用，避免不必要的闭包

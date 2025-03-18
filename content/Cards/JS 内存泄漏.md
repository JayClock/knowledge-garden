---
date: 2024-10-16T10:15:18
updated: 2025-02-19T10:50:37
share: true
tags:
  - review
---
- 变量销毁不了，一定就是内存泄漏吗？
	不一定，只有在**非预期的场景下，变量没有被[[./JS GC|垃圾回收]]**，才算内存泄漏。闭包虽然内存没有被回收，但是符合我们的预期表现。【注意】这一说法没有定论，有些面试官可能会说“不可被垃圾回收就是内存泄漏”，不可较真。
- 如何检测内存泄漏
- 内存泄漏的场景
	- 被全局变量、函数引用，组件销毁时未被清除
		```js
		window.arr = this.arr
		window.print = ()={}
		```
	- 被全局事件、定时器引用，组件销毁时未被清除
		```js
		this.intervalId = setInterval(()=>{
			console.loh(this.arr)
		},100)
		```
	- 被自定义事件引用，组件销毁时未清除
		```js
		const printArr = () => {
			console.log(this.arr)
		}
		
		window.addEventLisner('resize', printArr)
		
		window.removeEventLisner('resize', printArr)
		```


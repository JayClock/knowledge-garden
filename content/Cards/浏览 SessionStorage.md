---
date: 2025-05-20T16:53:10
updated: 2026-05-15 12:16:33
share: true
noteId: 1778807088130
---
浏览器 SessionStorage 的机制和使用要点是什么？

---

SessionStorage 和 [[./浏览器 LocalStorage|LocalStorage]] 都是在HTML5才提出来的存储方案，SessionStorage 主要用于临时保存同一窗口(或标签页)的数据，刷新页面时不会删除，关闭窗口或标签页之后将会删除这些数据。
- **SessionStorage与LocalStorage对比**：
	- SessionStorage和LocalStorage都在**本地进行数据存储**；
	- SessionStorage也有同源策略的限制，但是SessionStorage有一条更加严格的限制，SessionStorage**只有在同一浏览器的同一窗口下才能够共享**；
	- LocalStorage和SessionStorage**都不能被爬虫爬取**；
- **常见用法**：
	```js
	// 保存数据到 sessionStorage
	sessionStorage.setItem('key', 'value');
	// 从 sessionStorage 获取数据
	let data = sessionStorage.getItem('key');
	// 从 sessionStorage 删除保存的数据
	sessionStorage.removeItem('key');
	// 从 sessionStorage 删除所有保存的数据
	sessionStorage.clear();
	// 获取某个索引的Key
	sessionStorage.key(index)
	```
- **使用场景**：
	- 由于SessionStorage具有时效性，所以可以用来存储一些网站的游客登录的信息，还有临时的浏览记录的信息。当关闭网站之后，这些信息也就随之消除了。

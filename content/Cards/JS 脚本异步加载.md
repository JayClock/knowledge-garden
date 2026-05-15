---
date: 2025-05-19T20:49:50
updated: 2026-05-15 12:16:33
share: true
noteId: 1778807091445
---
JS 脚本异步加载的核心机制是什么？

---

1. 动态创建 `<script>` 标签，并设置其 src 属性为需要加载的脚本 URL。这种方式可以通过设置 onload 或 onreadystatechange 事件来检测脚本是否加载完成。
	```js
	const script = document.createElement('script');
	script.src = 'path/to/script.js';
	script.onload = function() {
	 // 脚本加载完成后执行的回调函数
	};
	document.body.appendChild(script);
	```
2. 使用 [[./XMLHttpRequest|XMLHttpRequest]] 对象或 Fetch API 发送异步请求，并在请求成功后将响应文本解析为 JavaScript 代码，然后使用 eval() 函数或 Function() 构造函数来执行脚本。
	```js
	const xhr = new XMLHttpRequest();
	xhr.open('GET', 'path/to/script.js');
	xhr.onload = function() {
	 const script = document.createElement('script');
	 script.textContent = xhr.responseText;
	 document.head.appendChild(script);
	};
	xhr.send();
	```
3. 使用 `async`，`asnyc` 是下载完成后，立即异步加载，**加载好后立即执行**，多个 `asnyc`，多个 async 属性的标签，不能保证加载的顺序
4. 使用 `defer`，`defer` 是下载完成后，立即异步加载。加载好后，如果 DOM 树还没构建好，则先**等 DOM 树解析好再执行**；如果DOM树已经准备好，则立即执行。多个带defer属性的标签，按照顺序执行。

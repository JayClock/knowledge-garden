---
date: 2024-10-26T15:06:04
updated: 2026-05-15 12:16:33
share: true
noteId: 1778807091593
---
JS 严格模式的核心机制是什么？

---

- 如何开启
	```js
	'use strict' // 全局开启
	
	function fn() {
	  'use strict' // 某个函数开启
	
	}
	```
- 特点
	- 全局变量必须先声明
		```js
		"use strict";
		n = 10; // ReferenceError: n is not defined
		```
	- 静止使用 with
		```js
		"use strict";
		var obj = { x: 10 };
		with (obj) {
		  // Uncaught SyntaxError: Strict mode code may not include a with statement
		  console.log(x);
		}
		```
	- 创建 evel 作用域
		```js
		"use strict";
		var x = 10;
		eval("var x = 20; console.log(x)");
		console.log(x);
		```
	- 静止 this 指向 window
		```js
		"use strict";
		function fn() {
		  console.log("this", this); // undefined
		}
		fn();
		```
	- 函数参数不能重名
		```js
		"use strict";
		// Uncaught SyntaxError: Duplicate parameter name not allowed in this context
		function fn(x, x, y) {
		  return;
		}
```

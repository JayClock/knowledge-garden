---
date: 2024-10-25T16:16:45
updated: 2026-05-15 10:03:24
share: true
noteId: 1778807090447
---
CSS 定位的规则和常见用法是什么？

---

- absolute 和 relateive 分别依据什么定位
	- relative 依据自身定位
	- absolute 依据最近一层的 positive / relative 定位

	```html
	<!DOCTYPE html>
	<html>
	  <head>
	    <meta charset="UTF-8" />
	    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
	    <meta http-equiv="X-UA-Compatible" content="ie=edge" />
	    <title>absote relative 定位问题</title>
	    <style type="text/css">
	      body {
	        margin: 20px;
	      }
	      .relative {
	        position: relative;
	        width: 400px;
	        height: 200px;
	        border: 1px solid #ccc;
	        top: 20px;
	        left: 50px;
	      }
	      .absolute {
	        position: absolute;
	        width: 200px;
	        height: 100px;
	        border: 1px solid blue;
	        top: 20px;
	        left: 50px;
	      }
	    </style>
	  </head>
	  <body>
	    <p>absolute 和 relative 定位问题</p>
	    <div class="relative">
	      <div class="absolute">this is absolute</div>
	    </div>
	  </body>
	</html>
```

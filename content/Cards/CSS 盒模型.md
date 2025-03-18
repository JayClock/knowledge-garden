---
date: 2024-10-25T16:11:46
updated: 2025-02-19T10:50:37
share: true
tags:
  - review
---
- 盒模型宽度计算
	- offsetWidth = (内容宽度 + 内边距 + 边框)，无外边距
	- offsetWidth = 100 + 20 + 2 = 122
	```css
	#div1 {
	  width: 100px;
	  padding: 10px;
	  border: 1px solid #ccc;
	  margin: 10px;
	  box-sizing: border-box; // offsetWidth 为100
	}
```
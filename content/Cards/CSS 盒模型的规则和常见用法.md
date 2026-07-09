---
date: 2024-10-25T16:11:46
noteId: 1778930946741
share: true
updated: 2026-07-09 11:00:29
---
CSS 盒模型的规则和常见用法是什么？

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

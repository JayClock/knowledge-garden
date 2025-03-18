---
date: 2024-09-24T22:00:31
updated: 2025-02-19T10:50:35
share: true
tags:
  - review
---
- 出现原因：
	DOM 操作非常耗时，[[./数据驱动（MVVM）|数据驱动]]视图下，如何有效控制 DOM 操作。
- 解决方案：
	DOM 操作很慢，但是 JS 执行很快，通过 JS 模拟 DOM 结构，[[./Diff 算法|Diff 算法]]计算出最小的变更，来操作对应的 DOM
- JS 模拟 DOM 结构示例：

	```html
	<div id="div1" class="container">
	  <p>vdom</p>
	  <ul style="font-size: 20px">
	    <li>a</li>
	  </ul>
	</div>
	```

	```js
	{
	  tag: 'div',
	  props: {
	    className: 'container',
	    id: 'div1',
	  },
	  children: [
	    {
	      tag: 'p',
	      children: 'vdom',
	    },
	    {
	      tag: 'ui',
	      props: {
	        style: 'font-size:20px',
	      },
	      children: [
	        {
	          tag: 'li',
	          children: 'a',
	        },
	      ],
	    },
	  ],
	}
	```
- 典型的 vdom 库：[snabbdom](https://github.com/snabbdom/snabbdom)
- vdom 真的很快吗？
	- vdom 并不快，JS 直接操作 DOM 才是最快的
	- 但“数据驱动视图”要有合适的技术方案，不能全部 DOM 重建
	- vdom 就是目前最合适的技术方案（并不是因为它快，而是合适）
	- svelte 就不用 vdom
	- angular 用不用？

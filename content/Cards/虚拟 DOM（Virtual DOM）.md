---
date: 2024-09-24T22:00:31
updated: 2024-10-25T14:18:05
share: true
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

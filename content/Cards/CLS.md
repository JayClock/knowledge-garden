---
date: 2025-05-16T18:39:27
updated: 2025-05-16T18:52:24
share: true
---
- **概念**：[积布局偏移（Cumulative Layout Shift，简称 CLS）](https://web.dev/articles/cls)是一个网页指标，用于衡量在网页的整个生命周期内所有意外布局偏移的总分。阅读一篇新闻文章时，页面顶部的广告突然弹出，导致所有内容向下移动。
- **优化建议**：每一帧中，浏览器视口内的所有元素没有水平或垂直距离的移动。
	1. 给每张图片设置 width height 属性，让浏览器提前在网页上分配空间，最大程度减少重排和重新布局的可能
		```html
		<img 
		  src="image.jpg" 
		  width="400" 
		  height="160" 
		  class="cls" 
		  alt="image"
		/>
		```
	2. 对于异步加载带来的动态内容，可以通过骨架屏的方式，进行高宽限制
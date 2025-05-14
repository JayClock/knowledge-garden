---
date: 2025-05-14T10:43:43
updated: 2025-05-14T11:00:41
share: true
---
![TTFB Values](https://knowledge-garden.oss-cn-shanghai.aliyuncs.com/images/TTFB%20Values.svg)
- **三个阶段**
	- **HTTPRequestTime**：用户访问前端应用时，他的浏览器会向服务器发送 HTTP 请求。在这个阶段，浏览器需要向服务器发送一次页面请求
	- **ProcessRequestTime**：服务器收到通信请求后，会开始生成页面或数据。这个过程可能涉及数据库调用、缓存读取、页面文档生成等多种情况。所以需要一些时间来生成响应页面
	- **HTTPResponseTime**：服务器处理完成后，它会将页面内容返回给浏览器，这就是 HTTP 响应的过程。由于两端位于不同的区域，因此在响应传输阶段也需要一定的时间才能返回到用户那里
---
date: 2025-05-04T21:22:13
updated: 2026-05-16 19:29:23
share: true
noteId: 1778930950666
---
URL 包含哪些部分？

---

1. 协议（protocol）：如 `http://`、`https://`、`ftp://` 等
2. 域名（domain）：如 `www.example.com`
	- 子域名：`www`
	- 主域名：`example`
	- 顶级域名：`com`
3. 端口号（port）：如 `:80`、`:443`（可选，HTTP 默认 80，[[./HTTPS 如何保证传输安全？|HTTPS 如何保证传输安全？]] 默认 443）
4. 路径 (path)：如 `/users/123/orders`，来指示表示某个资源，而**这种结构可以看作是对某种层次结构遍历的结果**。而这个结构，就是我们的**领域模型**。比如
	```plantuml
	class User {}
	
	class Order {}
	
	User "1" *-- "*" Order
	```
5. 查询参数 (query string)：如 `?id=123&name=test`
6. 锚点/片段标识符 (fragment)：如 `#header`

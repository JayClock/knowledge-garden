---
date: 2025-05-20T16:49:44
updated: 2025-05-20T16:51:34
share: true
---
LocalStorage是HTML5新引入的特性，由于有的时候我们存储的信息较大，[[./浏览器 Cookie|Cookie]]就不能满足我们的需求，这时候LocalStorage就派上用场了。
- **LocalStorage的优点：**
	- 在大小方面，LocalStorage的大小一般为5MB，可以储存更多的信息
	- LocalStorage是持久储存，并不会随着页面的关闭而消失，除非主动清理，不然会永久存在
	- 仅储存在本地，不像Cookie那样每次HTTP请求都会被携带
- **LocalStorage的缺点：**
	- 存在浏览器兼容问题，IE8以下版本的浏览器不支持
	- 如果浏览器设置为隐私模式，那我们将无法读取到LocalStorage
	- LocalStorage受到[[./同源策略|同源策略]]的限制，即端口、协议、主机地址有任何一个不相同，都不会访问
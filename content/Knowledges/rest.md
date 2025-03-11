---
date: 2025-01-18T15:41:31
updated: 2025-03-11T14:03:05
share: true
---
**客户端-服务端（Client-Server）**: 这个更专注客户端和服务端的分离，服务端独立可更好服务于前端、安卓、IOS等客户端设备。

**无状态（Stateless）**：服务端不保存客户端状态，客户端保存状态信息每次请求携带状态信息。

**可缓存性（Cacheability）** ：服务端需回复是否可以缓存以让客户端甄别是否缓存提高效率。

**统一接口（Uniform Interface）**：通过一定原则设计接口降低耦合，简化系统架构，这是RESTful设计的基本出发点。当然这个内容除了上述特点提到部分具体内容比较多详细了解可以参考这篇[REST论文内容](https://www.ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm)。

**分层系统（Layered System）**：客户端无法直接知道连接的到终端还是中间设备，分层允许你灵活的部署服务端项目。

**按需代码（Code-On-Demand，可选）**：按需代码允许我们灵活的发送一些看似特殊的代码给客户端例如JavaScript代码。
---
date: 2025-05-11T14:23:48
updated: 2026-05-15 12:16:33
share: true
noteId: 1778807090990
---
HTTP 0.9 的关键特性是什么？

---

![HTTP 0.9 请求流程](https://knowledge-garden.oss-cn-shanghai.aliyuncs.com/images/HTTP%200.9%20%E8%AF%B7%E6%B1%82%E6%B5%81%E7%A8%8B.png)

- 客户端先要根据 IP 地址、端口和服务器建立 [[./TCP|TCP]] 三次握手
- 建立好连接之后，会发送一个 GET 请求行的信息，如GET /index.html用来获取 index.html。
- 服务器接收请求信息之后，读取对应的 HTML 文件，并将数据以 ASCII 字符流返回给客户端。
- HTML 文档传输完成后，断开连接。

---
date: 2025-01-29T12:54:43
noteId: 1778930950167
updated: 2026-07-25 09:00:47
---
Smart Domain Pattern 的核心思想和适用场景是什么？

---

- Object-Oriented Approach（No service）
- Model as fully connected object graph （Not disconnected aggreation）
- Direcly map to restful API（with HATEOAS）
- Act as an absracion layer to hide implentation details
- Consistent between conceptual model / model / api

Entity is not about value，but about identity and association。
Can be mapped easily as s lossess representation model
Association is as abstraction mechanism for connections
Association is as abstraction mechanism for lifecycle
![Pasted image 20250129182130](https://knowledge-garden.oss-cn-shanghai.aliyuncs.com/images/Pasted%20image%2020250129182130.png)
kenk back CRC 法

Restful 不是关于 get put put post，而是学习了互联网架构模式（数据表达行为），和面向对象本书数据抽象行为一致

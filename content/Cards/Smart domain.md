---
date: 2025-07-11 23:29:39
updated: 2025-07-14 22:35:38
share: true
---
[代码样例](https://github.com/JayClock/platform/tree/main)
在传统的 DDD 设计中，我们往往会想下面这样写
```
UserService {
    create User
    update User
}

OrderService {
    create Order
    update Order
}
```
给每一个实体都构造一个 

- 完全[[../Knowledges/面向对象|面向对象]]（没有 service）
- 所有模型建立成完全连接的对象图（所有聚合都不会断开）
- 所有模型会直接映射成 [[../Knowledges/HATEOAS|RESTful api]]（HATEOAS 形式）
- 屏蔽所有实现细节抽象层
- 概念模型、模型、api 上完全映射一致
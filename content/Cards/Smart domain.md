---
date: 2025-07-11 23:29:39
updated: 2026-05-15 09:35:34
share: true
noteId: 1778807093246
---
Smart domain 的核心思想和适用场景是什么？

---

在传统的 DDD 设计中，我们往往会想下面这样写
```
// 数据结构 (通常是一个简单的 POJO/POCO)
class User {
    private Long id;
    private String name;
    private String email;
    // 只有 getters 和 setters...
}

// 操作数据的过程/服务
class UserService {
    private UserRepository userRepository;

    // 过程一：创建用户
    public void createUser(UserDTO userData) {
        User user = new User();
        user.setName(userData.getName());
        user.setEmail(userData.getEmail());
        // ... 其他业务逻辑和校验
        userRepository.save(user);
    }

    // 过程二：更新用户
    public void updateUser(Long userId, UserDTO userData) {
        User user = userRepository.findById(userId);
        user.setName(userData.getName());
        // ... 其他业务逻辑和校验
        userRepository.save(user);
    }
}
```
在这个结构中：
1. **`User` 实体（Entity）是“贫血”的**：它几乎没有任何业务逻辑，只是一个数据的容器。它的所有属性都可以通过 `set` 方法被外界随意修改，自身不负责维护其数据的一致性和业务规则。它就像一个 C 语言中的 `struct`。
2. `UserService` 是一个“过程脚本”：所有的业务逻辑、验证规则、状态变更都集中在 `UserService` 中。`UserService` 就像一个包含了一系列函数的模块，它接收数据（`User` 对象），处理它，然后输出结果。这个服务“指挥”着 `User` 对象，而不是 `User` 对象“自己行动”。

当业务逻辑变得复杂时，不同的事务脚本之间很容易出现代码重复。由于没有一个核心的、富含业务逻辑的领域模型，业务规则会散落在系统的各个角落，难以维护和演进。最典型的就是 [[./Smart UI|Smart UI]]。

在真正的DDD中，我们追求的是**充血模型（Rich Domain Model）**。
- 完全[[../Knowledges/面向对象|面向对象]]（没有 service）
- 所有模型建立成完全连接的对象图（所有聚合都不会断开）
- 所有模型会直接映射成 [[../Knowledges/Restful|RESTful api]]（HATEOAS 形式）
- 屏蔽所有实现细节抽象层
- 概念模型、模型、api 上完全映射一致
[代码样例](https://github.com/JayClock/platform/tree/main)

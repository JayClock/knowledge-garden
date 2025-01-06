---
date: 2024-10-09T15:30:30
updated: 2025-01-06T09:51:48
share: true
title: 产研提效 02｜User 入手，构建第一个模型
categories:
  - 产研提效
  - ai
---
#### 当反模式遇到新技术

在上一篇中我们讨论了一些平时觉得没什么问题，但是违反认知的反模式。这些反模式可以说是，我们在使用 AI 时最大的问题。

**贫血模型表达业务**带来的“各有各的道理”，导致我们无法在生成代码时选择有效的上下文，毕竟选哪一个“都行”。
**特性分支**带来的知识滞后性，导致一部分人在花费大精力"重构"，另一部分人却在用 AI 不断生成本该被废弃掉的用法。
**写一点跑一下**的开发习惯，可以说是最糟糕的。我们自己都不知道自己写的代码，会对原有系统造成什么影响，却希望 AI 生成的代码，可以避免意料之外的变更。

我们习以为常的反模式，导致我们根本无法理解遗留系统中有什么，而我们要正确分解任务，恰恰需要我们对遗留系统的合理理解。我们直接把代码库 rag 化，让开发者通过对话的形式，去理解系统可以吗？当然可以，前提是代码库本身就是可读的。**代码没有任何文档和注释，就想要 AI 来理解代码，可以说是团队追求 AI 辅助研发时，最大的误区了**。
#### DDD：能让人读懂，就能用 AI 查

所谓合理理解遗留系统，其实就是团队之间能够拉齐共识。当我们阅读到别人的代码时，多数时刻都应该处于 **Clear** 模式。我们不光要明白这段代码完成了什么业务，也要理解它实现的架构模式（比如如何分层，用了哪些技术的哪些 API）。

那么我们的对于软件工程的要求就在于：
1. 如何更快速的理解软件结构？
2. 讨论及更改需求时，我们要如何更快地定位到要变更的部分？
3. 当我们和业务沟通时，如何提供更低的传递成本？

自然而然地，我们需要
#### 你的分层合理吗？

在我们平时开发中，我们往往会将接口设计分为以下几个层次。
1. **控制器层（Controller Layer）**：负责处理 HTTP 请求，调用服务层的方法，并将结果返回给客户端。
	```java
	@RestController
	@RequestMapping("/api/users")
	public class UserController {
	
	    @Autowired
	    private UserService userService;
	
	    @GetMapping
	    public List<User> getAllUsers() {
	        return userService.getAllUsers();
	    }
	
	    @GetMapping("/{id}")
	    public ResponseEntity<User> getUserById(@PathVariable Long id) {
	        return userService.getUserById(id)
	                .map(ResponseEntity::ok)
	                .orElse(ResponseEntity.notFound().build());
	    }
	
	    @PostMapping
	    public User createUser(@RequestBody User user) {
	        return userService.createUser(user);
	    }
	
	    @PutMapping("/{id}")
	    public ResponseEntity<User> updateUser(@PathVariable Long id, @RequestBody User userDetails) {
	        return ResponseEntity.ok(userService.updateUser(id, userDetails));
	    }
	
	    @DeleteMapping("/{id}")
	    public ResponseEntity<Void> deleteUser(@PathVariable Long id) {
	        userService.deleteUser(id);
	        return ResponseEntity.noContent().build();
	    }
	}
	```
2.  **服务层（Service Layer）**：负责业务逻辑的处理，调用仓库层的方法来操作数据库。
	```java
	@Service
	public class CustomerService {
	
	    private final CustomerRepository customerRepository;
	
	    @Autowired
	    public CustomerService(CustomerRepository customerRepository) {
	        this.customerRepository = customerRepository;
	    }
	
	    public List<Customer> getAllCustomers() {
	        return customerRepository.findAll();
	    }
	
	    public Optional<Customer> getCustomerById(Long id) {
	        return customerRepository.findById(id);
	    }
	
	    public Customer createCustomer(Customer customer) {
	        return customerRepository.save(customer);
	    }
	
	    public Customer updateCustomer(Long id, Customer customerDetails) {
	        Customer customer = customerRepository.findById(id).orElseThrow(() -> new RuntimeException("Customer not found"));
	        customer.setName(customerDetails.getName());
	        customer.setEmail(customerDetails.getEmail());
	        return customerRepository.save(customer);
	    }
	
	    public void deleteCustomer(Long id) {
	        customerRepository.deleteById(id);
	    }
	}
	```
3. **仓库层（Repository Layer）**：负责与数据库交互，提供数据的增删改查操作。
	```java
	public interface CustomerRepository extends JpaRepository<Customer, Long> {
	}
	```
4. **模型层（Model Layer）**：定义模型对象（如 `Customer`），用于直接映射数据库
	```java
	@Entity
	public class Customer {
	    @Id
	    @GeneratedValue(strategy = GenerationType.IDENTITY)
	    private Long id;
	    private String name;
	    private String email;
	
	    public Long getId() {
	        return id;
	    }
	
	    public void setId(Long id) {
	        this.id = id;
	    }
	
	    public String getName() {
	        return name;
	    }
	
	    public void setName(String name) {
	        this.name = name;
	    }
	
	    public String getEmail() {
	        return email;
	    }
	
	    public void setEmail(String email) {
	        this.email = email;
	    }
	}
```
这种基于贫血模型的传统开发模式，将数据与业务逻辑分离，违反了 OOP 的封装特性，实际上是一种**面向过程**的编程风格。它只是一层一层去传递数据罢了。但是，现在几乎所有的 Web 项目，都是基于这种贫血模型的开发模式，甚至连 Java Spring 框架的官方 demo，都是按照这种开发模式来编写的。 

这个原因其实很简单，在软件开发早期，我们做的基本上还是较为简单的 CURD。不需要花费大力气去精心设成**充血模型**，毕竟本身业务行为就不多，做出来的充血模型也比较贫瘠。

但是在软件规模扩张的过程中，我们会面对**面向过程**的开发模式带来的诸多问题
1. 服务层的无限制扩张，包含了过多的上下文信息，最终导致代码的僵化，也就是我们平时吐槽的“改不动的代码”。
2. 服务层中往往会出现大量重复的判断逻辑，为了降低重复，我们往往会把这些重复代码封装层各种 util，但是在多数情况下这并没有解决什么问题，我们依旧需要深入实现细节，才能区分 uil 和 service 的职能。而且在多数情况下，工具方法是在 util 还是 service 是非常随心所欲的，也没有什么职能可以区分。
3. 线性调用的面向过程写法，无法支持复杂业务的网状结构，带来的就是难以理解的依赖关系。

即使仅仅是当前如此简单的代码示例，我们也依旧会有如下一些问题：
1. 模型层的数据结构和控制器层的返回结果完全一致，数据结构的变化会直接表现在前端请求接口的地方
2. 模型层中使用了 jpa 相关的注解，就意味着在模型层就限制了实现层只能通过 Hibernate、EclipseLink 等符合 JPA 规范的持久化框架。低层次模型只能限制高层次具体要实现什么接口，而不应该限制如何实现。
# 何时调整分层？

1. 团队中已经有“两个披萨”规模的人数，也就是 8 个人以上，这时已经对管理者带来了一定的要求。
2. 找 5 个开发工程师，单独对同一个要迭代的功能进行任务分解，在大多数公司中，这 5 个人往往会分解出 5 种不同的样子。人员规模上去了，但是团队认知却没有拉齐。在开发中的具体表现就是，我们在做所谓的 codereview 时，负责 review 的人既不能确定代码中是否实现了正确的功能，也不明确否按照合理的软件架构去组织代码。所有的交付验证，全部积压到了 QA 上。

如果满足上面的条件，我们其实已经陷入了“知识僵化”的境地，即所有的业务知识和架构知识，都存在于少数人的脑子中，而非由代码来表达。这样的团队往往是不重视重构的团队（小步快跑的重构，不是花几个月甚至几年的时间开个新模块拉坨大的)。我们不得不处理处理越来越混乱的系统，不断拖慢我们的进度。

# 什么是充血模型？

充血模型是一种软件设计模式，特别是在领域驱动设计（DDD）中被广泛应用。它强调将业务逻辑和行为紧密地绑定到对应的实体（Entity）或值对象（Value Object）上，而不是将这些逻辑分散在 service 或 controller 中。通过这种方式，充血模型能够**更好地反映现实世界中的业务规则和交互，使代码更具表达力和可维护性**。

具体来说，充血模型要求在实体上直接定义与该实体相关的业务行为方法。例如，在一个图书借阅系统中，如果需要表达“客户切换账号这个行为”这一行为，应该在`Customer`实体上定义一个`switchAccount`方法，即`customer.switchAccount()`。这种设计方式使得实体不仅包含数据（属性），还包含与这些数据相关的行为（方法），从而形成一个“充血”的实体。

# 谁来查询实体？

对于读者和图书，读者与图书是一对多的关系的情况下，如果我们要查询某一本图书，那么自然而然的，我们会把查询图书的逻辑，绑定在 reader 实体上，即`reader.findBookByName(...)`。但是，当读者登陆的时候，我们又应该由谁基于登陆信息，去查询出特定的读者信息呢。这似乎由回到使用 service 和 repository 去了。我们重新回顾一下平时在表中查询数据的过程，比如这个 SQL `SELECT * FROM users WHERE phone_number = '手机号'`；我们在查询某一个内容时，首先第一件事，就是要明确它在哪一个表（集合下）。**所以我们可以对这个集合进行建模**！对于查询 customer，我们需要构建一个 customers 对象

此时的模型如下图


```java
// 领域模型层不应该有具体实现，所以抽象成接口
// 持久化的时候，不论用什么持久化框架都与我无关
public interface Customers {  
    Optional<Customer> findById(Long id);  
}
```

对于实体本身，其实真正重要的，是唯一的身份标识（identity），实体的身份标识一旦被确立，就不可被更改。至于其它的属性，完全是可变的。我们可以把可变的与不可变的区分开来：

```java
public record CustomerDescription(String name, String email) {  
}

public class Customer {
	// 不可变的 identity
    private final String identity;
    // 可变的 description 描述
    private final CustomerDescription description;

    public Customer(String identity, CustomerDescription description) {
        this.identity = identity;
        this.description = description;
    }

    @Override
    public String getIdentity() {
        return identity;
    }

    @Override
    public CustomerDescription getDescription() {
        return description;
    }
}
```

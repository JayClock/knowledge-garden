---
date: 2024-10-09T15:30:30
updated: 2025-01-01T17:23:01
share: true
title: 产研提效 02｜User 入手，构建第一个模型
categories:
  - 产研提效
  - ai
---
在上一篇我们分享了几种常见的反模式，其实都不是什么技术问题。不管是用充血模型表达业务，还是通过 TDD 的方式去编写代码，更多的是一种技巧，就像英语一样，需要我们不断反复地去练习，才能掌握。而 TDD 的学习难点**理解需求，并将需求分解为功能点**。这就陷入了一种死循环，上一篇的各种反模式积累出来的问题，导致**我们无法正确理解已有的需求，而我们又必须基于对已经存在的需求的正确理解上，才能合理地分解业务**。虽然按照 TDD 的模式开发各种工具对个人来说是一种很好地学习方式，但是却难以向团队传递 TDD 带来的诸多好处。

我的切入点是：
1. 通过对遗留系统的改造，建立一个新系统。
2. 在可读性较高的新系统中，去建立 TDD 的练习场。
#### 向钱看齐

很多时候，我们所谓地对遗留系统的处理，往往是一种**伪装成“重构”的重写**，在一次性大量代码变更下，带来诸多 breakchange。至于为什么要重构，可能是性能过低，可能是代码过长，也有可能是单纯地某一个员工代码写烦了以重构为名申请了个任务罢了。最终的表现就是，明明花了大量时间在对代码的处理上，但不管是 bug 数量，还是未来新增逻辑的效率，都没有什么提升。

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

---
date: 2025-01-18T15:41:31
updated: 2025-07-13 23:46:49
share: true
---
REST（表述性状态转移）是一种架构风格，而非协议，其精髓在于一系列约束，这些约束由 Roy Fielding 在其博士论文中定义 。在其所有约束中，“统一接口”是将其与其他网络架构风格区分开来的核心特征，而 HATEOAS 正是实现统一接口不可或缺的关键组成部分 。  

与真正的 REST/HATEOAS 方法形成鲜明对比的是，业界普遍的做法是通过 HTTP 构建 RPC风格的 API（随之而来的是**大量面向过程代码**） 。这种方法通常依赖 Swagger 或 OpenAPI 等工具生成静态文档，客户端开发者根据这份“契约”硬编码所有 API 端点的 URL 。这种模式在客户端和服务器之间建立了紧密的耦合关系，一旦服务器的 URL 结构发生变化，客户端应用就可能崩溃 。  

HATEOAS 所要解决的正是这个问题。其核心思想是，一个 REST 客户端在与应用交互时，除了一个初始的入口点 URL 和对超媒体（如 HTML 或特定的 JSON 媒体类型）的通用理解外，几乎不需要任何关于如何与服务器交互的先验知识 。客户端的所有后续操作都应通过解析服务器响应中动态提供的信息来发现 。

比如在传统的非 HATEAOS 架构中，前端代码库中充斥着用于构建 API 端点的字符串模板和拼接逻辑，例如 `const url = /api/orders/${orderId}/items`。这种做法不仅繁琐且易错，还增加了JavaScript包的体积。采用HATEOAS后，客户端不再需要构建URL。取而代之的是，它只需在API响应中查找具有特定关系类型（`rel`）的链接，并直接使用其`href`属性 。这消除了整整一类客户端代码。

这种架构范式要求前端开发者从一个“客户端无所不知”（即客户端根据静态的 OpenAPI/Swagger 规范来编排调用）的模型，转变为一个“服务器指引方向”的模型。当采用 HATEOAS 时，业务逻辑的重心也发生了转移。在非 HATEOAS 应用中，前端可能需要获取数据并执行自身的逻辑（例如，`if (balance > 0) { showWithdrawButton(); }）`来控制 UI。而在 HATEOAS 应用中，前端的逻辑被简化为 `if (response.links.withdraw) { showWithdrawButton(); }` 。这意味着关于“何时可以提款”的业务规则完全由后端掌控，前端演变为一个更纯粹的、用于渲染服务器所提供状态转换的“引擎”。这简化了客户端，但要求后端团队对应用的完整状态逻辑负全责。

这种逻辑上的精简对前端性能有着切实的积极影响。更少的条件判断、URL 模板和状态管理代码意味着更小的包体积，一个更小的包体能够带来一系列连锁优势：更快的下载时间（尤其在移动网络环境下）、更短的JavaScript解析和编译时间，**最终促成更快的“可交互时间”（Time to Interactive, TTI），这是一个衡量用户体验的核心性能指标**。

此外，这种客户端逻辑的简化不仅仅是代码量的减少，它还创造了一个更具弹性和“性能更优”的开发流程。一个只负责渲染服务器指令的“哑”客户端，更不容易出现因前后端业务逻辑不同步而导致的错误 。当服务器的业务规则变更时（，前端无需重新部署。服务器只需开始发送不同的链接组合，UI便能自动适应。

![smart-domain](https://knowledge-garden.oss-cn-shanghai.aliyuncs.com/images/smart-domain.png)

传统的 JDBC 形式，需要大量散落在各处的 service 和 mapper 来保持生命周期一致性，每次我们新增一个功能，都需要在整个项目中，调用大量之间没什么关联的 service，形成一个巨大的 service 调用网络。

很多人使用 JDBC 的形式去使用 DDD，最终却发现，越是复杂的项目，service 调用网越混乱，新增功能时越是难以找到需要用的 service。最终只能得出一个 [[./领域驱动设计|DDD]] 无用的结论。

还有一个现象是，很多人用 AI 会在 prompt 中，要求 AI 遵循 SOLID 原则，最终导致项目中有大量的只有一两个方法的 service。虽然遵循 SOLID，但是却无法从代码中，反推出背后有哪些业务在调用它。

而 sub-resource 的形式，更适合 DDD 映射业务模型的关联关系，下面是 java 的 spring hateaos 下的形式，ts 目前没有相关的框架，也许可以这么设计 [[../Express/restful web service spike|restful web service spike]]

```java
// 根入口 customer
@Path("/customers")
public class CustomersApi {
    private Customers customers;

    @Inject
    public CustomersApi(Customers customers) {
        this.customers = customers;
    }

    @Path("{id}")
    public CustomerApi findById(@PathParam("id") String id) {
        return customers.findById(id).map(CustomerApi::new).orElse(null);
    }
}

public class CustomerApi {
    private Customer customer;

    public CustomerApi(Customer customer) {
        this.customer = customer;
    }

   // 获取单个 customer
    @GET
    public CustomerModel get(@Context UriInfo info) {
        return new CustomerModel(customer, info);
    }

   // 获取 customer 下的 accounts
    @Path("accounts")
    public AccountsApi accounts() {
        return new AccountsApi(customer);
    }
}
```

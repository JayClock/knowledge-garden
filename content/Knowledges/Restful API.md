---
date: 2025-01-18T15:41:31
updated: 2025-05-17T22:38:24
share: true
---
RESTful API 是指符合 REST 架构风格的 API 设计，而 REST 架构风格是对互联网规模架构（Internet Scale Architecture）的总结与提炼。这一切都源于 Roy Fielding 提出的一个问题：既然互联网（Internet）是人类迄今为止构造的最大的软件应用，那么到底是什么样的架构原则，支撑了如此规模的异构且互联的系统呢？我们能从中学习到什么，以帮助我们更好地构建软件？

Roy Fielding 将互联网定义为分布式超媒体信息获取系统（Distributed Hypermedia Information Retrieval System）。也就是由超媒体描述的、分布式的信息系统。在这个系统中，信息分布在不同的服务器中，并由超媒体联通。换句话说，[分布式超媒体](<[REST论文内容](https://ics.uci.edu/~fielding/pubs/dissertation/top.htm)>)是互联网的集成策略

- **客户端-服务端（Client-Server）**: 这个更专注客户端和服务端的分离，服务端独立可更好服务于前端、安卓、IOS等客户端设备。
- **无状态（Stateless）**：服务端不保存客户端状态，客户端保存状态信息每次请求携带状态信息。比如 Cookie 等
- **可[[缓存|缓存]]性（Cacheability）** ：服务端需回复是否可以缓存以让客户端甄别是否缓存提高效率。
- **统一接口（Uniform Interface）**：通过一定原则设计接口降低耦合，简化系统架构，这是RESTful设计的基本出发点。当然这个内容除了上述特点提到部分具体内容比较多详细了解可以参考这篇[REST论文内容](https://ics.uci.edu/~fielding/pubs/dissertation/top.htm)。
- **分层系统（Layered System）**：客户端无法直接知道连接的到终端还是中间设备，分层允许你灵活的部署服务端项目。
- **按需代码（Code-On-Demand，可选）**：按需代码允许我们灵活的发送一些看似特殊的代码给客户端例如JavaScript代码。

![[smart-domain|smart-domain]]

传统的 JDBC 形式，需要大量散落在各处的 service 和 mapper 来保持生命周期一致性，这就表示我们越想通过 [[./领域驱动设计|领域驱动设计]] 的方式去设计代码，越发现我们的代码无法和业务模型映射起来。这就带来了业务和技术双方的极大沟通成本。

而 sub-resource 的形式，更适合 DDD 映射业务模型的关联关系

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

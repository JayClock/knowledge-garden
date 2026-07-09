---
title: 15分钟：HATEOAS 资源契约架构
date: 2026-04-21 15:58:29
updated: 2026-07-09 10:45:13
tags:
  - interview
  - architecture
  - hateoas
  - frontend
  - typescript
---

# 15分钟：HATEOAS 资源契约架构

> [!abstract] 一句话总结
> 我解决的是多租户业务里，同一个角色、同一条数据，在不同状态和不同权限上下文下，**能看到什么、能点什么、能提交什么字段** 经常在多端漂移的问题。我的方案是把业务动作从前端 `if-else` 中抽出来，沉到后端资源表达里，通过 HATEOAS 的 `_links` / `_templates` 返回“当前资源当前上下文下允许的动作契约”，再用 TypeScript SDK 和 React Hooks 消费这套契约。

## 1. 问题背景：按钮权限不是前端小问题

在多租户管理场景里，一个资源并不是只有静态数据。它还隐含了很多和上下文相关的业务规则：

- 当前用户是什么角色；
- 当前租户有什么权限；
- 当前资源处于什么状态；
- 当前客户端能展示哪些动作；
- 当前动作需要提交哪些字段。

如果只从前端角度看，这个问题很容易被理解成按钮权限控制，或者 API Service 封装。但放到整个业务维护角度里看，它真正影响的是 **多端业务规则一致性**。

Web、小程序、App 都要表现出同一套业务规则。只要有一个端漏掉某个状态判断，用户看到的动作就会不一致，测试也要重新回归。

## 2. 常规做法的问题：前端复制了一份后端状态机

常规做法是，后端返回一个代表业务状态的 `status` 字段，前端再根据 `status`、`role`、`permission` 写大量判断：

```ts
if (status === 'pending' && role === 'admin') {
  showApproveButton();
}

if (status === 'rejected' && canEdit) {
  showResubmitButton();
}
```

这种方式一开始能跑通，但业务复杂后，成本会快速放大：

- 后端修改状态机流转规则，或者增加一种角色，前端就要跟着改判断并重新发版；
- 后端重构接口，比如从 `/v1/` 升到 `/v2/`，或者调整路径规范，前端硬编码 URL 都要排查；
- Web、小程序、App 各写一套判断，经常出现某一端漏改；
- Payload 字段要求散落在前端，必填、枚举、格式校验一旦和后端不一致，就会产生很多可以提前避免的 400 错误。

在多次测试成本复盘中，我们经常看到同一类问题：同一个角色，在不同客户端的按钮显隐不一致；接口路径或字段变动带来大量联动改动。

本质原因是：**业务规则的权威来源在后端，但执行判断却散落在多个前端。**

继续叠加 Redux、封装更多 API Service，最多只能让代码看起来整齐一点，依旧解决不了规则在沟通中漂移的问题。

## 3. 方案选择：把“能做什么”放回资源表达本身

早期我也探索过几种方案。

第一种是前端维护一份状态机配置，把 `if-else` 收敛成配置表。它可以减少一些重复代码，但本质上还是让前端解释后端规则。

第二种是单独做一个权限接口，前端先请求“当前数据有哪些操作可用”。这个比硬编码好，但权限、URL、Method、Payload Schema 还是分散的。

最终我选择 HATEOAS。核心思想是：

> 当前资源在当前上下文下能做什么，应该和资源状态一起返回。

所以后端在返回资源数据时，除了业务字段，还要返回：

- `_links`：当前资源可以继续导航到哪些资源；
- `_templates`：当前用户、当前状态下可以执行哪些动作，以及动作对应的 URL、Method、Payload 字段要求。

例如审批单资源可以长这样：

```json
{
  "id": "order-1",
  "status": "pending",
  "amount": 1000,
  "_links": {
    "self": { "href": "/orders/order-1" },
    "approve": { "href": "/orders/order-1/approve", "method": "POST" }
  },
  "_templates": {
    "approve": {
      "method": "POST",
      "properties": [
        { "name": "comment", "required": false, "type": "text" }
      ]
    }
  }
}
```

这样前端不需要关心抽象的 `status=pending` 到底意味着什么，也不需要自己解释“审批中、已驳回、已撤回”分别能点什么。前端只需要看当前资源里有没有 `approve` 这个动作。

如果后端没有返回这个动作，按钮就不展示；如果返回了，前端就按模板提交。

## 4. SDK 落地：不是 request 封装，而是资源状态机客户端

为了让这套契约在前端真正可用，我设计了一套 TypeScript SDK。它不是简单的 request 封装，而是一个 HATEOAS 资源状态机客户端。

工程上我把它拆成两个包：

| 包 | 职责 |
|---|---|
| `@hateoas-ts/resource` | 框架无关核心包，负责 `Client`、`Resource`、`StateFactory`、`Fetcher`、`Cache`、`Action/Form` |
| `@hateoas-ts/resource-react` | React 薄适配层，提供 `ResourceProvider`、`useResource`、`useInfiniteCollection`、Suspense Hooks |

核心能力主要有两个：

1. `follow()`：沿着 relation 导航，避免前端硬编码 URL；
2. `action()`：根据后端下发的表单契约执行动作，避免前端手写 Method、URL 和 Payload Schema。

```ts
// 1. 通过泛型严格约束可跟进的 relation，减少硬编码 URL
const postsResource = user.follow('posts', { page: 1 });

// 2. 获取状态，如果当前状态允许创建，就根据 action 表单契约提交
const postsState = await postsResource.get();

if (postsState.hasLink('create-post')) {
  await postsState.action('create-post').submit({
    title: '新文章',
  });
}
```

SDK 内部会自动读取后端下发的 `_links` 或 `_templates` 里的 `href`、`method` 和字段约束，再在底层组装请求。这样前端代码不再依赖具体 URL，而是依赖稳定、具有业务语义的 Relation Name。

后端以后改路径、升版本，只要资源关系不变，前端大部分代码就不需要改。

## 5. 核心调用链：Client → Resource → Fetcher → StateFactory → Cache

这套 SDK 的内部调用链大概是：

```text
createClient({ baseURL })
  -> 初始化 ClientInstance、内容类型解析器和中间件

client.go<User>('/users/123')
  -> 解析 URI，按绝对 URI 复用 Resource 实例

resource.get()
  -> 先读缓存
  -> 如果没有完整缓存，则通过 Fetcher 发送请求
  -> Fetcher 执行认证、Accept、缓存失效等中间件
  -> 响应回来后，根据 Content-Type 选择 StateFactory
  -> StateFactory 把 HAL / HAL-Forms / Siren / Collection+JSON 解析成统一 State
  -> 写入 Cache，并通过 update / stale / delete 事件通知上层
```

这里有几个关键设计点。

### 5.1 Entity 把数据和链接都编码进类型系统

`Entity<TData, TLinks>` 同时表达资源数据和可导航链接：

- `state.data` 有业务字段类型；
- `state.follow('posts')` 的返回类型由 `TLinks['posts']` 推导；
- 不存在的 relation 在 TypeScript 层就会报错。

这样 HATEOAS 不是“运行时才知道有什么链接”，而是通过类型把稳定的业务 relation 显式建模出来。

### 5.2 Resource 按 URI 复用，统一缓存和事件源

`ClientInstance` 内部用绝对 URI 作为 key 缓存 `Resource` 实例。这样同一个资源在客户端只有一个事件源，可以统一处理：

- 请求去重；
- 缓存读写；
- `update` / `stale` / `delete` 事件；
- React Hooks 的订阅刷新。

### 5.3 StateFactory 处理内容协商

后端可能返回 HAL、HAL-Forms、Siren、Collection+JSON，甚至自定义媒体类型。SDK 通过 `StateFactory` 把不同响应格式解析成统一的 `State`。

这使业务层只面向统一接口：

```ts
state.data;
state.links;
state.hasLink('approve');
state.action('approve').submit(payload);
```

不需要业务组件关心具体媒体类型差异。

### 5.4 Action/Form 把超媒体表单变成可执行状态迁移

`_templates`、Siren actions、Collection+JSON queries 这类动作契约会被归一成 `Form` / `Action`。

`action.submit()` 做三件事：

1. 根据表单契约校验 payload；
2. 根据 method 和 content type 序列化请求；
3. 把响应重新解析成新的资源 State。

这就把“按钮点击之后调用哪个接口、传哪些字段”从组件里抽掉了。

## 6. UI 层：React 只响应资源状态，不解释业务规则

到了 UI 渲染层，原来几十行按钮控制逻辑，可以变成：

```tsx
{state.hasLink('approve') && (
  <Button onClick={() => state.action('approve').submit(formData)}>
    审批
  </Button>
)}
```

如果当前用户没权限，或者当前状态不允许审批，后端直接不返回 `approve`。前端对应按钮自然不会出现。

这其实和 React 的理念是一致的：UI 完全由 state 决定。区别是过去我们在前端维护一套和后端同步的业务状态机，再让 UI 响应这套前端状态机；而在 HATEOAS 下，接口返回本身就是当前上下文下的可操作状态。

在 React 适配层，我刻意没有让 Hooks 承担业务判断。`useResource()` 主要做三件事：

1. 解析 Resource 或 ResourceRelation；
2. 读取缓存或触发请求；
3. 监听 Resource 的 `update` / `stale` 事件并刷新组件。

分页也是同样的思路。`useInfiniteCollection()` 不自己拼 `page=2`，而是沿着服务端返回的 `next` relation 继续 follow。这样分页、按钮、表单提交都遵循同一套超媒体契约。

## 7. 带来的收益：一致性、可演进、可测试

一旦协作边界锁死在 API 层状态机作为唯一事实来源，就会带来几个明显收益。

### 7.1 多端一致性

Web、小程序、App 消费同一份 `_links` / `_templates` 契约。权限按钮是否出现，由后端动作字典决定，而不是每个端各写一份判断。

### 7.2 接口路径可演进

前端不硬编码具体 URL，只依赖稳定的 Relation Name。后端做路径重构、版本升级，只要 relation 不变，前端不需要大规模联动。

### 7.3 测试范围收敛

过去测试要反复验证每个端的按钮判断。现在重点可以收敛到两层：

- 后端是否在不同角色、状态、租户下返回正确动作契约；
- 前端 SDK 是否正确解析 `_links` / `_templates` 并渲染 UI。

### 7.4 Agent 友好

这套形式对 AI Agent 也很友好。

Agent 本质上是在代替用户查询数据、分析并执行下一步操作。它不能超出当前用户权限。传统 Agent 可能需要读取 Swagger、API 文档，并在知识库里记录大量规则运算。

但在 HATEOAS 架构下，Agent 只需要读取当前资源状态下的 `_links` 和 `_templates`，就能知道：

- 当前用户有哪些可执行动作；
- 每个动作需要传什么参数；
- 下一步可以导航到哪些资源。

也就是说，后端返回的超媒体契约天然可以转换成 Agent 工具定义或 action schema。

## 8. 总结收束

HATEOAS 解决的不是“前端少写几个 URL”的问题，而是 **业务规则在多端复制和漂移的问题**。

过去前端通过 `status`、`role`、`permission` 自己解释业务状态，本质上是把后端状态机知识复制到多个端里。状态机一变，Web、小程序、App、测试用例和接口文档都可能漂移。

改成 `_links` 和 `_templates` 后，当前资源能做什么、动作怎么提交、字段有什么约束，都跟资源状态一起返回。前端 UI、自动化测试、端侧 SDK，甚至后续 AI Agent，都可以消费同一份动作契约。

而 `hateoas-ts` 的工程化价值，是把这套契约真正落到代码里：用 `Entity` 做类型安全导航，用 `Resource` 管理 URI 级资源实例，用 `StateFactory` 做内容协商，用 `Fetcher` 承载横切中间件，用 `Cache + EventEmitter` 驱动 React 更新，最后让业务组件只关心“当前 state 允许什么动作”。

---

## 追问防线

- 🛡️ **架构解耦防线（前端）**：前端如何处理兜底状态或无网环境 *(如果后端接口挂了或者没有返回 _links，前端页面是不是就彻底白屏不能用了？)*
- 🛡️ **状态流转防线（前端）**：链式 Follow 中间环节报错时前端如何捕获 *(client.follow().follow()，这中间异步如果断掉了，UI 交互怎么反馈给用户？)*
- 🛡️ **类型安全与契约防线（前端）**：动态链接如何保证 TypeScript 类型推导和代码提示 *(既然所有接口 URL 和 Payload 都是动态从 _links 读取的，前端如何保证调用时的类型安全和智能提示？)*
- 🛡️ **SDK 代码设计防线（前端）**：hateoas-ts 项目代码设计面试题 *(如果面试官追问这个 HATEOAS TS SDK 具体是怎么设计的，如何处理 Resource、StateFactory、Fetcher、Cache、React Hooks？)*
- 🛡️ **领域模型与超媒体组装防线（后端）**：后端如何高性能组装超媒体动作并校验状态机 *(后端在返回每一条资源时都需要实时计算当前用户和状态下的所有合法 _links，这会不会带来严重的 N+1 查询与鉴权性能瓶颈？)*
- 🛡️ **多级缓存与一致性防线（全栈）**：资源打散后如何设计多级缓存并保证一致性 *(资源被高度打散后请求量增加，你们的前后端多级缓存是如何设计并保证一致性的？)*

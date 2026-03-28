---
tags:
  - frontend-interview
  - hateoas
  - project
  - team-ai
  - 前端面试系列
created: 2026-03-24
date: 2026-03-24 09:35:01
updated: 2026-03-28 15:20:25
share: true
---
# HATEOAS 作为面试项目怎么讲

## 一句话定位

不要把这个项目讲成“我用了 HATEOAS”。

更好的讲法是：

> 我在一个多消费端项目里，解决了前后端 URL 耦合、动作发现、接口演进成本高的问题。HATEOAS 是我选的实现手段，而不是最终目的。

---

## 面试里怎么给这个项目定性

### 适合的岗位

- 前端高级工程师
- 前端架构方向
- BFF / API 协作型前端
- Agentic UI / AI 应用前端

### 不要错误定性

不要讲成：

- “后端返回了几个 `_links`，这就是 HATEOAS”
- “这比普通 REST 更高级”
- “Swagger 不重要，HATEOAS 就够了”

这种讲法很容易让面试官觉得你在概念堆砌。

---

## 这个项目真正能讲的价值

### 1. 前后端解耦

前端不再手写接口路径，也不依赖页面代码里拼 URL，而是通过资源关系导航。

例如不是写：

```ts
fetch(`/api/users/${id}/projects`)
```

而是写：

```ts
resource.follow('projects')
```

这样后端只要保证关系语义稳定，路径结构就可以演进，前端修改面更小。

### 2. 动作可以被发现，而不是写死

这个项目不只是返回数据，还返回 HAL-FORMS `_templates`，让前端或 AI agent 能发现“这个资源能做什么”。

例如：

- 当前资源能不能更新
- 用什么方法提交
- 提交目标是什么
- 表单字段有哪些
- 哪些字段必填

这让前端表单和动作层可以做更强的通用化。

### 3. 前端把 HATEOAS 真正消费起来了

这个项目不是后端自嗨式 HATEOAS。

前端有独立的 `@hateoas-ts/resource` 和 `@hateoas-ts/resource-react`：

- 资源对象支持 `follow(rel)`
- 支持延迟关系解析
- 支持缓存
- 支持请求去重
- 支持分页关系 `next`
- React 层封装了 `useResource`、`useInfiniteCollection`

所以它已经形成了消费闭环。

### 4. 很适合 AI / Agent 场景

普通 REST 更适合人写代码时查文档。

HATEOAS + HAL-FORMS 更适合：

- AI agent 发现可执行动作
- 自动构造请求
- 前端根据资源动态渲染能力

这也是这个项目相比普通 CRUD 更有辨识度的地方。

---

## 结合 Team AI 项目，面试时应该讲什么

### 后端层

后端资源不仅返回业务数据，也会返回：

- `_links`
- `_embedded`
- `_templates`

例如用户资源会暴露：

- `accounts`
- `projects`
- `default-project`
- `update-user`

这意味着客户端不只是拿数据，还可以发现关系和动作。

### 前端层

前端通过资源客户端消费这些关系：

- `follow(rel)` 做语义导航
- `useResource` 获取单资源
- `useInfiniteCollection` 基于 `next` 做分页
- breadcrumb / sidebar 也可以跟资源关系走

这比“接口文档 + axios + 手写 hooks”更可演进，但实现复杂度也更高。

### 工程层

这个项目还有一个很适合面试表达的点：

> 我不是只在后端加了一层 HATEOAS，而是把它抽象成了前后端共享的资源导航契约，并封装成独立的 TypeScript client 和 React hook 体系。

这句话很重要，因为它体现的是设计能力，不只是 API 风格偏好。

---

## 推荐的话术结构

### 版本一：1 分钟

> 我在 Team AI 里做的不是普通 REST CRUD，而是一套可发现的资源式 API。后端资源除了数据，还会返回关系链接和动作模板；前端不拼 URL，而是通过 `follow(rel)` 做类型化导航。这样分页、表单动作、面包屑这些 UI 能力都可以基于资源关系通用化，也更适合 Web 和 AI agent 共用一套 API。它的好处是降低耦合、提升接口演进能力，代价是实现复杂度更高，所以我只在核心资源上使用，而不是全站泛化。

### 版本二：2 到 3 分钟

可以按这个顺序讲：

1. 先讲问题  
   我们的项目不只有一个前端页面在消费 API，还希望让不同客户端和 AI agent 都能使用同一套能力。如果前端大量手写 URL、手写动作和表单，接口一变就很脆。

2. 再讲方案  
   所以后端返回 HAL/HAL-FORMS 资源，除了数据外还提供关系和动作模板。前端封装成资源客户端，通过 `follow(rel)` 做导航，不再手工拼路径。

3. 再讲落地  
   我们不仅做了后端资源模型，还做了 TypeScript HATEOAS Client、React Hooks、分页关系消费、动作模板解析，所以这不是概念验证，而是一条完整链路。

4. 最后讲 tradeoff  
   这种设计对简单后台系统可能过重，但对于多消费端、能力可发现、接口演进频繁的场景很合适。

---

## 简历 bullet 可直接使用

- 设计并实现基于 HAL/HAL-FORMS 的可发现 REST API，支持资源导航、嵌入资源与动作模板。
- 封装 TypeScript HATEOAS Client 与 React Hooks，支持类型安全 `follow(rel)`、缓存、请求去重和分页导航。
- 将资源模板解析为通用动作/表单模型，减少前端对 URL 和接口细节的硬编码依赖。
- 让 Web 与 AI agent 共用一套资源契约，提升接口演进能力与多端复用效率。

---

## 面试官如果追问“你具体做了什么”

可以从下面几个点里选 2 到 3 个展开：

### 我做了资源导航抽象

我把资源访问抽象成 `Resource` 和 `ResourceRelation`，让前端按语义关系导航，而不是依赖路径结构。

### 我做了前端消费层

我封装了 React Hooks，让单资源、分页集合、Suspense 读取都可以复用这套资源语义。

### 我做了动作模板解析

我把 HAL-FORMS 的 `_templates` 解析成前端通用表单定义，用于构建动作和校验能力。

### 我做了工程能力而不是单点页面

我不是在某一个页面里硬编码接口，而是做成可以复用的 client / hook / form schema 体系。

---

## 项目里的证据点

如果面试里需要给出更具体的实现证据，可以提这些文件：

- `packages/resource/src/lib/resource/resource.ts`
- `packages/resource/src/lib/resource/resource-relation.ts`
- `packages/resource/src/lib/state/hal-state/parse-hal-templates.ts`
- `packages/resource-react/src/lib/hooks/use-resource.ts`
- `packages/resource-react/src/lib/hooks/use-infinite-collection.ts`
- `libs/backend/api/src/main/java/reengineering/ddd/teamai/api/representation/UserModel.java`

---

## 不要主动展开的风险点

- 不要上来就讲 Richardson Maturity Model
- 不要把 HATEOAS 说成银弹
- 不要说它一定优于普通 REST
- 不要忽略复杂度和团队学习成本

更稳妥的说法是：

> 这是一个针对多消费端、可发现动作、接口频繁演进场景的工程化取舍。

---

## 最后结论

这个项目最适合的包装方式不是“我会 HATEOAS”，而是：

> 我把前后端通信从“基于路径的接口调用”，升级成了“基于语义关系的资源导航和动作发现”，并且前端真正把这套模型消费起来了。

这句话比单讲 HATEOAS 更像成熟工程师的话。



## 按项目经历风格优化后的写法

### 项目名称

HATEOAS 请求管理

### 项目简介

面向多消费端场景设计的 HATEOAS 请求管理库，用于高效消费基于 HAL / HAL-FORMS 的 RESTful API。通过后端返回的 link、method 与 template 驱动前端请求、动作发现与表单渲染，避免前端硬编码 URL、payload interface 以及权限判断逻辑，提升接口演进能力与多端复用效率。

### 工作内容与成果

☻ 主导 HATEOAS 资源模型与 TypeScript SDK 设计，抽象 Resource、Relation、Template 等核心对象，支持按语义关系 `follow(rel)` 导航，而非在页面层手写 URL

☻ 主导链式请求与延迟关系解析机制实现，只需持续 follow 后端返回的 link，即可逐步获取关联资源，降低前端与接口路径结构的耦合

☻ 主导 HAL-FORMS 动作模板解析与通用表单 schema 转换，避免前端硬编码 payload interface、method 与字段约束，提升动作和表单能力的可配置性

☻ 实现缓存、请求去重、分页关系消费等基础能力，统一资源访问过程中的状态管理与性能策略，减少前端样板代码

☻ 统一不同客户端的权限与动作发现逻辑，让“当前资源能做什么”更多由服务端声明驱动，减少前端分散判断和权限漂移问题

☻ 支撑 Web 与 AI Agent 共用一套资源契约，为资源导航、动态表单和 Agentic UI 场景提供基础能力

### 一段简历压缩版

设计并实现基于 HAL / HAL-FORMS 的 HATEOAS 请求管理库，抽象 Resource / Relation / Template 等核心模型，支持按语义关系 `follow(rel)` 链式导航、动作模板解析、分页消费、缓存与请求去重。通过服务端声明驱动前端请求、表单与权限发现，减少 URL、payload interface 和动作逻辑的硬编码，提升多端复用与接口演进能力。

### 更像你当前简历风格的三条式写法

- 主导 HATEOAS 请求管理库设计与实现，支持基于 link / method / template 的资源导航与动作发现，降低前端对 URL 和接口结构的硬编码依赖。
- 封装链式 follow 调用、动作模板解析、分页关系消费、缓存与请求去重能力，减少页面层样板代码并提升资源访问一致性。
- 统一 Web 与其他客户端的权限和动作发现逻辑，为动态表单、资源驱动 UI 和 AI Agent 消费同一套 API 契约提供支撑。


### Boss / 猎聘项目经历描述

负责设计并实现面向多消费端场景的 HATEOAS 请求管理库，基于 HAL / HAL-FORMS 统一前端对资源导航、动作发现、动态表单和分页关系的消费方式。通过 `follow(rel)` 链式关系导航、模板解析、缓存与请求去重机制，减少 URL、payload interface 和权限逻辑的硬编码，提升接口演进能力、多端复用效率以及 AI Agent 场景下的资源消费一致性。

### Boss / 猎聘三条式写法

- 主导 HATEOAS 请求管理库建设，基于 HAL / HAL-FORMS 统一资源导航、动作发现与动态表单消费模式。
- 封装 `follow(rel)` 链式调用、模板解析、分页关系消费、缓存与请求去重能力，显著减少前端样板代码和硬编码接口逻辑。
- 支撑 Web 与 AI Agent 共用同一套资源契约，提升多端一致性与接口演进效率。

## 关联逐字稿

- [[./Team AI 15 分钟逐字稿（完整版）|Team AI 15 分钟逐字稿（完整版）]]



## 一个很具体的落地例子：layout prefer

如果面试官觉得 `follow(rel)` 还是有点抽象，我会补一个很接地气的例子：我们连页面壳层都在按资源关系拿。

比如前端在拉项目页、图页这类主资源时，会额外带一个 `Prefer: layout=sidebar, layout=breadcrumb`。这个意思不是让后端替前端换模板，而是告诉后端：这次请求是给工作台布局用的，你顺手把侧边栏和面包屑相关的导航资源也一起带回来。

这样后端就会把 `_links.sidebar`、`_embedded.sidebar`、`_links.breadcrumb`、`_embedded.breadcrumb` 一起返回。前端收到后，不是自己拼导航，也不是每个页面再单独查一遍菜单，而是直接按资源关系去渲染 sidebar 和 breadcrumb。

而且它还是按需的。没带这个 Prefer，后端就不会把这些布局信息塞进响应里，所以普通 API 调用不会平白多一坨导航数据。这个点在面试里其实很好用，因为它能说明我不是在堆概念，而是在做有边界的工程取舍。

如果我要收一句，我会说：这个项目里 HATEOAS 不是只拿来做列表跳详情，连页面壳层导航都一起资源化了。


## 再补一句更像工程取舍的话：breadcrumb 也是渐进增强

如果面试官继续追问，既然后端会返回 breadcrumb，是不是就要等主资源回来之后才能渲染导航，我会补一句：我不会把 breadcrumb 完全绑定到主内容请求完成之后才出现。

因为 breadcrumb 属于 layout shell，不属于主内容本体。更好的做法是先基于当前 pathname 渲染一个同步 fallback breadcrumb，保证用户切路由后立刻知道自己到了哪里、页面在加载什么、还能不能返回上一级；然后等带 Prefer: layout=breadcrumb 的资源响应回来，再用后端给出的真实业务名称覆盖。

这样既保留了 HATEOAS 的优势：项目名、实体名、可跳转关系都由资源声明；也保留了渐进增强的体验：壳层先稳定出现，再逐步增强为更准确的导航。换句话说，资源驱动不等于所有东西都要一起阻塞，layout shell 和主内容应该分层加载。
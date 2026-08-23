---
title: 简历回答逐字稿：HATEOAS TypeScript SDK 与类型安全约束
date: 2026-07-03 22:30:00
updated: 2026-08-23 08:51:38
tags:
  - interview/script
  - resume/hateoas
  - typescript
---

# 简历回答逐字稿：HATEOAS TypeScript SDK 与类型安全约束

关联：[[职业经历]]、[[全栈工程师简历]]、[[简历追问：HATEOAS TypeScript SDK 与类型安全约束]]、[[15分钟：HATEOAS 资源契约架构]]。

> [!warning] 回答边界
>
> - SDK、类型约束、zod 校验、缓存和 React Hooks 属于个人直接实现。
> - 服务端资源表达由我设计契约并与后端共同落地，服务端代码不是个人实现。
> - 真实资源是应用、表单、工作流和工作区导航；下文代码只用于解释机制。

## 30 秒开场

我做这个 SDK 时，目标不是再封一层 Axios，而是把 HATEOAS 的资源状态机消费方式固化下来。业务代码不应该到处拼 URL，也不应该每个页面都自己解析 `_links` 和 `_templates`。

所以我把 SDK 抽成几个核心概念：`Client` 负责入口和中间件，`Resource` 代表一个 URI 级资源实例，`State` 代表资源当前数据和 links，`follow()` 负责沿 relation 导航，`action()` 负责按后端模板提交动作。TypeScript 主要约束稳定的 relation 和 payload 形状，运行时再用 zod 做契约校验。

## 如果面试官问：为什么 SDK 设计会倒逼模型和接口设计？

因为 TypeScript 只能约束稳定的业务 relation。如果服务端资源边界和生命周期不清楚，relation 名称就会随着页面和接口路径变化，SDK 再强类型也只是把不稳定结构写进类型系统。

在 SDK 落地过程中，我逐渐把问题从“前端怎样调用接口”向上追到“资源是什么、聚合关系是什么、动作为什么合法”。因此后续参与四色建模和 RESTful API 设计，再把稳定资源关系落实回 SDK 类型、`follow()` 和 `action()`。这条演进仍然以客户端可维护性为目标，不代表服务端实现都由我完成。

## 如果面试官问：它和 Axios + React Query 有什么区别？

我会说 Axios 解决的是请求发送，React Query 解决的是服务端状态缓存，但它们不负责理解“资源关系”。

在 HATEOAS 下，业务代码关心的是：从当前资源能不能 follow 到某个 relation，当前 action 能不能执行，payload 是否符合当前模板。这些能力如果每个业务页面自己写，就会重新散掉。

所以 SDK 的抽象更像资源客户端：

```ts
const application = client.go<ApplicationEntity>("/applications/app-1")
const state = await application.get()

if (state.hasLink("publish")) {
  await state.action("publish").submit(payload)
}
```

这里真正重要的是 `publish` 这个业务 relation，而不是某个写死的发布接口路径。代码是机制示意，不代表生产接口的完整字段。

## 如果面试官追：动态 links 怎么做 TypeScript 类型安全？

我会先承认这里有天然矛盾：HATEOAS 是运行时动态返回，TypeScript 是开发期静态检查。所以我的策略不是假装所有东西都能静态化，而是分两层。

第一层，把稳定的业务 relation 显式建模到类型里，比如：

```ts
type ApplicationLinks = {
  publish: ActionRelation<PublishPayload, ApplicationState>
  revoke: ActionRelation<RevokePayload, ApplicationState>
  workflow: ResourceRelation<WorkflowEntity>
}
```

这样业务代码写 `state.follow('not-exist')` 在开发期就能报错。第二层，运行时仍然要检查后端这次有没有真的返回这个 relation。如果类型里有 `publish`，但当前状态下后端没有返回，SDK 不能硬调接口，而是返回 action missing 的标准错误或让 `hasLink('publish')` 为 false。

所以类型解决“你写的 relation 名是不是系统认可的”，运行时校验解决“当前资源状态下这个 relation 是否真的可用”。

## 如果面试官追：payload 类型从哪里来？

我会先讲项目里的实际做法：对稳定的 relation、action 和 payload 显式定义 TypeScript 类型，并用 zod 做运行时校验，再通过契约测试检查前后端对 `_links`、`_templates` 和 payload 的理解是否一致。

从 OpenAPI 或 JSON Schema 自动生成类型是这个 HATEOAS SDK 的可演进方向，但该项目没有完成自动生成，不能把后续协同建模平台中“AI 生成 OpenAPI 草稿”的能力倒算成这里的生产事实。运行时提交时，SDK 仍不能只相信前端类型；校验失败要返回字段路径和错误信息，而不是只抛字符串。

## 如果面试官追：缓存和 React Hook 怎么处理？

我会这样说：

SDK 内部会按绝对 URI 复用 `Resource` 实例。这样同一个资源在客户端只有一个事件源，方便做请求去重、缓存更新和订阅通知。

`resource.get()` 会先查缓存，如果缓存可用就返回；如果 stale 或缺失，再走 fetcher。请求回来后由 StateFactory 解析成统一 State，写回 cache，然后发出 update 事件。React 层的 `useResource()` 只是薄适配：订阅 resource 的 update/stale/delete 事件，驱动组件刷新。

动作提交成功后，不一定粗暴全量刷新。简单场景可以用响应的新 State 覆盖当前资源；复杂场景会把相关 collection 标记 stale，让下次进入时重新拉。这个策略要跟业务一致性要求有关。

## 如果面试官追：zod 校验失败怎么反馈？

我会说这类错误不能只给开发者看，也要能被 UI 消费。

下面用缺少必填字段做机制示例，实际错误结构以项目实现为准：

```ts
{
  type: 'PayloadValidationError',
  action: 'reject',
  fields: [
    { path: ['comment'], code: 'required', message: '请输入驳回原因' }
  ]
}
```

表单层就可以把它映射到字段错误；监控层也可以记录是哪一个 action 的契约不匹配。

## 收尾句

所以这套 SDK 的价值不在于封装 HTTP，而在于把“资源、关系、动作、模板、缓存、运行时校验”变成一套统一消费模型，让业务页面少写状态机和路径字符串。它也是我从复杂前端和多端一致性出发，进一步理解资源建模与 RESTful API 的关键转折点。

---
title: 简历追问：HATEOAS TypeScript SDK 与类型安全约束
date: 2026-07-03 22:00:00
updated: 2026-10-03 13:11:10
tags:
  - interview/follow-up
  - resume/hateoas
  - typescript
---

# 简历追问：HATEOAS TypeScript SDK 与类型安全约束

关联：[[项目介绍：HATEOAS 资源契约架构]]。

## 对应简历描述

> 设计基于 relation 图谱遍历的 TypeScript 客户端 SDK，封装 `follow()` 与 `action()` 等能力，并结合泛型约束与运行时校验，尽量让 relation、action 与 payload 在开发期可提示、运行期可被 zod 统一验证。

## 面试官真正想确认

你是否理解“动态超媒体”和“静态类型系统”之间的矛盾，而不是把 SDK 做成普通 `request.get('/xxx')` 封装。

## 连续追问链

### 1. SDK 边界

- SDK 为什么要单独做？直接用 Axios + React Query 不够吗？
- 为什么 relation 的类型稳定性依赖资源边界、生命周期和 RESTful API 语义？
- SDK 落地怎样推动你从多端消费继续理解业务／领域建模，而不是单纯扩大后端技术栈？
- `core` 包和 `react` 适配包怎么拆？哪些能力必须框架无关？
- `Resource`、`State`、`Action`、`Fetcher`、`Cache` 之间的调用链是什么？

### 2. 类型安全

- `Entity<TData, TLinks>` 里的 `TLinks` 怎么约束 `follow('xxx')` 的可选 relation？
- 不存在的 relation 是在 TypeScript 编译时报错，还是运行时报错？两者边界怎么划？
- 动态后端返回的 relation，如何和前端静态类型声明保持一致？靠代码生成、手写类型，还是契约测试？
- `action('approve').submit(payload)` 的 payload 类型从哪里来？模板字段如何映射成 TS 类型？

### 3. 运行时校验

- 既然 TypeScript 只在开发期有效，运行时为什么还要 zod？
- 如果后端返回 payload schema 和前端类型不一致，SDK 是 fail fast、降级，还是给 UI 返回契约错误？
- zod 校验失败的错误对象如何让业务组件可理解，而不是只抛一串技术异常？

### 4. 状态、缓存与 React

- 同一个 URI 的资源实例如何复用？为什么不能每次 `follow()` 都 new 一个独立对象？
- `action()` 成功后如何刷新缓存？只更新当前资源，还是级联标记 stale？
- React Hook 如何处理请求去重、组件卸载、AbortController、Suspense 或 loading 状态？

## 现场代码题

> 请设计一个最小 API，让 `user.follow('posts').get()` 能推导出 posts 的数据类型，同时 `user.follow('not-exist')` 在 TS 层报错。

继续追：如果服务端运行时没有返回 `posts` relation，但 TS 类型里有，SDK 应该怎么表现？

## 准备证据

- SDK 核心接口签名或伪代码。
- 一个 relation 类型推导示例。
- 一个 zod 校验失败的错误样例。
- 一个 action 后缓存失效和 React 组件刷新的流程图。

## 面试注意事项

- 讲清编译期静态类型推导与运行时 Schema 校验结合的双重防护机制。
- 解释对后端动态下发 HAL/HAL-FORMS 结构的契约解析与安全兜底。
- 说明 SDK 封装了资源导航、状态机驱动与联动缓存失效，超越简单的请求封装。
- 强调类型安全必须建立在上游严谨的 RESTful 资源建模之上。

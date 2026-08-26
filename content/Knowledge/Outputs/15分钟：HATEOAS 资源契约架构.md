---
title: 15分钟：HATEOAS 资源契约架构
date: 2026-04-21 15:58:29
updated: 2026-08-24 16:57:29
tags:
  - interview
  - architecture
  - hateoas
  - frontend
  - typescript
---

# 15分钟：HATEOAS 资源契约架构

> [!warning] 事实边界
>
> - 真实资源是应用、表单、工作流和工作区导航，客户端是 PC Web 与移动 Web；审批单、订单等只用于解释机制。
> - 本人负责业务／领域模型、RESTful / HATEOAS 契约、TypeScript SDK 和 React 消费层；服务端代码由后端同事实现。
> - 动态 Agent 工具、离线 mutation 队列、disabled reason 和后端性能优化方案属于架构延展，不说成已上线成果。

> [!tip] 使用方式
> 默认先说 2 分钟版。面试官继续追问时，再从 5 分钟主讲法或文末具体回答中选择一条展开；不要连续背满 15 分钟。

## 30 秒开场

这个项目最早解决的是 PC Web 和移动 Web 重复维护状态、角色和权限规则的问题。我把“当前资源能访问什么、能执行什么动作”收敛到服务端返回的 `_links` 和 `_templates`，再用 TypeScript SDK 统一消费。做下去以后我发现，稳定的 relation 依赖清楚的资源边界和生命周期，所以又继续参与了业务建模和 RESTful API 设计。

## 2 分钟项目介绍

低代码平台里的应用、表单、工作流和工作区导航同时服务 PC Web 与移动 Web。过去后端返回 `status`，各端再根据角色和权限判断按钮、导航和提交字段。规则一变，几个端都要修改，很容易出现一边有动作、另一边没有的情况。

我先推动 HATEOAS 资源动作契约。服务端在资源里返回 `_links` 和 `_templates`：relation 表达当前可以导航到哪里或执行什么动作，template 描述提交方式和字段约束。前端只消费 `publish`、`revoke` 这类业务 relation，不再复制一份状态机。

为了让几个端稳定使用这套契约，我设计并实现了 TypeScript SDK。`Client` 管理入口和中间件，`Resource` 表示 URI 级资源，`follow()` 沿 relation 导航，`action()` 按 HAL-FORMS 模板提交；资源缓存和更新事件再驱动 React Hooks。稳定 relation 在 TypeScript 中建模，运行时数据仍通过 Standard Schema 和 Zod 校验。

SDK 落地后也暴露出上游问题：如果资源边界和动作语义本身混乱，SDK 只能统一调用方式。所以我继续从应用、表单和工作流的生命周期出发参与四色建模、RESTful URI 和动作契约设计，再与后端共同落到 API 表达层。服务端代码由后端同事实现。

生产阶段的通用能力后来被我拆成 `@hateoas-ts/resource` 和 `@hateoas-ts/resource-react` 两个公开 npm 包。当前可以确认的是多端消费、SDK、测试和公开发布，不补写下载量或效率比例。

## 5 分钟主讲法

### 1. 多端规则为什么会漂移

当时 PC Web 和移动 Web 都要根据 `status`、`role`、`permission` 判断导航、按钮和表单动作。后端调整状态流转或权限规则以后，多个前端要分别修改和回归。继续封装 API Service 只能整理代码，解决不了业务规则在几个端重复解释的问题。

我希望把业务合法性的权威来源放回服务端资源表达，让前端专注交互呈现。

### 2. 为什么选择 HATEOAS

我考虑过把判断收敛成前端配置表，也考虑过单独增加权限接口。前者仍然由前端解释后端状态，后者又把权限、URL、Method 和 payload 规则拆散了。

最后采用 HATEOAS：`_links` 表达资源导航和动作入口，`_templates` 表达动作的 Method、Content-Type 和字段约束。当前资源没有返回 `publish`，前端就不开放发布；返回以后，SDK 按模板提交。relation 是业务语义，不是按钮名称，因此 PC 和移动端可以采用不同交互，但消费同一动作事实。

### 3. 契约为什么会倒逼模型和 API

刚开始我关注的是多端怎么消费。真正设计 relation 时，必须先回答资源是什么、生命周期怎样、当前角色在哪个状态下可以做什么。如果这些问题不清楚，`_links` 最后还是会退化成按钮数组。

所以我从应用、表单、工作流和工作区导航的业务事件出发，参与四色建模，识别资源和聚合边界，再设计 RESTful URI、relation 与动作契约。服务端 API 表达由我和后端共同落地，后端代码不算个人实现。

### 4. SDK 怎样把契约交给前端

SDK 不是 Axios 的再封装。`Client` 负责入口和中间件，`Resource` 按绝对 URI 复用实例，`StateFactory` 把 HAL、HAL-FORMS 等响应解析成统一 State，`Cache` 与事件通知负责状态更新。

业务代码通过 `follow()` 沿 relation 导航，通过 `action()` 提交动作，不需要到处拼 URL。稳定 relation 可以进入 TypeScript 类型；但后端是否在当前状态返回 relation 仍是运行时事实，所以 SDK 还要检查 `hasLink()`，并用 Standard Schema 或 Zod 校验 payload。React Hooks 只订阅资源状态，不重新判断业务合法性。

### 5. 结果和边界

生产阶段，应用、表单、工作流和导航由 PC 与移动端消费同一资源动作契约。后端调整可访问页面或合法动作后，前端不再分别维护对应判断。测试重点也可以从多个端重复回归按钮规则，收敛到契约矩阵和消费层行为。

后来我把通用消费模型独立成两个 npm 包并持续维护。它们可以证明 SDK、测试和发布能力，但不能反推生产项目规模，也不能派生外部采用和商业收益。

动态 Agent 工具、完整离线队列、disabled reason 和服务端 N+1 优化都属于后续讨论。当前项目可以确认的是模型、契约、SDK、React 消费和多端落地。

## 深挖入口

- 契约如何从多端问题走向模型与 API：[[简历回答逐字稿：HATEOAS 资源动作契约消费层设计]]
- SDK、类型与运行时校验：[[简历回答逐字稿：HATEOAS TypeScript SDK 与类型安全约束]]
- 缓存、错误和弱网边界：[[简历回答逐字稿：HATEOAS 兜底状态与错误标准化处理]]
- Agent 作为新客户端的架构延展：[[简历回答逐字稿：HATEOAS Agent 友好与权责对等]]

## 收尾句

这段经历让我从前端多端一致性出发，先做统一消费，再继续追到资源模型和 API 契约。HATEOAS 让几个客户端消费同一份“当前资源能做什么”的业务事实，少写 URL 只是随之带来的结果。

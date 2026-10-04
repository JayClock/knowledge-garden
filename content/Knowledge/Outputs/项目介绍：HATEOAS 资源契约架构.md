---
title: 项目介绍：HATEOAS 资源契约架构
date: 2026-04-21 15:58:29
updated: 2026-10-04 17:40:26
tags:
  - interview
  - architecture
  - hateoas
  - frontend
  - typescript
---

# 项目介绍：HATEOAS 资源契约架构

## 提取词

多端状态漂移 ｜ 超媒体动作契约 ｜ 四色建模倒逼资源设计 ｜ TS SDK 状态工厂与 Standard Schema ｜ 渐进试点与开源交付

## 2 分钟版本

当时我们在做低代码平台，里面的应用、表单和工作流同时服务 PC Web 与移动端。过去后端只返回简单的状态码，两端的前端各自写判断代码，根据状态码、角色和权限字典决定按钮和导航。规则一变两端都要修改，很容易出现一端能点、另一端漏改的不一致。

为了解决多端规则漂移，我推动引入了 HATEOAS 超媒体动作契约。服务端在资源中直接返回 `_links` 和 `_templates`：links 表达当前能跳到哪里或执行什么动作，template 描述提交方式与字段约束。前端只声明式消费 `publish` 这类业务 relation，不再复制一套状态机。

为了让多端稳定消费，我设计并实现了 TypeScript SDK。`Client` 管理入口和中间件，`Resource` 基于 URI 复用实例，`follow()` 沿 relation 导航，`action()` 按模板提交；稳定 relation 在 TypeScript 中建模，运行时数据接入 Standard Schema 和 Zod 校验，再由资源状态驱动 React Hooks。

实际推进中我也发现，如果后端资源边界本身混乱，SDK 只能统一调用。所以我继续从应用和工作流的生命周期出发，参与上游四色建模、RESTful URI 和动作契约设计，再与后端协同落地 API 表达层。项目从工作区导航试点切入逐步推广，并将通用消费层独立开源，沉淀了 233 项自动化测试。

## 5 分钟主讲

我先介绍一下这个项目的背景。当时我们在做低代码平台，里面的应用、表单和工作流需要同时跑在 PC Web 和移动端上。最早的做法是后端接口只返回简单的数字状态码，两端的前端各自在本地写一大堆判断，根据状态码、用户角色和权限字典，来决定页面上要不要展示发布按钮、撤回按钮或某个表单项。

这很快带来了**多端规则漂移**：后端业务状态或权限逻辑一旦调整，PC 端和移动端就得分别修改代码并重新回归，联调时经常出现“PC 端能点、移动端漏改”的不一致。在前端层层封装 API Service 只能规整代码，根本没解决业务合法性在客户端被重复解释的缺陷。

为了根治这个问题，我推动引入了 HATEOAS 超媒体动作契约。我没有去单独开一个权限接口，因为那会把 URL、请求方法、状态机和参数校验再次拆散。我采用的做法是：让服务端直接在业务资源中下发 `_links` 和 `_templates`。`_links` 用 relation 表达当前资源可以导航到哪里或执行什么动作；`_templates` 则明确声明该动作对应的 HTTP Method、提交字段与校验规则。

这样前端就不再需要知道后台复杂的状态码和角色组合了。前端只需要声明式地消费当前资源有没有下发 `publish` 这个 relation。有 relation 就渲染按钮；点击之后直接按模板规范提交。业务合法性的事实源收敛回服务端，前端回归到纯粹的交互呈现。

但在实际推进时，我发现最大的阻力其实在上游：如果后端的资源边界模糊、生命周期没有定义清楚，`_links` 最终就会退化成一组专门给前端画按钮的特定字符串，失去通用契约的价值。所以我意识到，前端不能只坐在链路末端被动接接口。我主动从应用、表单和工作流的生命周期切入，参与到上游的领域建模中。我们采用四色建模法，梳理了流转记录等时标性关键凭证，理清了核心聚合根与资源边界。

在接口设计上统一 RESTful URI 规范，将操作收敛为标准资源的生命周期流转。比如不设计形如 `/api/publishWorkflow` 这类 RPC 接口，而是建模为“发布版本”资源的创建或状态迁移，并在工作流资源中自然派生出 `publish` relation。服务端 API 表达由我和后端协同落地，真正让前后端在同一份业务语义契约下协作。

契约定义好后，为了让多端稳定消费，我设计并实现了配套的 TypeScript SDK。它不是简单的 Axios 封装，而是一个完整的资源状态消费层：底层架构上，`Client` 统一收拢入口与拦截器，`Resource` 基于绝对 URI 实现实例缓存与复用；`StateFactory` 屏蔽协议差异，将 HAL 与 HAL-FORMS 解析为统一的资源状态树。业务层通过 `follow()` 声明式导航，通过 `action()` 结合模板提交表单，彻底摆脱硬编码拼 URL。

在类型安全上我做了一层取舍：稳定 relation 在 TypeScript 中建模为字面量联合类型，提供完整的代码补全；但由于服务端是否在当前状态下发该 relation 是运行时事实，SDK 强制提供 `hasLink()` 防御判断，并接入 Standard Schema 与 Zod 校验提交数据。UI 层进一步封装 React Hooks，组件只需订阅资源状态变化。

在落地路径上，我们采取渐进式推进策略：先以低风险的工作区全局导航和页面路由做试点，验证跑通后，再逐步推广到表单和工作流主链路，过渡期保留了传统 RESTful 的兼容降级通道。契约统一后，业务调整时前端不再需要维护状态机，测试回归也从每个端逐一验证按钮显隐，收敛为契约矩阵与消费层测试。

为了沉淀长期工程资产，我将这套通用消费模型独立抽象并开源为两个 npm 包（`@hateoas-ts/resource` 与 `@hateoas-ts/resource-react`），沉淀了 34 个测试套件、233 项自动化测试与完备的类型定义，至今保持独立维护。

这段经历让我从前端多端一致性出发，先建立契约消费层，再继续追到上游业务模型与接口契约。HATEOAS 让多个客户端消费同一份“当前资源能做什么”的运行时事实，少写 URL 只是随之带来的结果。

## 高频追问

### 如果面试官问：为什么一个前端问题最后会走向建模和 RESTful API？

因为 SDK 只能统一消费方式，不能把一个本身混乱的接口变稳定。真正设计 relation 时，我需要先回答资源是什么、生命周期如何变化、当前角色在什么状态下可以做什么。如果这些问题不清楚，`_links` 最后只会变成给前端画按钮的特定字符串，HATEOAS 也只是换一种形式复制混乱。

所以我的能力是从前端消费层逐步向上游延伸的：先解决 PC Web 与移动 Web 的多端规则漂移，再因为 relation 稳定性问题参与业务与领域建模，从应用、表单、工作流和工作区导航的业务事件中识别资源边界，最后设计 RESTful URI 与动作契约，并和后端共同落实到 API 表达层。

这条能力仍然服务于复杂前端：从上游稳定客户端要消费的业务知识。在具体落地中，我与后端团队分工协作：我主导领域模型、契约定义与客户端 SDK 研发，与后端协同完成 API 表达层对接。

### 如果面试官问：你具体怎么设计 `_links` 和 `_templates`？

`_links` 主要表达资源导航和动作入口，比如 `self`、`workflow`、`publish`、`revoke`；`_templates` 更偏动作提交契约，包含 HTTP Method、Content-Type 和 payload 字段约束。

我没有把它设计成“按钮数组”，因为按钮只是 UI 表现，真正稳定的是业务 relation：同一个 `publish` 可以在 PC Web 渲染为右上角主按钮，在移动端做成底部操作条，但都消费同一份资源动作事实。

服务端返回的结构设计如下：

```json
{
  "id": "app-1",
  "status": "draft",
  "_links": {
    "self": { "href": "/applications/app-1" },
    "workflow": { "href": "/applications/app-1/workflow" }
  },
  "_templates": {
    "publish": {
      "method": "POST",
      "properties": [{ "name": "comment", "type": "string", "required": false }]
    }
  }
}
```

前端看到 `publish` 就知道当前上下文允许发布，但为什么允许仍由后端状态、角色和权限规则决定。业务合法性的事实源收敛回服务端，前端回归到纯粹的交互呈现。

### 如果面试官追：没有返回某个动作，前端是隐藏还是禁用？

这类情况不能让业务页面自己猜，需要由统一策略处理。

动作缺失可能表示当前状态不可执行、当前用户无权限或契约尚未就绪。UI 呈现可以根据产品交互需要决定：

- **非关键动作**：没有 relation 就直接不展示，减少页面视觉噪音。
- **关键高预期动作**（如审批页里的审批按钮）：展示禁用态，并由后端返回原因提示（如“当前状态不可审批”或“非当前审批人”）。

这里的核心架构原则是：**前端可以决定交互呈现，但绝不重新实现一份业务状态机**去推算为什么不能点。

### 如果面试官追：列表 100 条资源，每条都算动作，会不会很慢？

在与后端团队共同设计契约时，核心原则是避免在接口组装层按资源逐条查询权限，而是将动作计算与资源上下文、批量鉴权深度绑定，从架构层面规避 N+1 查询风险。

### 如果面试官问：SDK 和 Axios 与 React Query 有什么区别？

Axios 解决网络请求发送，React Query 解决服务端状态缓存，但它们都不负责理解“资源关系”。

在 HATEOAS 下，业务代码关心的是：从当前资源能不能 follow 到某个关联资源，当前 action 能不能执行，payload 是否符合当前模板约束。这些能力如果由每个业务页面自己写，多端逻辑又会重新分散。

SDK 提供了面向资源的消费抽象：

```ts
const application = client.go<ApplicationEntity>("/applications/app-1")
const state = await application.get()

if (state.hasLink("publish")) {
  await state.action("publish").submit({ comment: "发布上线" })
}
```

这里真正重要的是 `publish` 这个业务 relation，而不是某个写死的发布接口路径。SDK 把“资源定位、关系导航、模板校验、缓存复用”封装为连贯的消费层。

### 如果面试官追：动态 links 怎么做 TypeScript 类型安全？

这里有天然矛盾：HATEOAS 是服务端在运行时动态返回的，而 TypeScript 是编译期静态检查。

我的方案是分层处理：稳定的业务 relation 在 TypeScript 中显式建模为联合类型：

```ts
type ApplicationLinks = {
  publish: ActionRelation<PublishPayload, ApplicationState>
  revoke: ActionRelation<RevokePayload, ApplicationState>
  workflow: ResourceRelation<WorkflowEntity>
}
```

这样业务代码写 `state.follow('not-exist')` 在开发期就能立即获得类型报错和 IDE 代码补全。

到了运行时，SDK 必须做防御性检查：即使类型里声明了 `publish`，但如果当前状态下服务端因为权限或状态机未下发该 link，SDK 强制通过 `hasLink('publish')` 返回 false，并在直接调用不存在的 action 时抛出明确的 `ActionMissingError`。编译期类型保证 relation 名称正确，运行时校验确认当前资源状态可用。

### 如果面试官追：payload 类型从哪里来，运行时如何校验？

对稳定的 relation、action 和 payload，我们在端侧定义明确的 TypeScript Interface 与 Zod Schema。

在执行 `action.submit(payload)` 时，SDK 接入 Standard Schema 规范，在端侧通过 Zod 执行运行时同步校验。如果校验失败，直接在本地拦截请求并返回精准的字段错误（包含 `path`、`code` 和 `message`），直接驱动表单字段高亮报错，避免无效网络请求冲击后端。

### 如果面试官追：资源缓存和 React Hooks 怎么处理？

SDK 内部基于绝对 URI 实现 `Resource` 实例的单例缓存与复用。同一个 URI 在客户端只有一个事件源，天然实现请求去重与并发合并。

`resource.get()` 优先读取内存缓存；若缓存过期或缺失，则走底层 Fetcher 拉取最新数据。响应返回后由 `StateFactory` 统一解析 HAL 与 HAL-FORMS，更新缓存并触发资源变更事件。

在上层 React 封装中，`useResource(uri)` 订阅该资源实例的 update 事件驱动组件重新渲染。动作提交成功后，支持直接用新返回的 State 局部更新当前资源实例，或将相关关联集合标记 stale，兼顾性能与数据最终一致性。

### 如果面试官问：_links 拿不到页面是不是就废了？

页面绝不能简单白屏。

如果初次请求资源本身失败，页面进入资源加载失败与网络重试状态。如果本地有缓存数据，但刷新时动作契约未拿到，系统将页面置为“基于缓存快照的只读模式”，暂时禁用关键提交动作，防止客户端在状态未同步时产生不可逆副作用。

同时在错误模型上建立标准化分级：区分 `NetworkError`、`Unauthorized`、`Forbidden`、`ActionMissing`、`PayloadValidationError` 与 `Conflict`，让 UI 呈现、监控报警和自动重试拥有统一清晰的决策依据。

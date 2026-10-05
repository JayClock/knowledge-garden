---
title: 项目介绍：HATEOAS 资源契约架构
date: 2026-04-21 15:58:29
updated: 2026-10-05 21:10:17
tags:
  - interview
  - architecture
  - hateoas
  - frontend
  - typescript
---

# 项目介绍：HATEOAS 资源契约架构

## 提取词

多端规则漂移 ｜ `_links` 与 `_templates` ｜ 独立资源消费层与协议适配 ｜ URI 复用与响应驱动缓存 ｜ 模板驱动校验与动态表单 ｜ 上游资源建模 ｜ 增量改造边界与回归验证 ｜ 工作区导航试点与开源交付

## 2 分钟版本

当时我们在做低代码平台，应用、表单和工作流同时服务 PC 端与移动端。两端 UI 可以不同，但同一用户面对同一资源，能访问的页面和执行的操作需要一致。过去后端返回数据、状态码和权限信息，多端各自组合规则；即使抽成公共模块，客户端仍要维护一份与服务端并行的推导逻辑，规则变化时两端都要调整。

我推动引入 HATEOAS 超媒体动作契约，把“当前资源能做什么”的决策收敛回服务端。资源中通过 `_links` 表达关系与入口，通过 `_templates` 描述提交方法和字段约束。前端消费 `publish` 这类稳定的 relation，而不是各自推导业务状态机。

我设计并实现了独立的 TypeScript SDK 和 React Hooks，把导航、提交和资源复用统一到消费层。业务通过 `follow()` 导航，通过 `action()` 按模板提交。TypeScript 约束稳定的 relation 与资源类型；当前动作是否可用由运行时契约判断，字段再通过 Standard Schema 与 Zod 校验。

但 SDK 能统一消费，不能替团队确定资源边界和生命周期。所以我继续参与上游建模和 RESTful API 设计，与后端共同落地契约。我们先在低风险的工作区导航试点，再推广到表单和工作流。在既有消费能力覆盖下，客户端直接消费服务端更新的关系和动作；通用消费层随后沉淀为两个独立 npm 包。

## 5 分钟主讲

这个项目来自低代码平台的多端一致性问题。应用、表单和工作流同时服务 PC Web 与移动端，两端 UI 可以不同，但同一用户面对同一资源，能访问的页面和执行的动作需要一致。过去后端返回数据、状态码和权限信息，多端自己组合规则。抽公共模块能减少重复代码，却仍在客户端保留了一套与服务端并行的推导逻辑；规则变化时，多端要同步修改和回归。

我推动引入 HATEOAS，由服务端根据资源生命周期和用户上下文下发契约。`_links` 表达资源关系与入口，`_templates` 描述提交方法、字段和约束。页面消费 `publish` 这样的业务 relation：有当前入口就呈现相应操作，再按模板提交。服务端负责决定当前能做什么，多端负责交互呈现与契约消费。

推进时，我发现 SDK 可以统一消费，但不能替团队决定资源模型。如果边界与生命周期不清，relation 就容易成为临时的按钮名称。我从应用、表单和工作流的业务事件切入，用四色建模澄清关系和状态约束，再与后端共同设计 RESTful URI 与动作契约。

以工作流发布为原理示例，假设发布创建新版本，就要先明确草稿和发布版本的边界、发布前后的状态、成功后返回什么资源，再设计 `publish` 和提交模板。我负责模型与契约设计、客户端研发，与后端协同落地 API 表达层。

SDK 是独立的资源消费层：`Fetcher` 处理请求，Client 按 `Content-Type` 选择 `StateFactory`，将业务数据、关系与模板整理为统一 State；`Resource` 按绝对 URI 定位与复用。业务通过 `follow()` 导航、通过 `action()` 按模板提交。实例复用与数据缓存分开处理：`get()` 优先读取已有完整缓存，需要新数据时用 `refresh()` 主动刷新，相同进行中的请求由 SDK 去重。

类型安全上，TypeScript 约束稳定的 relation、资源数据和目标类型，当前入口通过 `hasLink()` 判断。字段来自 `_templates.properties`，生成 Zod 规则，经 Standard Schema 做运行时校验。业务页面也已接入动态表单，根据模板生成 JSON Schema 渲染字段，React Hooks 订阅资源状态。字段变化在既有渲染、校验和提交能力覆盖内时，可以直接消费新模板；需要新控件或特殊交互时，再调整前端。

落地时，我们先以工作区导航试点，在工作区响应中增加 `_links` 和 `_templates`，PC 与移动端改为 SDK 消费，按 `workflow` relation 渲染入口。MSW 模拟 relation 有无，Vitest 渲染导航组件并断言 DOM。随后推广到表单和工作流，保留 BFF 作为迁移退路。

推进的难点是证明后端增量改造的成本和数据风险可控。我与后端明确本次不改库表和原有请求参数，原保存接口响应保持不变，再用 AI 辅助生成 workflow 保存、发布的端到端测试做回归。保存用例以相同输入对比原有响应，检查已覆盖保存场景的输入输出兼容性。

后来我将通用消费模型独立为两个 npm 包：`@hateoas-ts/resource` 和 `@hateoas-ts/resource-react`，公开仓库有 34 个测试文件、233 项通过的自动化测试。这段经历让我从多端一致性出发，先建立消费层，再继续追到上游业务模型与接口契约。

## 高频追问

### 如果面试官问：为什么一个前端问题最后会走向建模和 RESTful API？

SDK 能统一消费契约，但资源是什么、生命周期怎样变化、资源之间有什么关系，需要先通过业务建模确定。

以工作流发布为原理示例，假设业务要求发布时创建一个新版本，就需要先明确发布版本的资源边界、发布前后的状态，以及成功后返回什么资源。这些定义确定了，才能设计 URI、`publish` relation 和提交模板。否则只是给接口贴上 `publish` 名称，前后端对它操作什么、产生什么结果，仍可能理解不同。

所以我继续参与上游建模和 API 设计，先与后端明确业务语义，再把它表达成稳定的资源契约，最后由 SDK 提供统一的多端消费方式。我负责模型与契约设计、客户端 SDK 和 React 消费层研发，与后端协同落地 API 表达层。

### 如果面试官问：把权限和请求封装在前端公共模块中复用也能做到多端一致，为什么还要上 HATEOAS 动作契约？

把接口请求、权限判断或状态判断抽成前端公共模块，确实能规整调用并减少端侧的重复代码。但这解决的是**端侧实现的复用**，客户端依然需要在本地运行一套与服务端业务规则并行的推导逻辑。

HATEOAS 动作契约解决的是**职责边界的收敛**：

1. **推导与消费分离**：由服务端根据资源生命周期和当前用户上下文，直接决定该资源此刻能做什么、提交什么字段；客户端只负责按业务 relation 进行消费和交互呈现，不再在端侧复制状态机。
2. **动作要素一体化**：传统的公共模块往往把“有没有权限（布尔值）”、“调哪个接口（URL 与 Method）”、“入参是什么（Payload Schema）”割裂维护；而超媒体契约通过 `_links` 与 `_templates` 将动作的入口、协议、提交字段与约束内聚在资源上下文里，服务端调整规则或生命周期时，客户端无需同步升级端侧推导代码。

所以两者不是非此即彼，而是层次不同：SDK 负责多端消费层面的统一，而 HATEOAS 契约保证多端消费的是同一份来自服务端的运行时动作事实。

### 如果面试官问：后端直接在接口里返回 `canPublish` 这类布尔值不也行吗？

如果业务诉求仅仅是控制一个发布按钮的显示或隐藏，返回布尔值确实是最轻量直接的方案。

但在复杂低代码平台的应用与工作流场景下，用户面对的不只是一个按钮，而是一系列与生命周期绑定的操作闭环。返回 `canPublish: true` 只回答了“能不能点”，没有回答：

- 点击后要调用哪个 URI、采用什么 HTTP Method；
- 提交时需要携带哪些必填或选填字段（例如发布备注、版本说明）；
- 动作成功后会引起哪些关联资源的变化与缓存失效。

如果只返回布尔标记，上述接口路径和提交结构依然要硬编码在前端各处；而引入 HATEOAS 超媒体契约，是用同一套结构同时表达**动作入口、协议方法、提交约束与资源关系**，配合 SDK 让多端实现端到端的声明式消费。

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

前端根据本次快照中的 `publish` 呈现可用入口；资源读取时的可用性由后端状态、角色和权限规则决定，实际提交时仍由服务端重新判断业务合法性。前端负责交互呈现与契约消费。

### 如果面试官追：没有返回某个动作，前端是隐藏还是禁用？

这类情况不能让业务页面自己猜，需要由统一策略处理。

动作缺失可能表示当前状态不可执行、当前用户无权限或契约尚未就绪。UI 呈现可以根据产品交互需要决定：

- **非关键动作**：没有 relation 就直接不展示，减少页面视觉噪音。
- **关键高预期动作**（如审批页里的审批按钮）：可以保留禁用态；需要解释不可用原因时，可以进一步设计服务端原因提示，让页面展示“当前状态不可审批”等信息。

这里的核心架构原则是：**前端可以决定交互呈现，但绝不重新实现一份业务状态机**去推算为什么不能点。

### 如果面试官追：列表 100 条资源，每条都算动作，会不会很慢？

在与后端团队共同设计契约时，核心原则是避免在接口组装层按资源逐条查询权限，而是将动作计算与资源上下文、批量鉴权深度绑定，从架构层面规避 N+1 查询风险。

### 如果面试官问：工作区导航试点具体怎样改造与验证？

试点改造分为后端响应表达和前端消费两部分。我与后端协同在工作区资源响应中增加 `_links` 和 `_templates`：服务端根据当前权限提供 `workflow` 工作流列表入口，以及更新工作区基本信息的动作模板。

PC 与移动端将原来的 service 调用改为 SDK 消费。原先页面根据状态与权限信息推导入口是否可见，迁移后直接检查当前响应中有没有 `workflow` relation：有就渲染入口，没有就不展示；隐藏或禁用由产品设计决定，业务可用性由服务端契约表达。

验证时，我用 MSW（Mock Service Worker）模拟有、无 `workflow` relation 的两种工作区响应，再在 Vitest 中渲染导航组件，通过 DOM 断言检查工作流入口是否符合对应的渲染预期。有 relation 时预期入口存在，没有时预期入口不存在。这组导航组件测试验证的是客户端对契约的消费。

### 如果面试官问：推进中最难的地方是什么，怎样证明改造成本与风险可控？

最难的不是代码怎么写，而是让后端协作方确认增量改造的成本和数据风险可控。实现可以很轻，但协作方更关心它会不会影响已有的数据更新行为。

我与后端把改动范围明确到 API 表达层：在资源响应中增加 `_links` 和 `_templates`，保持表结构和原有请求参数不变。原 workflow 保存接口的返回本身没有改动，沿用已有的输入输出契约；资源表达则新增超媒体元数据。

验证上，我用 AI 辅助生成针对 workflow 接口正常保存与发布的端到端测试，在前后端实现后重新做回归。保存用例使用相同输入，对比原有的原始响应 JSON，检查已覆盖保存场景的输入输出兼容性。这样把成本和风险讨论落到具体改动边界与回归断言上。

### 如果面试官追：导航组件测试与 workflow 端到端回归分别验证什么？

导航组件测试使用 MSW 模拟工作区响应，在 Vitest 中渲染组件并检查 DOM，验证客户端如何消费有、无 `workflow` relation 的契约。

workflow 端到端回归针对保存与发布的已有接口流程，在前后端实现后重新验证。以保存为例，原接口返回没有变化，因此用相同输入对比原有响应 JSON，检查该保存场景的兼容性。两组测试分别关注入口的契约消费和已有写入接口的回归。

### 如果面试官问：SDK 这个独立的资源消费层具体承担什么？

我做的是独立的资源消费层，主要让业务页面按资源关系导航、按动作模板提交。

比如工作流发布，页面关心当前有没有 `publish`，以及怎样提交。SDK 负责解析服务端返回的 `_links` 和 `_templates`，业务通过 `follow()` 导航资源，通过 `action()` 获取动作并提交，再在运行时校验字段。

内部由 `Fetcher` 处理网络请求，`StateFactory` 将不同格式的响应解析为资源状态，`Resource` 按绝对 URI 定位与复用。普通读取优先使用缓存，需要最新数据时通过 `refresh()` 主动刷新。

这样，资源导航、动作提交和缓存处理集中在同一套消费层里，多端不用各自实现这些协议逻辑。若比较 Axios 与 React Query，比较的是职责：它们提供通用请求或状态缓存能力，SDK 进一步统一消费资源关系和动作模板。

```ts
const application = client.go("/applications/app-1")
const state = await application.get()

if (state.hasLink("publish")) {
  await state.action("publish").submit({ comment: "发布上线" })
}
```

### 如果面试官问：StateFactory 比直接返回 response.json() 多解决什么问题？

StateFactory 解决的是协议适配，不只是把响应转成 JSON 对象。SDK 消费资源时，除了业务数据，还需要资源 URI、关系和动作模板。如果页面直接拿原始 JSON，这些格式解析规则就会分散到业务代码中。

在当前实现里，Client 根据响应的 `Content-Type` 选择对应 Factory。以 HAL-Forms 为例，它把普通业务字段放到 `data`，把 `_links` 和 HTTP `Link` 响应头解析成统一的 Links，把 `_templates` 转换成内部的 Form 和 Field，并整理嵌入资源、保留响应头与资源 URI 上下文。

最终业务面对同一个 State 接口：通过 `data` 读取属性，通过 `follow()` 导航，通过 `action()` 获取动作再提交，而不用自己拆解原始协议字段。

因此，StateFactory 统一的是资源状态的消费方式。协议差异留在解析层，资源访问由 Resource 处理，动作校验和提交由 Action 处理。

### 如果面试官追：动态 links 怎么做 TypeScript 类型安全？

我把编译期和运行时分开处理。TypeScript 约束稳定的 relation 名称、资源数据和目标资源类型；服务端这次有没有返回某个入口，则是运行时事实。

例如，稳定的 relation 与目标 Entity 可以这样声明：

```ts
import type { Entity } from "@hateoas-ts/resource"

type WorkflowEntity = Entity<{ id: string; status: string }>

type ApplicationEntity = Entity<
  { id: string; status: string },
  {
    self: ApplicationEntity
    workflow: WorkflowEntity
    publish: ApplicationEntity
    revoke: ApplicationEntity
  }
>
```

业务代码因此能获得 relation 名称与目标类型的检查和补全。运行时再通过 `state.hasLink("publish")` 判断当前入口是否可用；调用不存在的动作时，`state.action()` 抛出 `ActionNotFound`。提交字段的合法性由模板和运行时 Schema 校验处理。

### 如果面试官追：提交字段从哪里来，运行时如何校验？

字段定义来自服务端当前动作模板的 `_templates.properties`，包含字段类型和必填等约束。SDK 将这些字段转换成 Zod 校验规则，通过 Standard Schema 接口接入 `action.submit(payload)` 的运行时验证。

校验失败时，请求在客户端被拦截，并抛出 `ActionValidationError`，其中的 `issues` 提供字段路径和错误消息，供页面展示字段错误。

业务页面也已接入这套模板驱动的动态表单：将模板字段描述转换成 JSON Schema 后，按页面样式渲染。校验与表单渲染共同消费服务端当前模板，字段定义随服务端调整，而不是在前端预先维护一份静态字段表。

### 如果面试官追：哪些变化可以不用前端重新发布？

关键是既有 relation、动作语义和消费能力是否仍然适用。角色或状态规则变化时，服务端调整当前下发的关系与动作，前端继续消费同一套契约，不需要同步改写端侧状态机。

以新增“发布说明”必填字段为原理示例，如果字段类型、校验规则和提交方式都在现有能力覆盖内，页面可以根据新模板渲染输入项、收集数据，再按模板提交。这里既需要校验，也需要用户能实际填写字段，不能仅凭“SDK 会拦截缺字段请求”判断无需发版。

如果 relation 名称或动作含义改变，或者新增字段需要新控件、特殊交互和提交处理，就需要相应调整前端。动态表单提供的是既有能力范围内的契约消费，而不是自动完成所有 UI 变化。

### 如果面试官追：资源缓存和 React Hooks 怎么处理？

我把 Resource 实例复用与响应状态缓存分开处理。同一个 Client 按目标绝对 URI 定位和复用 `Resource`，relation 名称负责表达关系，不作为资源身份。不同页面访问同一个目标，可以复用已有实例；两个都叫 `workflow` 的 relation 如果指向不同 URI，就对应不同资源。

`resource.get()` 优先读取已有完整状态缓存，缓存缺失时通过 `Fetcher` 请求，再由 `StateFactory` 解析响应。需要最新数据时，`resource.refresh()` 主动重新请求，并使用 `Cache-Control: no-cache`。相同进行中的请求由 SDK 去重。

React 层的 `useResource()` 通过内部读取 Hook 订阅 `update` 和 `stale`。收到 `update` 时用新 State 更新组件状态；收到 `stale` 时，只有开启 `refreshOnStale` 才主动调用 `resource.refresh()`，这个配置默认是 `false`。Hook 在卸载时清理监听。缓存失效通知与组件拿到新状态，是两个不同的环节。

### 如果面试官追：动作成功后，Content-Location 怎样更新缓存与页面？

以 `action.submit()` 经缓存中间件的路径为例，成功的 POST 这类修改响应会按规则处理请求 URI 的缓存失效。其它受影响资源可以由 HTTP `Link` 响应头的 `invalidates` relation 声明，`Location` 指向的资源也纳入失效范围。

如果响应带 `Content-Location` 且允许缓存写入，SDK 将本次响应体解析为该 URI 对应的新 State，写入缓存并发出 `update` 事件。这里的数据来自本次修改请求的响应体，不需要为此额外发一次 GET。`Content-Location` 标识这份响应内容对应的资源 URI，可以不同于提交请求的 URL。

React Hook 收到 `update` 后更新组件状态，让页面按新 State 重新渲染。这条路径是直接写回新状态；缓存失效后重新请求则由另一条刷新路径处理。

### 如果面试官追：没有返回新列表内容，SDK 怎样使关联列表缓存失效？

当前缓存中间件读取 HTTP `Link` 响应头的 `invalidates` relation，解析出受影响资源 URI，再调用 `clearResourceCache()` 清理缓存并发出 `stale` 事件。示意响应头如下：

```http
Link: </items>; rel="invalidates"
```

源码还支持通过 `inv-by` 注册缓存依赖，再沿依赖关系传播失效。`collection` 表达成员所属的集合；当前实现使用明确的失效声明或依赖关系来确定缓存失效范围。

列表收到 `stale` 后，配置 `refreshOnStale` 的消费方会重新请求，取得新 State 后通过 `update` 更新页面。失效通知本身不携带新列表数据。

### 如果面试官追：页面拿到 publish 后，提交前权限或状态变化怎么办？

资源返回的动作信息是读取时的快照。固定按钮或 `canPublish` 判断同样会遇到这个时间窗口，实际执行是否合法仍由服务端在提交时判断。

作为这种假设场景的处理方案，我会按接口约定区分权限拒绝和资源状态冲突，先给用户明确反馈，再调用当前 Resource 的 `refresh()`，重新取得服务端状态、关系和动作模板，避免继续使用旧缓存快照。

拿到新 State 后，页面按当前契约更新入口；如果已没有 `publish`，就按交互设计隐藏或禁用。后续操作基于新契约重新确认，而不是直接自动重试原发布请求。

### 如果面试官问：_links 拿不到页面是不是就废了？

我会先区分资源加载失败，还是资源已加载但当前没有某个动作入口。初次加载失败时，页面应展示错误与重试入口；已有缓存快照时，可以继续展示内容，但关键提交需要依据当前有效契约判断，不能在客户端重新推导一份权限或状态规则。

在页面容错设计上，可以把加载、只读查看和动作提交分开处理；在错误分级设计上，可以结合网络失败、HTTP 状态、动作缺失和字段校验失败，分别决定提示、重试或刷新。这样既保留可用内容，也让动作执行依赖明确的资源状态。

## 实现与证据

- SDK 用法与公开包：[[Knowledge/Sources/hateoas-ts/README|SDK 说明]]；[[Knowledge/Sources/hateoas-ts/RELEASE|发布说明]]。
- 协议分发与 State 构造：`Knowledge/Sources/hateoas-ts/packages/resource/src/lib/client-instance.ts` 的 `getStateForResponse()`；`Knowledge/Sources/hateoas-ts/packages/resource/src/lib/state/hal-state/hal-state.factory.ts`。
- 模板与字段解析：`Knowledge/Sources/hateoas-ts/packages/resource/src/lib/state/hal-state/parse-hal-templates.ts`。
- 动作校验与提交：`Knowledge/Sources/hateoas-ts/packages/resource/src/lib/action/action.ts`。
- 缓存响应契约与事件：`Knowledge/Sources/hateoas-ts/packages/resource/src/lib/middlewares/cache.ts`；`client-instance.ts` 的 `cacheState()` 与 `clearResourceCache()`。
- React 订阅与刷新策略：`Knowledge/Sources/hateoas-ts/packages/resource-react/src/lib/hooks/use-read-resource.ts`。
- workflow 保存、发布回归及保存响应的比较范围来自实际项目经历；公开 SDK 的 34 个测试文件、233 项通过测试对应通用消费层的自动化验证。

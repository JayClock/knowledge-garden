---
date: 2026-05-05 20:16:56
updated: 2026-07-09 10:45:13
---
# 动态链接的 TypeScript 类型推导与代码提示

**面试官追问：** *“既然所有接口 URL 和 Payload 都是动态从 `_links` 或 `_templates` 读取的，前端怎么知道有哪些 link？如何保证调用时的类型安全和智能提示？这不就变成 any 满天飞了吗？”*

**核心防御思路（化解“动态与类型安全冲突”的矛盾）：**
这确实是典型的“运行时动态”与“编译时静态”的矛盾。我们的解法是**通过泛型驱动的实体抽象（Generic Entity Abstraction）配合标准 Schema 校验模式，将编译时的强类型契约与运行时的动态路由完美结合**。

1. **泛型驱动的实体接口定义（Type-safe Entity Contracts）**：
 在底层 HATEOAS SDK（`@hateoas-ts/resource`）的设计上，我们放弃了传统的全局接口字典（集中式 API 列表），而是将类型抽象为 `Entity<TData, TLinks>` 的核心结构。前端开发者需要像定义聚合根一样，定义各个资源的 HATEOAS 契约：
   ```typescript
   type Post = Entity<{ id: string; title: string }, { self: Post; author: User }>;
   type User = Entity<
     { id: string; name: string },
     { self: User; posts: Collection<Post>; 'create-post': Post }
   >;
   ```
 这种方式使得数据载荷形状（Data Shape）和它可用的关系链接（Links & Actions）在编译阶段就被完全敲定。

2. **深度的 SDK 泛型封装与推导（Type Gymnastics）**：
 我们在 SDK 内部对资源的导航（`.follow()`）和动作（`.action()`）方法做了极严苛的泛型约束：
 `follow<K extends keyof TEntity['links']>(rel: K)`。
 当执行 `const posts = await user.follow('posts').get();` 时，IDE 的智能提示会自动限制只能输入 `'self' | 'posts' | 'create-post'`。并且 `posts` 的类型会被自动推断为 `State<Collection<Post>>`。如果手滑拼错或者强行传入不存在的 link 关系，TypeScript 会在编译期直接阻断，彻底消灭了“any 满天飞”的情况。

3. **Schema Plugin 与运行时边界防御（Runtime Validation Boundaries）**：
 哪怕通过了编译期校验，网络请求的动态性也注定了我们不能 100% 信任运行时的网络结构。我们在 SDK 中埋了两层运行时防御：
 - **安全寻址与降级**：当寻址不到期望的 link 或 form template 时，SDK 绝不默默崩溃，而是直接抛出细分的 `LinkNotFound` 或 `ActionNotFound`。这些异常会被上层的 Error Boundary 接管并展示友好的用户提示。
 - **动态表单与标准 Schema 校验**：我们引入了 `@standard-schema/spec`，并内置了对 Zod 的支持（`zodActionSchemaPlugin`）。在执行 `action.submit(payload)` 时，SDK 首先会根据服务端实际下发的 HAL-Forms 字段（如 `required`, `minLength`, `pattern` 等）自动构建 Zod Schema，在发起 HTTP 请求前对表单化 payload 进行校验。如果不符合服务端给出的动态约束，直接在本地抛出 `ActionValidationError`，提前拦截错误。

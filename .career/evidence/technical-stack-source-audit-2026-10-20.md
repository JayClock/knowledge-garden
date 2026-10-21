# 项目技术栈源码核对｜2026-10-20

## 本轮授权与核对方式

用户明确要求：建模平台的技术栈不需要 MCP、FM JSON；HATEOAS、监控与低代码工作流分别回到下面三个指定目录核对，并更新事实文件。

- HATEOAS：`content/Knowledge/Sources/hateoas-ts/`
- 监控：`content/Knowledge/Sources/企业级监控平台全栈架构设计/miaoma-monitor/`
- 低代码工作流：`content/Knowledge/Sources/企业级类扣子、Dify AI 应用引擎架构设计/miaoma-aiflow-v2/`

本轮静态读取 package.json、构建配置和实际源码引用，没有安装依赖或执行构建、测试及服务。依赖版本只描述当前材料快照，不推定公司生产版本、上线范围或个人编码归属。

根 package.json 的 SHA256：

| 来源 | SHA256 |
|---|---|
| hateoas-ts | `ea117a52809945b05e2b675f6b99a3ac305b5c0e474ac86ff9c8c1ab77803c52` |
| miaoma-monitor | `0881b53f0c70037cb9e5830045063682ba8716cbe1ceadf280834e8703b913ee` |
| miaoma-aiflow-v2 | `6441234188b847df422f6faa50bdc88e20726823c47dcbc6fcb6922f0b4ab16d` |

## Monorepo 统一记录口径

用户在本轮进一步明确：“monorepo 统一使用 nx + pnpm 记录”。因此，职业事实、经历文档和后续对外技术栈统一使用 **Nx＋pnpm**。

`miaoma-monitor` 和 `miaoma-aiflow-v2` 当前参考快照中的 Turborepo 配置仍按源码原样保留，只用于说明材料差异，不作为本人项目的 Monorepo 技术栈，也不据此声称已完成这些参考仓库的 Nx 迁移。本轮不修改任何源码或构建配置。

## 建模平台

当前对外技术栈以 Electron、React、React Flow、Pi SDK、OpenAPI 为口径，MCP 与 FM JSON 不列入技术栈。FM JSON 是模型表示名称，不作为独立框架或工具；也不再从 MCP 同步模块推导桌面端技术栈。

本轮上下文是技术栈列项纠正，不将“不需要”扩大为对历史功能从未实现的断言。此前单独确认的同步功能记录继续保留，当前技术栈选材不消费这些记录；Figma AI 的 MCP 事实不受本次纠正影响。

## HATEOAS

### 可核对技术

- SDK：TypeScript、HAL / HAL-FORMS、Inversify、Immer、Zod、Standard Schema。
- React 消费层：React Hooks 与 Context。
- 工程：Nx、pnpm Workspace、Vite、vite-plugin-dts、TypeDoc。
- 测试：Vitest、MSW、Testing Library。

### 文件与机制

路径均相对 `content/Knowledge/Sources/hateoas-ts/`：

- `package.json`：Nx / pnpm 任务及 TypeScript、React、Vite、Vitest、MSW、Testing Library、TypeDoc 声明。
- `packages/resource/package.json`：Inversify、Immer、Zod、`@standard-schema/spec` 等核心依赖。
- `packages/resource/src/lib/container.ts`：Inversify 容器与服务绑定。
- `packages/resource/src/lib/state/base-state.ts`：通过 Immer 的 `freeze` 冻结状态数据。
- `packages/resource/src/lib/action/action.ts`：Standard Schema 提交验证接口。
- `packages/resource/src/lib/action/zod-action-schema-plugin.ts`：由字段描述生成 Zod 校验。
- `packages/resource/vite.config.ts`：Vite 库构建、类型声明生成与 Vitest 配置。
- `packages/resource-react/package.json`、`packages/resource-react/src/lib/hooks/use-read-resource.ts`：React 消费层与测试工具。
- `README.md`、`RELEASE.md`：文档与发布流程说明；本快照缺少 `.github/`，不把文档描述当作本轮已检查到实际 workflow 文件。

业务页面的 JSON Schema 动态表单仍由既有用户确认支持，与 SDK package 的直接依赖清单分开。Axios、React Query 不作为本 SDK 的实际技术栈。

## 监控 SDK 与数据采集后端

### 可核对技术

- SDK：TypeScript、PerformanceObserver、源码内置的 Web Vitals 指标实现、Fetch、XMLHttpRequest 和浏览器异常入口。
- 服务与数据：NestJS、Kafka、ClickHouse；服务端还声明 TypeORM、PostgreSQL 等基础依赖。
- 工程记录口径：Nx＋pnpm；tsup 与 tsc 用于编译和类型声明生成。参考快照使用 Turborepo，按上方统一口径处理。

### 文件与机制

路径均相对 `content/Knowledge/Sources/企业级监控平台全栈架构设计/miaoma-monitor/`：

- `package.json`、`turbo.json`：pnpm、Turborepo、tsup、TypeScript 及任务配置。
- `packages/core/package.json`、`packages/browser/package.json`、`packages/browser-utils/package.json`：core / browser / browser-utils 包依赖、tsup 编译与 tsc 类型声明生成。
- `packages/browser-utils/src/metrics/lib/observe.ts`、`packages/browser-utils/src/metrics/onLCP.ts`：PerformanceObserver 与内置 Web Vitals 指标实现；不称为已经安装 `web-vitals` npm 包。
- `packages/browser/src/tracing/errorsIntegration.ts`：全局错误和未处理 Promise 拒绝入口。
- `packages/browser/src/transport/index.ts`：Fetch 上报。
- `apps/backend/dsn-server/package.json`：NestJS、kafkajs、ClickHouse 客户端及 TypeORM / pg 声明。
- `apps/backend/monitor/package.json`、`apps/backend/monitor/src/app.module.ts`：后端基础依赖与 TypeORM 接入。
- `apps/backend/dsn-server/src/fundamentals/clickhouse/clickhouse.module.ts`：ClickHouse 客户端注入。
- `apps/backend/monitor/src/fundamentals/kafka/KafkaComsumerService.ts`：Kafka 消费接口；其 `writeToClickHouse` 仍为日志和注释，不能据此声称此快照已运行验证完整消费入库链路。

### 与已确认经历的分工

- `miaoma-monitor` 继续作为代表性机制核对材料，不因其中 React / Vue 适配目录为空或局部实现不全，否定既有明确确认的多框架接入、生产 Sourcemap 或数据后端事实。
- 源码中的 `apps/frontend/monitor` 含 React、Vite、Tailwind CSS、Radix UI、TanStack Query、Axios、Recharts 等控制台依赖；既有项目范围明确不含可视化分析，不将这些控制台依赖自动列为本人已交付成果或核心技术栈。
- 已确认的系统响应性能提升 50% 保持原口径；本轮不产生新的运行或性能结论。

## 低代码工作流引擎

### 可核对技术

- 工作流前端：TypeScript、React、Next.js、React Flow（`@xyflow/react`）、Tiptap、Tailwind CSS、Radix UI、React Hook Form、Zod。
- 执行与反馈：TypeScript 引擎、SSE；NestJS API 服务。
- 数据层：Prisma、PostgreSQL。
- 工程与测试记录口径：Nx＋pnpm、tsup；引擎包配置 Vitest。参考快照中的 Turborepo 不进入本人项目技术栈。

### 文件与机制

路径均相对 `content/Knowledge/Sources/企业级类扣子、Dify AI 应用引擎架构设计/miaoma-aiflow-v2/`：

- `package.json`：pnpm、Turborepo、TypeScript、tsup。
- `apps/workflow/package.json`：Next.js、React、React Flow、Tiptap、Tailwind CSS、Radix UI、React Hook Form、Zod、Prisma / pg 声明。
- `apps/workflow/components/flow/editor/index.tsx`：React Flow 画布接入。
- `apps/workflow/components/flow/settings/variable-editor/index.tsx`、`variable-mention.ts`、`slash-command.ts`：Tiptap 变量节点与 Suggestion 接入。
- `apps/workflow/components/ui/form.tsx`、`button.tsx`：表单与 Radix UI 组件依赖。
- `apps/api-server/package.json`：NestJS、Prisma、pg、RxJS。
- `apps/api-server/prisma/schema.prisma`：PostgreSQL datasource。
- `apps/api-server/src/modules/workflow/workflow.controller.ts`：`text/event-stream` 服务端响应。
- `apps/workflow/lib/hooks/use-workflow-runner.ts`：前端流式读取与 TextDecoder 解码。
- `packages/ai-engine/package.json`：tsup 构建、Vitest 测试配置。

### 与已确认经历的分工

- `miaoma-aiflow-v2` 是代表性重实现，不把此快照的所有包都扩大为个人交付范围。
- 原有个人职责保持：执行引擎、编辑器、公式链路及 SSE 服务端与前端；其他 API 与 Prisma / PostgreSQL 持久化沿用后端协作分工。
- 源码含 LangChain、LangGraph、Qdrant 和 AI / 知识库节点等扩展，不因依赖存在就把用户已确认的普通业务工作流改写成 AI / RAG 项目。

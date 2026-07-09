---
title: Evidence 项目简历描述与面试话术
date: 2026-07-03 13:00:00
updated: 2026-07-09 20:21:41
tags:
  - resume/project
  - interview/story
  - evidence
  - local-first
aliases:
  - Evidence 简历项目
  - Evidence 面试话术
---

# Evidence 项目简历描述与面试话术

> [!note]
> 这份素材用于补充 [[全栈工程师简历]]。建议根据投递方向选择「前端架构 / 全栈平台 / AI 工程化」其中一个版本，不要全部塞进正式简历，避免篇幅过重。

## 一句话定位

**Evidence 是一个本地优先的业务履约建模与证据映射平台**：借鉴 Obsidian 的 Vault、Canvas、Properties/Bases 与关系图谱体验，但面向复杂业务建模场景，把合同、履约请求、履约确认、参与方、角色和上下文沉淀为可版本化、可审查、可视化的模型资产。

## 和 Obsidian 现有功能的对应关系

| Obsidian 功能 | Evidence 中的对应能力 | 简历表达重点 |
|---|---|---|
| Vault 本地文件库 | `.evidence/entities` 与 `.evidence/associations` 本地模型目录 | 本地优先、文件即模型、可 Git 管理 |
| Canvas | 履约建模画布，展示 Evidence / Role / Participant / Context | 复杂图谱渲染、自动布局、领域可视化 |
| Properties / Bases | Logical Entities 表格、类型、子类型、属性、Markdown 说明 | 结构化知识管理、概念字典 |
| Graph View / Backlinks | Association 关系图谱，表达实体间履约关系 | 关系建模、依赖追踪、上下文边界 |
| 插件 / AI 工作流 | Pi RPC + AI 建模助手，流式输出 proposal | AI 辅助建模、人工审查、可控应用 |
| 桌面端体验 | Tauri Desktop + 内嵌 Axum API + SQLite | Web/Desktop 单前端，多运行时部署 |

---

# 简历可直接复制版本

## 版本 A：全栈 / 平台工程版

### Evidence｜本地优先的业务履约建模与证据映射平台

**项目简介**

面向复杂业务履约建模场景，设计并实现一个类 Obsidian 的本地优先建模平台。系统以 Workspace 为入口，将业务概念抽象为 Evidence、Participant、Role、Context 等逻辑实体，并通过关系图谱表达 RFP、Proposal、Contract、Fulfillment Request、Fulfillment Confirmation 等履约凭证流。项目支持 Web 与 Tauri Desktop 双端运行，模型数据可沉淀为本地 `.evidence` YAML 文件，便于版本管理、Diff 审查和长期演进。

**工作内容与成果**

- **本地优先模型存储设计**：参考 Obsidian Vault 思路，设计 `.evidence/entities` 与 `.evidence/associations` 文件结构，将业务实体与关系落为可读 YAML 文件；Rust 持久层负责解析、校验、序列化与 CRUD，使模型资产可被 Git 管理、Diff 审查和 AI 工具读取。
- **领域驱动后端架构**：基于 Rust Axum 构建 REST API，以 `Entity / HasMany / HasOne` 等 trait 抽象领域模型，将 User、Workspace、LogicalEntity、Diagram、Node、Edge 等聚合和持久化实现解耦，并通过 Fake Store、SQLite/PostgreSQL 实现共享契约测试。
- **HAL/HATEOAS 资源契约**：后端资源统一返回 `_links` 与 `_templates`，前端通过 relation 跟随资源和动作模板，而不是硬编码 API 路径，降低 Web/Desktop 双端和后端接口演进时的契约漂移。
- **Web/Desktop 单前端架构**：使用 React + Vite 作为唯一前端代码源，浏览器模式消费远程 Axum API，桌面模式由 Tauri 启动内嵌 Axum 服务并使用本地 SQLite，保证同一套 UI 在 Web 与 Desktop 下共享领域语义。

## 版本 B：前端架构版

### Evidence｜类 Obsidian 的业务建模 Canvas 平台

**项目简介**

设计并实现一个面向业务履约建模的可视化工作台，参考 Obsidian Canvas 与 Graph View 的交互范式，将合同、履约请求、履约确认、角色、参与方和上下文抽象为结构化图节点，通过自动布局和关系投影帮助用户理解复杂业务流程中的权责、凭证和边界。

**工作内容与成果**

- **复杂图谱画布实现**：基于 React、React Flow 与 ELK 构建建模 Canvas，支持 Context 容器、Evidence 节点、Role/Participant 分层展示，以及支付、开票、发货等多条履约分支的领域化布局。
- **履约语义布局算法**：不是使用通用节点随机布局，而是围绕 RFP → Proposal → Contract → Fulfillment Request → Fulfillment Confirmation 的业务阶段设计布局规则，将合约前上下文、合约上下文、履约泳道和参与对象分层展示。
- **关系收敛与引用投影**：针对同一 Participant 在多条履约分支中反复出现的问题，设计 reference node 与 canonical edge，将公共参与方投影到履约行内，同时保留到原始节点的虚线引用，降低图谱阅读噪音。
- **结构化实体视图**：参考 Obsidian Properties / Bases，构建 Logical Entities 表格与详情抽屉，支持实体类型、子类型、属性和 Markdown 内容展示，让概念字典与图谱视图保持一致。

## 版本 C：AI 工程化版

### Evidence｜AI 辅助的业务履约建模平台

**项目简介**

围绕 AI 参与业务建模后的可控性问题，设计一个「自然语言需求 → 建模建议 → 人工审查 → 文件化模型」的 AI 辅助建模流程。系统通过 Pi RPC 调用受限工具读取和编辑 `.evidence` 模型目录，并以流式事件展示 reasoning、tool call、tool execution 和 proposal JSON，避免 AI 直接越权修改核心模型。

**工作内容与成果**

- **AI 建模助手集成**：基于 AI SDK 与 SSE 构建建模助手面板，将自然语言需求流式转化为建模建议，前端实时展示思考过程、工具调用、执行结果和最终 proposal。
- **受控工具边界设计**：后端通过 Pi RPC 启动独立进程，并限制工具范围为 read/edit/write/ls/find/grep，运行目录限定在 `.evidence` 模型空间，降低 AI 对项目其他代码和用户环境的误操作风险。
- **Proposal-first 审查机制**：AI 输出不直接视为最终结果，而是转化为包含 add/update/delete entities 与 relationships 的结构化 proposal，前端以摘要、变更数量和 JSON 原文展示，保留人工审查与回滚空间。
- **流式事件适配层**：将 Pi RPC 的 message_update、tool_execution_start/end、agent_end 等事件转换为前端可消费的 SSE 事件，统一处理 reasoning、文本增量、工具调用与异常状态。

---

# 正式简历精简版

如果正式简历只留 3 条，可以用这一版：

- 设计并实现本地优先的业务履约建模平台，将 Evidence、Participant、Role、Context 等业务概念落为 `.evidence` YAML 文件，支持 Git 版本管理、Diff 审查和模型演进。
- 基于 React Flow + ELK 构建类 Obsidian Canvas 的建模画布，实现上下文容器、履约分支自动布局、关系收敛展示和结构化实体管理。
- 基于 Rust Axum 构建 HAL/HATEOAS API，并集成 Tauri Desktop、SQLite/PostgreSQL 与 AI 建模助手，支持 Web/桌面双端和自然语言建模建议。

---

# 面试可聊项目描述

## 1 分钟介绍

Evidence 这个项目可以理解成「面向业务建模场景的 Obsidian + Canvas + AI 助手」。Obsidian 解决的是个人知识本地化和双链组织的问题，而 Evidence 解决的是复杂业务履约过程怎么被结构化表达的问题。

我把业务中的凭证、角色、参与方和上下文抽象成四类逻辑实体，并用 `.evidence` 目录下的 YAML 文件作为模型源。前端用 React Flow 做 Canvas，用 ELK 和领域规则做自动布局；后端用 Rust Axum 提供 HAL/HATEOAS API；桌面端用 Tauri 包一层本地 SQLite 和内嵌 API。后面还接入了 AI 建模助手，让用户可以用自然语言生成建模 proposal，但不会绕过人工审查直接改模型。

这个项目重点不是画图本身，而是把复杂业务知识沉淀成「可读文件 + 资源契约 + 可视化图谱 + AI 可审查建议」的工程资产。

## 3 分钟展开

这个项目的背景是，我在做业务建模和履约建模时发现，很多复杂业务规则并不缺页面，而是缺一种能持续沉淀的结构化表达方式。普通文档容易变成自然语言堆积，普通流程图又缺少实体、属性和可审查的关系数据，所以我参考 Obsidian 的本地优先体验做了 Evidence。

系统里有三个核心设计。

第一是**文件即模型**。每个业务概念是 `.evidence/entities/*.yaml`，每条关系是 `.evidence/associations/*.yaml`。这样模型不是锁在数据库里，而是可以被 Git 版本管理、被 AI 工具读取、被 Code Review 审查。数据库只负责 Workspace、用户和本地桌面状态，模型本身保持本地文件可读。

第二是**领域语义 Canvas**。我没有直接用通用布局算法把节点铺开，而是结合履约建模方法，把 RFP、Proposal、Contract、Fulfillment Request、Fulfillment Confirmation 映射成业务阶段，再按合约前上下文、合约上下文、履约泳道、角色层和参与对象层进行布局。这样用户看到的不是一团点线，而是带业务语义的履约图。

第三是**超媒体资源契约和 AI 审查边界**。后端每个资源都返回 `_links` 和 `_templates`，前端沿着 relation 消费 API；AI 侧则通过 Pi RPC 生成 proposal，前端展示工具调用和 JSON 变更摘要，让 AI 产物先进入审查态，而不是直接变成不可控修改。

如果面试官问这个项目的价值，我会说它不是一个普通画图工具，而是一次把「知识管理、本地优先、领域建模、可视化和 AI 辅助」组合在一起的平台工程实践。

---

# 可以重点聊的技术点

## 1. 为什么参考 Obsidian，而不是直接做一个 SaaS 建模工具？

可以这样回答：

Obsidian 最有价值的地方不是 Markdown 编辑器，而是它的本地优先模型：数据在用户手里，文件可读、可迁移、可被 Git 管理。Evidence 参考的是这个底层理念，而不是简单复刻 UI。

业务建模资产和普通业务数据不一样，它更像长期演进的知识资产，需要被审查、被 diff、被回滚、被 AI/脚本处理。如果直接存在数据库里，短期 CRUD 会方便，但长期的模型演进、跨工具协作和版本审查会变困难。所以我把模型源放在 `.evidence` 文件目录里，数据库只维护 Workspace 和运行态信息。

## 2. YAML 文件和数据库之间怎么取舍？

可以这样回答：

我的取舍是：**业务模型源文件优先，运行时状态数据库优先**。

- YAML 适合保存实体、关系、属性、说明这些需要人读、人审查、可版本化的模型资产。
- SQLite/PostgreSQL 适合保存用户、Workspace、成员、运行状态、索引和未来可能扩展的协作数据。
- 后端持久层把 YAML 文件投影成领域对象，对前端仍然暴露统一 API，所以前端不需要关心底层来自文件还是数据库。

这种设计牺牲了一部分复杂查询能力，但换来了可审查性、可迁移性和 AI 工具友好性。

## 3. Canvas 自动布局难点是什么？

可以这样回答：

难点不是把 React Flow 接起来，而是通用图布局无法表达履约建模里的语义顺序。

例如 Contract 是合约入口，支付、开票、发货是三条履约分支；Role 应该在合约上下文上方，Participant 应该在下方；RFP 和 Proposal 属于合约前上下文。如果直接用 force layout 或普通 layered layout，图会有线交叉、上下文混乱和业务阶段错位。

所以我做了两层布局：先根据节点类型和子类型识别业务阶段，再构造合约前上下文、合约上下文、履约泳道和共享对象池；最后再用 ELK 处理局部连线和位置计算。这样布局结果更符合业务阅读顺序。

## 4. HATEOAS 在这个项目里解决什么问题？

可以这样回答：

我不是为了概念使用 HATEOAS，而是因为这个项目天然有资源导航关系：Root → User → Workspace → Diagram / LogicalEntities / Relationships。Web 和 Desktop 共用一套前端，如果前端到处硬编码 API 路径，后端演进时很容易产生契约漂移。

所以后端每个资源都返回 `_links`，动作类能力返回 `_templates`。前端从 API root 开始 follow relation，例如 follow `default-user`，再 follow workspace 的 `diagram` 或 `logical-entities`。这样前端消费的是资源关系，而不是散落的字符串路径。

## 5. AI 建模助手为什么不直接自动修改？

可以这样回答：

因为建模和普通代码补全不一样，它会影响业务概念、权责边界和后续协作。如果 AI 直接改模型，用户很难判断它改了什么、为什么改、有没有越界。

所以我采用 proposal-first：AI 可以读取模型目录、生成建议、展示工具执行过程，但最终产物是结构化 proposal，包括新增/修改/删除哪些实体和关系。前端展示变更数量、摘要和 JSON 原文，让用户先审查，再决定是否应用。这个边界和我之前做 AI 交付治理时的思路一致：AI 可以提速，但不能绕过证据和审查。

## 6. Web 和 Desktop 怎么共用一套前端？

可以这样回答：

前端只依赖 API root，不直接依赖部署形态。浏览器模式下，API base URL 来自 Vite 环境变量或 `/api`；Tauri 模式下，桌面端启动内嵌 Axum API，并通过 Tauri command 返回随机端口的 API base URL。

这样 React 应用不需要区分自己是在浏览器还是桌面，只要初始化 API client 时拿到 root URL 即可。Desktop 负责本地 SQLite、系统目录选择和窗口壳，Web 负责正常 HTTP 部署，两者共享同一套资源契约和 UI。

## 7. 这个项目如何体现你的前端架构能力？

可以这样回答：

它不是单纯页面项目，前端里面有几个架构点：

1. HATEOAS Client 消费层，避免 API 路径硬编码。
2. React Flow Canvas 和领域布局算法，把业务语义映射成图形结构。
3. Logical Entities 的表格、详情抽屉和 Markdown 渲染，承接结构化数据与文档内容。
4. AI 助手面板，把 SSE、reasoning、tool call、proposal JSON 统一渲染成可审查过程。
5. Web/Desktop 共享前端，通过 runtime API base URL 适配不同部署环境。

所以这个项目更像一个平台型前端，而不是普通 CRUD 页面。

## 8. 这个项目如何体现你的全栈能力？

可以这样回答：

后端不是简单写接口，而是按领域模型拆了层：domain 层定义 User、Workspace、Diagram、LogicalEntity、Relationship 等 trait；persistent 层分别实现 Fake Store、SQLite/PostgreSQL 和 YAML 文件投影；api 层只负责 Axum 路由、请求解析和 HAL JSON 序列化。

这样做的好处是业务规则不散落在 handler 里，测试也可以复用契约。比如 Fake Store 可以跑快速单测，数据库实现可以跑集成测试，文件投影则可以独立验证 YAML 解析和序列化。

---

# 面试官可能追问与回答

## Q1：这个项目和 Obsidian 最大区别是什么？

Obsidian 是通用知识管理工具，核心对象是 Markdown note 和链接；Evidence 是领域建模工具，核心对象是业务凭证、参与方、角色和上下文。它不是让用户自由画图，而是把履约建模方法内置为结构化类型、关系和布局规则。

## Q2：为什么不用现成白板工具或流程图工具？

白板工具的问题是缺少结构化语义。它们能画出图，但图里的节点和边通常只是视觉元素，很难被 API、测试、AI 或 Git 审查消费。Evidence 的每个节点都是实体，每条边都是关系，图只是模型的投影，所以它可以进一步做校验、查询、生成和审查。

## Q3：你在这个项目中最核心的技术决策是什么？

最核心的是把模型源放在本地文件，而不是数据库或纯前端状态。这个决策影响了后面的所有架构：后端需要做文件投影，前端需要通过 API 消费，AI 需要受限在 `.evidence` 目录里工作，桌面端需要负责本地 Workspace 管理。它让系统更像开发者工具和知识库，而不是传统 SaaS。

## Q4：如果未来要多人协作怎么办？

短期可以依赖 Git 协作，因为模型是文本文件；中期可以在服务端增加索引、锁和冲突检测；长期可以把 YAML 作为 source of truth，数据库作为 query/index/cache layer。多人实时协作不是第一阶段目标，因为这个项目优先解决模型资产可读、可审查和可版本化的问题。

## Q5：这个项目目前有什么不足？

我会诚实说三个：

1. 当前更偏单人本地建模，多人协作能力还需要设计冲突解决和权限模型。
2. YAML 文件适合审查，但复杂查询和大规模索引需要额外的数据库投影层。
3. AI 目前以 proposal 和工具过程展示为主，还需要补更完整的 schema 校验、diff preview 和一键回滚能力。

这样回答反而能体现你对边界有判断。

---

# 可量化素材占位

> [!warning]
> 简历里不要硬编业务数据。可以从下面这些方向补充真实数字。

- 当前示例模型：`25` 个实体 YAML、`33` 条关系 YAML，用于验证履约建模布局和关系投影。
- 工程拆分：Web 前端拆为 API Client、UI、Shell、Diagram Feature、Logical Entities Feature、Resource Browser 等模块。
- 后端拆分：API、Domain、Persistent、Infrastructure 多 crate / library 分层。
- 质量验证：可补充 Rust contract tests、Vitest 组件测试、YAML parser 单测、Canvas layout 关键用例数量。
- 性能指标：可补充大图节点数、边数、布局耗时、SSE 首包时间、桌面启动时间等实测数据。

---

# 投递方向选择建议

## 投前端架构

突出：React Flow、ELK、Canvas、HATEOAS Client、AI 助手 UI、Web/Desktop 单前端。

不要过度展开 Rust domain trait，除非面试官追问全栈。

## 投全栈 / 平台工程

突出：Rust Axum、领域分层、文件 + 数据库混合持久化、HAL API、Tauri Desktop、契约测试。

强调「不是一个页面，而是一套建模平台」。

## 投 AI 工程化

突出：AI proposal-first、工具边界、SSE 流式事件、reasoning/tool call 展示、人工审查与回滚空间。

可以和 [[自我介绍]] 里的多智能体交付治理主线衔接。

---

# 可以插入到 [[全栈工程师简历]] 的位置

建议放在「项目经历」中，替换掉一个和目标岗位相关度较低的项目；如果投 AI 工程化岗位，可以放在「多智能体协同平台」之后，作为个人平台工程项目补充。

## 推荐最终标题

**Evidence｜本地优先的业务履约建模与 AI 辅助建模平台**

这个标题同时覆盖：

- 本地优先
- 业务建模
- AI 工程化
- 平台项目属性

## 最短版项目描述

Evidence 是一个参考 Obsidian 本地优先体验的业务履约建模平台，将业务凭证、角色、参与方和上下文沉淀为 `.evidence` YAML 模型文件，并通过 React Flow Canvas、Rust Axum HATEOAS API、Tauri Desktop 和 AI 建模助手实现可视化、可审查、可版本化的建模工作流。


## 15 分钟逐字稿

- 详见 [[15 分钟：Evidence 面试逐字稿]]。
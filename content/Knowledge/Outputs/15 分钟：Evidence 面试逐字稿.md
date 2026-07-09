---
title: Evidence 项目 15 分钟面试逐字稿
date: 2026-07-03 21:30:00
updated: 2026-07-09 20:21:41
tags:
  - interview/script
  - resume/project
  - evidence
aliases:
  - Evidence 15 分钟逐字稿
---

# Evidence 项目 15 分钟面试逐字稿

关联素材：[[Evidence 项目简历描述与面试话术]]、[[全栈工程师简历]]

> [!tip]
> 这份稿子适合在面试官说「挑一个你最能代表能力的项目展开讲一下」时使用。整体以 Evidence 为主，少量带出 HATEOAS 和 AI 协同治理，不要讲成单纯多智能体项目。

---

## 0:00 - 1:00 开场定位

如果让我选一个比较能代表我最近技术思考的项目，我会讲 Evidence。

Evidence 是一个本地优先的业务履约建模与证据映射平台。它有点像面向业务建模场景的 Obsidian：Obsidian 用 Vault、Canvas、Properties 和双链来管理个人知识；Evidence 则用本地模型文件、业务 Canvas、结构化实体和关系图谱来管理复杂业务中的合同、履约请求、履约确认、参与方、角色和上下文。

这个项目不是一个普通画图工具。它真正想解决的问题是：复杂业务知识如何从自然语言文档、会议讨论和零散流程图中沉淀为一套可版本化、可审查、可视化、也能被 AI 工具读取和辅助生成的模型资产。

我在这个项目里主要负责整体架构设计和核心实现，包括前端 Canvas、Rust Axum 后端、本地 `.evidence` 文件模型、Tauri Desktop 运行时，以及 AI 建模助手的 proposal-first 流程。

---

## 1:00 - 2:30 项目背景：为什么要做 Evidence

这个项目的背景和我之前做 SaaS、低代码、HATEOAS 资源契约的经历有关。

在企业系统里，很多复杂度不是来自页面，而是来自业务规则本身。比如一个采购履约场景里，会有询价、报价、合同、支付申请、支付确认、发货申请、发货确认、开票申请、开票确认。每一步都有凭证，每个凭证背后又有参与方、角色、权责、时间点、金额、验收条件和异常情况。

如果这些东西只写在 PRD 或会议纪要里，后面很容易出现几个问题：第一，业务概念没有统一语言，产品、研发、测试、业务方对同一个词理解不一致；第二，流程图只能表达顺序，但很难表达每个节点背后的结构化属性；第三，模型如果只存在数据库或页面状态里，不方便 Git Diff、审查和回滚；第四，AI 参与建模或生成代码时，也缺少一份可读、可操作的结构化上下文。

所以我想做一个工具，把复杂业务从「文档描述」提升为「模型资产」。Evidence 的核心就是围绕履约建模，把业务中的凭证、参与方、角色和上下文显式建模，再通过图谱和文件系统让它可以被人看、被系统校验、被 AI 辅助。

---

## 2:30 - 4:00 核心设计：从 Obsidian 借鉴了什么

我借鉴 Obsidian 的不是 UI 皮肤，而是几个底层理念。

第一是 Vault，本地优先。Evidence 里每个 Workspace 都可以对应一个本地项目目录，真正的业务模型放在 `.evidence` 目录下。实体在 `.evidence/entities`，关系在 `.evidence/associations`。每个文件都是 YAML，可读、可 diff、可提交到 Git，也可以被 AI 工具直接读取。

第二是 Canvas。Obsidian Canvas 是自由画布，适合组织知识卡片。Evidence 的 Canvas 更领域化，它不是随便画节点，而是把 Evidence、Role、Participant、Context 这些业务对象投影成图节点，再根据履约阶段做自动布局。

第三是 Properties 和 Bases。Obsidian 可以给笔记加属性，然后用 Bases 做结构化视图。Evidence 里有 Logical Entities 集合视图，展示实体名称、类型、子类型、属性和 Markdown 内容。也就是说，用户既可以从表格视角维护概念字典，也可以从 Canvas 视角理解关系。

第四是关系图谱。Obsidian 的双链和 Graph View 帮助人理解知识之间的连接。Evidence 里每条 association 都是一条业务关系，比如合同约束支付履约、支付请求被支付确认完成、某个角色由某个参与方扮演。图谱不是视觉装饰，而是模型本身的投影。

---

## 4:00 - 6:00 整体架构

整体架构上，Evidence 有三个运行面。

第一是 Web，使用 React + Vite。它是唯一的前端代码源，负责 Workspace、Logical Entities、Diagram Canvas 和 AI 建模助手等 UI。

第二是 Server，使用 Rust Axum。后端分成 API、Domain、Persistent 和 Infrastructure 几层。Domain 层定义 User、Workspace、LogicalEntity、Diagram、Node、Edge、Relationship 等领域对象和 trait；Persistent 层负责把数据库或 YAML 文件投影成领域对象；API 层只负责路由、请求解析和 JSON 资源序列化。

第三是 Desktop，使用 Tauri 2。桌面端不是另写一套产品，而是复用同一个 React 前端。Tauri 启动后会在本地拉起内嵌 Axum API，使用本地 SQLite 保存用户和 Workspace 信息，然后前端通过 Tauri command 获取 API base URL。这样 Web 和 Desktop 的差异只在运行时部署模型，不在业务语义和前端代码上分叉。

这个架构的好处是：浏览器模式可以作为普通 Web 应用运行，桌面模式可以作为本地建模工具运行；前端只认 API root，不关心底层是远程服务还是本地内嵌服务；后端领域模型也不和具体持久化方式强绑定。

---

## 6:00 - 8:00 本地优先模型与文件投影层

Evidence 里我最核心的一个设计决策，是把业务模型源放在本地文件，而不是一开始就完全放进数据库。

比如一个合同节点会是一个 YAML 文件，里面有 id、name、label、type、subType、parent 和 attributes。type 可能是 EVIDENCE，subType 可能是 contract。支付申请也是一个 YAML，subType 是 fulfillment_request。关系则放在 associations 目录，比如 contract 到 payment request 的关系，source 是合同，target 是支付申请，relationshipType 可以是 timeline 或 fulfillment。

后端的文件投影层负责几件事。

第一，扫描 `.evidence/entities` 和 `.evidence/associations` 目录，只读取 yaml 或 yml 文件。

第二，把 YAML 解析成领域对象，比如 LogicalEntity、DiagramNode、DiagramEdge。对于 Canvas 来说，实体文件会投影为节点，关系文件会投影为边。

第三，做基础校验和标准化，比如必填字段、空字符串处理、实体类型和子类型规范化。

第四，把文件修改时间映射为 createdAt、updatedAt 这类资源字段，让前端仍然像消费 API 资源一样消费模型。

这样设计有一个关键收益：模型资产不是被锁在某个应用里。它可以被 Git 管理，可以被 Code Review，可以被脚本批量处理，也可以被 AI 工具读取。数据库更多承担运行态、Workspace 管理和桌面本地状态，而不是把业务模型变成黑盒。

当然这个设计也有取舍。YAML 文件不适合复杂查询，也不适合高并发多人实时协作。所以我会把它定位为 source of truth，而不是查询层。未来如果要做多人协作，可以增加数据库索引层、锁机制和冲突检测，但模型源仍然可以保持文件化。

---

## 8:00 - 10:30 Canvas 和自动布局

前端最复杂的一块是建模 Canvas。

如果只是把 React Flow 接起来，其实不难。难点在于：业务履约图不是普通拓扑图，它有强语义顺序。RFP 和 Proposal 属于合约前上下文，Contract 是正式合约入口，后面会展开支付、开票、发货等多条履约分支。Role 通常应该在合约上下文上方，Participant 和 Thing 通常在下方。履约请求和履约确认则应该成对出现在一条履约泳道里。

所以我没有直接采用通用 force layout，而是做了领域语义布局。

第一步，先根据节点的 type、subType、label、name 等信息识别它属于哪个履约阶段。比如 rfp、proposal、contract、fulfillment_request、fulfillment_confirmation。

第二步，识别上下文。合约前阶段放到合约前上下文，合同和后续履约分支放到合约上下文。如果用户没有显式创建上下文，系统可以生成合成上下文，保证图谱仍然有清晰边界。

第三步，构造履约泳道。每个 Fulfillment Request 可以作为一行的起点，后面跟它对应的 Confirmation，以及相关补充 Evidence。这样支付、开票、发货可以形成横向分支，而不是全部挤在一个随机图里。

第四步，处理参与方和角色。Role 会放在上方，Participant、Thing、第三方系统等会放在下方。对于同一个参与方在多条履约分支里被引用的问题，我做了 reference node 的投影：在具体泳道里生成一个引用节点，同时用虚线关系指回 canonical node。这样既能减少跨层长边，又不丢失它是同一个参与方的事实。

最后，局部布局和连线再交给 ELK 处理。也就是说，我用领域规则先确定结构和分区，再用布局引擎处理几何细节。这样画布呈现出来不是一团点线，而是更符合业务阅读顺序的履约模型图。

---

## 10:30 - 12:30 AI 辅助建模

Evidence 里也接入了 AI 建模助手，但我没有把它设计成「AI 直接替用户改模型」。我的原则是 proposal-first。

用户可以在 Diagram 旁边的 AI 面板里输入自然语言需求，比如“帮我建模一个办公笔记本采购履约过程，包括询价、报价、合同、支付、发货和开票”。前端通过 AI SDK 的 useChat 发起请求，后端通过 SSE 把事件流推回来。

后端这一层会通过 Pi RPC 启动一个受控的 agent 进程，并且限制它的工具范围，比如 read、edit、write、ls、find、grep，同时把运行目录限定在 `.evidence` 模型目录。这个边界很重要，因为 AI 如果可以随便访问整个仓库或系统目录，风险太高。

在流式过程中，我会把 Pi RPC 的事件转换成前端可理解的事件，比如 reasoning started、reasoning chunk、tool call started、tool execution started、tool execution ended、agent ended。前端对应展示思考过程、工具调用、执行结果和最终 proposal。

最终输出不是一句自然语言结论，而是结构化 proposal。里面会包含 addEntities、updateEntities、deleteEntities、addRelationships、updateRelationships、deleteRelationships 这些变更。前端会展示变更摘要、每类变更数量，以及完整 JSON。

这里延续了我对 AI 工程化的判断：AI 可以提高建模效率，但不能绕过审查直接变成不可控修改。尤其是业务模型会影响后续研发、测试和产品理解，所以它必须有证据、有 diff、有人工确认和回滚空间。

这也是我把多智能体协同内容收敛到 Evidence 里的原因：我不想把它讲成一个抽象的 Agent 平台，而是落在一个具体建模工具里，让 AI 的作用变成建模加速器和证据生成器。

---

## 12:30 - 13:40 HATEOAS 经验在 Evidence 中的沉淀

虽然简历里我把 HATEOAS 资源契约单独作为一个项目讲，但 Evidence 其实也吸收了这套经验，只是它不是主角。

HATEOAS 项目解决的是企业 SaaS 多端、多状态、多角色下的规则漂移问题，让前端从解释状态机转向消费后端资源动作契约。

Evidence 里我更多把这套方法变成一种 API 设计习惯：前端从 API root 开始拿资源，通过资源关系进入用户、工作区、图谱和实体集合。这样 Web 和 Desktop 共用前端时，不需要在各处写死路径，也更容易让资源模型随着后端演进。

但是在简历表达上，我会把 HATEOAS 项目重点放在资源动作契约，把 Evidence 项目重点放在本地文件模型、Canvas、Tauri 和 AI proposal。这样两个项目不会重复，而是形成方法论和平台实践之间的关系。

---

## 13:40 - 14:30 项目难点与取舍

这个项目里我觉得比较有价值的取舍有三个。

第一个是文件模型和数据库的取舍。文件模型可读、可审查、AI 友好，但查询和并发弱；数据库查询强，但容易把模型资产锁在系统内部。我的选择是文件作为 source of truth，数据库作为运行态和未来索引层。

第二个是通用 Canvas 和领域 Canvas 的取舍。通用 Canvas 灵活，但业务语义弱；领域 Canvas 限制更多，但能把履约建模方法固化下来。Evidence 选择后者，因为它不是白板，而是业务建模工具。

第三个是 AI 自动化和人工审查的取舍。完全自动化看起来很酷，但风险不可控。proposal-first 稍微慢一点，但更适合业务建模这种需要权责清晰和可追溯的场景。

---

## 14:30 - 15:00 收尾总结

如果总结 Evidence 对我的意义，我会说它不是一个单点功能项目，而是我把几条经验合在一起的一次平台实践。

它把低代码和 SaaS 项目里沉淀的 Schema 思维、HATEOAS 项目里的资源契约思维、Obsidian 这类工具里的本地优先思维，以及 AI 工程化里的 proposal 和 evidence 思维组合到了一起。

最终目标是让复杂业务不再只停留在文档和口头共识里，而是变成一套可以被版本管理、被可视化、被审查、被 AI 辅助演进的模型资产。

所以如果面试官问我这个项目体现什么能力，我会说它体现的是复杂系统抽象能力、前端平台工程能力、Rust/Tauri 全栈落地能力，以及对 AI 参与软件交付后“可控性”和“证据链”的判断。

---

# 如果时间不够的 5 分钟压缩版

如果只给 5 分钟，我会这样讲：

Evidence 是一个本地优先的业务履约建模平台，可以理解成面向业务建模场景的 Obsidian。它参考 Obsidian 的 Vault、Canvas、Properties 和 Graph View，但核心对象不是笔记，而是业务里的 Evidence、Participant、Role 和 Context。

项目背景是复杂业务里的合同、履约请求、履约确认、参与方和权责关系，如果只靠 PRD 和流程图，很难长期维护，也不方便审查、回滚和 AI 读取。所以我把模型源设计成 `.evidence` 目录下的 YAML 文件，实体放在 entities，关系放在 associations。这样模型可以被 Git 管理、Diff 审查，也可以被 AI 工具读取。

架构上，前端是 React + Vite，Canvas 用 React Flow 和 ELK；后端是 Rust Axum，负责把 YAML 文件投影成 Workspace、Diagram、LogicalEntity、Relationship 等领域资源；桌面端用 Tauri 启动本地 Axum API 和 SQLite，Web 和 Desktop 共用同一套 React 前端。

前端最难的是 Canvas 自动布局。普通图布局无法表达履约语义，所以我先识别 RFP、Proposal、Contract、Fulfillment Request、Fulfillment Confirmation 这些阶段，再把它们放到合约前上下文、合约上下文和多条履约泳道里。Role 放上方，Participant 放下方，同一参与方在多个泳道里会用 reference node 投影，减少跨层连线。

AI 侧我采用 proposal-first。用户输入自然语言需求后，后端通过 Pi RPC 调用受控工具读取和修改 `.evidence` 模型目录，前端用 SSE 展示 reasoning、tool call、tool execution 和最终 proposal。AI 不直接越过用户修改模型，而是输出 add/update/delete entities 和 relationships 的结构化建议，保留人工审查和回滚边界。

这个项目最能体现的是我把业务建模、前端 Canvas、Rust/Tauri 全栈、本地优先和 AI 可控协作结合起来的能力。它不是一个画图工具，而是把复杂业务知识沉淀成可版本化、可视化、可审查、可被 AI 辅助演进的模型资产。

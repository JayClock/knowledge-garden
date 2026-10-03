---
title: 项目介绍：企业级类 Figma AI 设计与应用生成
sources:
  - "[[1.D2C!T2UI 全链路拆解、AI 设计生成引擎原理与项目初始化]]"
  - "[[2.可视化编辑器全栈开发、Agent 面板、 DSL 数据内核层设计]]"
  - "[[3.基于 Codex 多智能体引擎、Harness 内核架构与设计产物自验证落地]]"
  - "[[4.MCP 设计资产接入、服务端开发与多端交付及面试实战复盘]]"
  - "[[企业级类 Figma AI 设计与应用生成引擎架构设计与实践面试专项突击]]"
date: 2026-08-21 18:03:37
updated: 2026-10-03 13:09:50
---

# 项目介绍：企业级类 Figma AI 设计与应用生成

## 30 秒开场

这是我在鼎歆独立从 0 到 1 做的内部设计契约平台，连接产品设计与前端实现。我用设计 DSL 表达图层、布局、样式、变量和资产关系，再由 Agent、Canvas 编辑器、导入链路与只读 MCP 共同消费。当前核心交付是可编辑设计文档与桌面端；MCP 可辅助外部 Agent 生成 React 组件，后续可进一步演进端到端代码生成与双向同步。

## 1 分钟项目介绍

这个项目服务于公司内部的产品设计和前端协作。传统截图或口头交接只保留表面结果，图层、布局、Design Variables、资产和组件关系都会丢失，所以我先把这些意图固化为设计 DSL，作为产品设计与前端共同审核和消费的中间契约，没有让模型直接生成最终代码。

项目由我独立从 0 到 1 完成。一次任务先由 Coordinator 拆分页面区域，最多 5 个 Collaborator 并行生成各自的 Fragment；共享 Design Variables 和 Schema 统一结构，写入时再用串行合并和 revision 检查避免覆盖。生成后，Visual Harness 会通过截图定位问题节点，做局部修复，最多两轮。

AI 运行时早期接入 Codex CLI，后来迁移到内置 Pi SDK Agent Runtime。当前交付的是设计 DSL、可编辑设计文档和桌面端链路；外部 Agent 可以通过 MCP 读取设计并生成 React 组件，后续可继续拓展内置双向同步机制。

## 5 分钟主讲法

### 1. 为什么先建立设计契约

这个项目服务于公司内部的产品设计和前端协作。我把 D2C 的难点理解成设计语义重建：截图只剩像素，图层、布局规则、设计变量、资产和组件关系已经丢失；模型即使生成了能运行的代码，也未必保留产品设计意图，后续很难编辑和验证。

所以我先建立“自然语言／导入资产 → 设计 DSL → 可视化编辑 → 验证修复 → 前端消费”链路。DSL 是双方可检查的中间契约，模型只生成候选，Schema、revision、Visual Harness 和人工确认共同控制写入；当前先把可编辑的 L1 设计文档和消费接口做稳。

### 2. 我的职责和架构

这是我个人从 0 到 1 独立完成的内部研发工具。我负责需求分析、架构和核心实现。系统分成设计 DSL 与编辑器、Agent 生成与 Visual Harness、MCP 接入和 Electron 桌面交付四层，共用同一份设计结构。生成结果必须能继续编辑、验证和保存，失败也要能定位到具体阶段。

### 3. DSL 和编辑器

DSL 中有 Frame、Rectangle、Ellipse、Icon 和 Text 等节点，布局、样式、变换和 Design Variables 分开建模。TypeScript 的可辨识联合负责开发期约束；原生 JSON、Pencil 和 Figma 导入会先规范化，再经过 Zod / Schema 与运行时校验。

编辑器采用 Canvas + React 三栏结构，文档、选择和交互状态由单一数据源与发布订阅同步。命令模式和不可变数据支持历史栈与事务撤销；交互层完成单选、多选、框选、拖拽草稿、Esc 取消、跨容器 reparent、Auto Layout、基础节点吸附，以及图层重命名／隐藏／锁定和多选批量属性编辑。

### 4. Agent 生成和一致性

早期我用 Codex CLI Provider 验证模型调用、结构化输出和进程取消。后来迁移到内置 Pi SDK Agent Runtime，由短生命周期 AgentSession 管理模型、工具、事件、取消和资源释放。

生成时先形成 DesignWorkflowPlan，再由 Coordinator 产出共享 Design Variables 并拆成最多 5 个不重叠区域。每个 Collaborator 只生成自己 ownership 范围内的增量 DesignPatch；应用前检查操作合法性、Schema、越权和 baseRevision。Agent 面板中的 create / update / delete / reparent 操作使用 pending / applied / rejected 状态，让用户确认后再写入。单个 Worker 失败会保留 placeholder，其他区域继续生成。

Generation Run 状态机记录准备、生成、验证、修复和最终结果，Run 与 Thread 历史持久化支持断点恢复和历史回溯，UI 的进度与错误直接来自这些状态。

### 5. Visual Harness

Schema 能判断字段和节点关系是否合法，但看不出文本溢出、区域错位、层级混乱或对比度不足。所以文档组装后，我会截图交给多模态模型检查，并把问题绑定到具体 nodeId。

修复只替换问题节点，节点 ID 保持不变，之后重新截图验证。默认最多两轮，因为生成式修复不保证越改越好。超过上限就保留当前文档和问题，让用户接管。

### 6. MCP 和桌面端

MCP 只开放应用状态、选中节点、节点数据、截图和资产五类读取工具。写入还涉及事务、冲突、撤销和回滚；这些机制没有补齐前，外部 Agent 不能直接改文档。

MCP Server 运行在 Sidecar 中，通过 Stdio 接入 Agent，再通过 Bridge 访问 Electron 应用。macOS 使用 Unix Domain Socket，Windows 使用 Named Pipe。Bridge 统一处理超时、消息大小和应用未启动等情况。

Electron 分成 Main、Preload 和 Renderer。Sidecar 与 Schema 通过 `extraResource` 打包，运行时从 `process.resourcesPath` 解析。项目完成 macOS / Windows 双平台 package / make 与可运行安装包输出。

### 7. 交付边界

当前完成了设计 DSL、Canvas 编辑器、命令历史、多选与基础吸附、Plan / DesignPatch / Revision、多 Agent 分区生成、Generation Run、Visual Harness、只读 MCP、Bridge 和 macOS / Windows 桌面交付。核心产物是可继续编辑的 L1 设计文档。

只读 MCP 已能把选中节点、截图和资产交给外部 Agent，辅助生成 React 组件；内置完整页面代码和 Design 与 Code 双向同步作为后续演进方向。

## 高频追问

### 如果面试官问：为什么不让大模型直接生成代码？

大模型可以直接生成代码，问题是输出空间太大。同一个页面可以对应很多种 DOM、组件和样式组织方式，没有稳定的中间表示，后面很难编辑、比较和验证。

设计 DSL 把输出先收敛成受 Schema 约束的数据。编辑器、运行时校验、视觉检查和后续代码映射都围绕这份结构工作。当前阶段先把 L1 设计资产做稳，而不是一步跳到最终代码。

### 如果面试官问：为什么 AI 不能直接修改设计文档？

我把生成链路拆成 Plan → DesignPatch → Revision。Plan 先固定 Variables、模块和 ownership；DesignPatch 只提交增量操作，应用前检查操作类型、Schema、越权和 baseRevision；成功后才生成新 Revision。

对话面板里的 create、update、delete 和 reparent 操作还会先进入 pending，用户选择应用或拒绝后再变成 applied / rejected。这样 LLM 负责提出候选变更，规则引擎和用户共同掌握最终写入权。

### 如果面试官问：编辑器的撤销重做和多选怎样实现？

文档修改统一走纯函数命令，不允许 Canvas、图层面板或属性面板直接维护各自副本。历史栈保存 past / current / future，并用事务把一次拖拽过程合并成一条记录，所以 Ctrl+Z 只撤回一次完整拖拽。

选中状态使用 Set 管理，支持单选、Shift 加选／减选和框选；属性面板检测多选节点的混合值，再批量提交同一属性修改。文档、选择和交互草稿分开存储，通过发布订阅保持多视图一致。

### 如果面试官问：为什么 AI 运行时从 Codex CLI 迁移到 Pi SDK？

Codex CLI 适合快速验证本地模型调用、结构化输出和多 Agent 编排，但产品层还要自己处理命令参数、JSONL 事件、进程退出、取消和本地安装依赖。

迁移到内置 Pi SDK Agent Runtime 后，我可以通过 AgentSession、自定义工具和统一事件订阅直接接入桌面产品，并明确控制工具权限、超时、取消、资源释放和产品状态映射。Runtime 仍保持短生命周期和隔离边界。

### 如果面试官问：为什么用多 Agent，不用一个 Agent？

复杂页面由一个 Agent 串行生成时，上下文会越来越长，一处失败也容易导致整页重做。按不重叠区域拆分后，每个 Collaborator 只处理自己的 Fragment，失败可以留在局部。

代价也很明确：风格可能漂移，区域可能冲突，合并顺序也会影响结果。所以我同时加入共享 Design Variables、区域归属、固定顺序、revision 检查和最终验证。没有实测倍数，我只说明它缩短了架构上的关键路径。

### 如果面试官问：多 Agent 怎样避免相互覆盖？

规划阶段先为每个 Assignment 固定 agentId、regionId、区域和顺序。Collaborator 只生成自己的 Fragment，不直接修改完整文档。

结果由组装器串行写入，并检查当前 revision。版本不符合预期时不能静默覆盖，需要停止、合并或重试。局部写完以后还会验证完整文档。

### 如果面试官问：Visual Harness 和普通 Schema 校验有什么区别？

Schema 检查的是字段、类型和节点关系，不能判断文字是否溢出、区域是否错位、颜色对比是否合理。

Visual Harness 负责视觉层：先截图，再输出绑定 nodeId 的结构化问题，然后只修复对应节点并重新验证。两层检查分别处理结构合法和视觉可用，不能互相替代。

### 如果面试官问：为什么修复最多只做 2 次？

生成式修复不保证单调收敛，修好一个问题可能带来另一个问题。没有上限就可能一直消耗资源，甚至越修越乱。

所以每次只允许修改指定节点，改完重新验证，最多两轮。超过上限就保留当前结果和剩余问题，交给用户判断。

### 如果面试官问：MCP 和 Function Calling 有什么区别？

Function Calling 通常属于某个模型 API；MCP 是工具提供方和 Agent 客户端之间的协议，包含能力发现、输入 Schema、调用方式和工具语义，也支持 Stdio 这类本地进程接入。

这个项目需要让本地 Agent 读取桌面应用里的设计资产，所以 MCP 更适合作为标准接入层，也能让工具实现和具体 Agent Runtime 解耦。

### 如果面试官问：为什么 MCP 只读？

设计文档是核心资产。开放写入除了权限，还要处理事务、并发冲突、撤销和回滚。当前 MCP 的主要任务是读取节点、截图和资产，只读已经覆盖设计理解场景。

写入仍走编辑器现有的文档更新和 revision 路径。如果以后开放 MCP 写入，应该先补齐确认、事务、撤销和回滚，不能让 Agent 直接改文档。

### 如果面试官问：为什么需要 Bridge 和 Sidecar？

MCP Server 由 Agent 客户端作为独立进程启动，设计状态却在 Electron 应用里，两边的生命周期和权限不同。Sidecar 一侧接收 Stdio MCP 请求，另一侧通过本地 Socket 请求桌面应用，本身不保存业务状态。

Bridge 把 macOS 的 Unix Domain Socket 和 Windows Named Pipe 封装成统一接口，同时处理超时、大小限制和应用未启动等异常。这样协议、跨平台通信和编辑器状态不会混在一起。

### 如果面试官问：Electron 打包 Sidecar 有什么坑？

主要是可执行文件和资源路径。Sidecar 不能放在 ASAR 里直接运行，所以要通过 `extraResource` 单独打包；开发环境和打包后的路径也不同，生产环境要从 `process.resourcesPath` 解析。

macOS 和 Windows 需要各自的 Sidecar 二进制和 Maker。项目通过 Electron Forge 完成双平台 package / make、`extraResource` 资源打包和安装包验证。

### 如果面试官问：这个项目为什么可以叫“企业级”？

这里的“企业级”指工程约束，不是客户规模。项目有统一 DSL、运行时校验、状态机、并发控制、Run 历史持久化、视觉门禁、进程隔离、错误分级和桌面打包链路，它不是一次性的 Prompt Demo。定位上属于内部研发工具，核心价值在于工程架构的完备性与可扩展性。

### 如果面试官问：你个人到底做了哪些部分？

这个项目是我个人从 0 到 1 独立开发。我负责四层架构，以及 DSL、Canvas 编辑器、命令历史、Plan / DesignPatch / Revision、Codex CLI Provider、后续 Pi SDK Agent Runtime、多 Agent 编排、Generation Run、Visual Harness、MCP、Bridge、Sidecar 和 macOS / Windows 桌面交付。

当前核心产物是 L1 设计 DSL 和可编辑设计文档；MCP 可辅助外部 Agent 生成选中设计对应的 React 组件，内置完整页面代码生成和 Design 与 Code 双向同步作为后续演进方向。

### 如果面试官问：项目还有哪些不足？

最大的演进空间是核心产物目前聚焦于 L1 设计 DSL：外部 Agent 已可借助 MCP 生成选中 Frame 对应的 React 组件，后续内置 L2 组件代码、L3 完整页面和双向同步可继续深化。`.fig` 导入对 Auto Layout 属性、不支持节点以及样式去重和 Design Token 提取也还有优化空间。

后续继续演进时，先稳定 DSL 和编辑器，再扩展内置代码生成与回读，不断完善真实设计任务的端到端体验。

## 如果面试官问：为什么这是可恢复的渐进式 AI 架构？

我没有把模型输出当成系统唯一结果，而是先建立设计 DSL、可编辑文档、Canvas 编辑器和命令历史。多 Agent、Visual Harness 与 MCP 都在这份稳定结构上增强能力：Agent 只提交受 ownership 和 revision 约束的增量，视觉修复只替换问题节点并限制两轮，超过上限保留当前文档和 Run 历史交给用户。

因此 AI 失败是局部生成或修复失败，不应该抹掉用户已经拥有的设计资产。在架构上保证了即使 AI 生成不理想，系统仍具备完整的状态回滚与可编辑兜底能力。

## 收尾句

这个项目让我把复杂前端继续延伸到了 AI 生成系统。模型负责理解需求和生成候选内容，DSL、Schema、状态机、revision、进程边界和质量门禁负责把结果收住。当前核心交付是可编辑设计文档；MCP 辅助的外部组件生成已经打通，产品内置完整代码生成和双向同步仍是后续方向。

---
title: 项目介绍：企业级类 Figma AI 设计与应用生成
date: 2026-08-21 18:03:37
updated: 2026-10-20 15:56:22
---

# 项目介绍：企业级类 Figma AI 设计与应用生成

## 提取词

设计契约DSL ｜ Canvas命令历史与撤销 ｜ 多Agent分区与revision ｜ Visual Harness视觉门禁 ｜ 只读MCP与桌面交付

## 项目介绍

这个项目服务于公司内部的产品设计和前端协作。传统截图或口头交接只保留表面结果，图层、布局、Design Variables、资产和组件关系都会丢失，所以我先把这些意图固化为设计 DSL，作为产品设计与前端共同审核和消费的中间契约，没有让模型直接生成最终代码。

项目由我独立从 0 到 1 完成。一次任务先由 Coordinator 拆分页面区域，最多 5 个 Collaborator 并行生成各自的 Fragment；共享 Design Variables 和 Schema 统一结构，写入时再用串行合并和 revision 检查避免覆盖。生成后，Visual Harness 会通过截图定位问题节点，做局部修复，最多两轮。

AI 运行时采用内置 Pi SDK Agent Runtime，由短生命周期 AgentSession 管理模型、工具和取消。针对外部 Agent，我封装了只读 MCP Server，通过 Sidecar 与本地 Socket 与 Electron 桌面端通信，提供节点数据、截图和设计资产提取，辅助外部 Agent 生成 React 组件。当前交付的是设计 DSL、可编辑设计文档和桌面端链路，打通了从自然语言到可编辑设计资产的高确定性工程闭环。

## 简历描述

**AI D2C 设计引擎全栈开发 / 架构设计**

* **技术栈**：TypeScript、React 19、Tailwind CSS、Canvas、Electron、Pi SDK Agent Runtime、MCP（Stdio）、Unix Socket / Windows Named Pipe、Electron Forge、Electron Fuses、Nx + pnpm
* **项目简介**：独立设计并开发面向内部产品设计与前端协作的桌面端 AI 设计生成工具，采用“编辑器内核 / Agent 生成 / MCP 接入 / 多端交付”四层架构，产出设计 DSL 与可编辑设计文档。
* **工作内容与成果**：
  * **DSL 内核设计**：以设计 DSL 统一图层、布局、设计变量和资产关系，连接 Agent 输出、Canvas 编辑器与只读 MCP 消费，形成产品设计与前端实现共同使用的设计契约。
  * **编辑器内核开发**：基于 React 19 与 Canvas 实现图层树、属性面板、缩放平移、多选框选、拖拽、Auto Layout、批量属性与撤销重做，支持生成后的持续编辑。
  * **多智能体系统设计**：基于内置 Pi SDK Agent Runtime 编排 Coordinator 与最多 5 个 Collaborator；按区域并行生成 Fragment，以共享 Variables、ownership、revision 和串行合并队列控制写入一致性。
  * **视觉验证与局部修复**：实现 Visual Harness 的 validate → repair → revalidate 流程，通过截图定位具体 nodeId 并局部修复问题节点，默认最多两轮。
  * **MCP 标准化接入**：实现只读 MCP Server、Stdio Sidecar 与跨平台 Bridge，使用 Unix Socket / Windows Named Pipe 访问 Electron 编辑器状态，向外部 Agent 提供节点、截图和资产，辅助生成 React 组件。
  * **工程化与多端交付**：完成 Electron 三入口构建、extraResource 原生资源打包与 Fuses 安全加固，处理 Sidecar 开发及生产路径差异，输出 macOS / Windows 可运行安装包。

## 可能追问

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

### 如果面试官问：为什么这是可恢复的渐进式 AI 架构？

我没有把模型输出当成系统唯一结果，而是先建立设计 DSL、可编辑文档、Canvas 编辑器和命令历史。多 Agent、Visual Harness 与 MCP 都在这份稳定结构上增强能力：Agent 只提交受 ownership 和 revision 约束的增量，视觉修复只替换问题节点并限制两轮，超过上限保留当前文档和 Run 历史交给用户。

因此 AI 失败是局部生成或修复失败，不应该抹掉用户已经拥有的设计资产。在架构上保证了即使 AI 生成不理想，系统仍具备完整的状态回滚与可编辑兜底能力。

---
date: 2026-04-15 18:10:00
updated: 2026-05-15 10:03:23
share: true
---

# Routa Desktop 项目独立描述（AI-First Builder 视角）

 项目定性

Routa Desktop 最适合从 AI-First workflow 的角度来讲。它不是一个普通桌面版 AI 聊天工具，而是一个面向软件交付场景的本地优先 Builder runtime：Builder 和 AI 从任务理解、上下文准备、方案分析、代码实现、审查验证到结果回收，始终围绕同一套本地上下文和审计链路协作。

 最贴近招聘要求的一句话

这个项目最能体现的，不是“我接了一个 AI API”，而是“我在 AI 参与完整研发链路的前提下，负责给 AI 建立上下文、编排执行过程、审查输出结果，并把缺失信息持续补回系统”。

 为什么这个项目和 AI-First workflow 强相关

过去很多 AI Coding 场景，本质上还是“人提问，模型回答”，上下文大多停留在聊天里。但真实研发不是这样：从业务目标、需求理解、系统依赖到代码改动、验证结果，这些信息如果不能稳定传递，AI 就很容易在同一个地方反复出错。

Routa Desktop 解决的核心问题，就是把这些原本分散的信息变成可持续协作的系统对象：

- 用 `workspace`、`codebase`、`worktree`、`session` 承接任务上下文
- 用 `ACP` 统一编排不同 Agent runtime
- 用 `trace`、`review`、`fitness` 监测和审查 AI 的实际输出
- 当 AI 反复犯错时，把缺失上下文补回到文档、规则、specialist、评审和验证链路里

所以它特别贴合 Builder 这个角色：Builder 不是被动等 AI 出结果，而是主动把 AI 变成“这个问题的临时专家”，然后再对结果负责。

 我在这个项目里最能体现 Builder 能力的部分

 1. 在代码实现前补足上下文

Builder 最重要的工作，不是马上让 AI 写代码，而是先把 AI 理解问题所需要的上下文准备好。

在这个项目里，这件事对应的是：

- 用 `workspace` 作为顶层边界组织任务上下文
- 用 `codebase`、`worktree` 明确代码仓库和执行副本
- 用 `session` 承接一次执行线程，而不是把所有信息留在临时对话里
- 用显式对象而不是口头记忆去管理 `artifact`、`review`、`trace`

这本质上是在做 context engineering，而不是单纯 prompt engineering。

 2. 把模糊问题拆成 AI 能执行的步骤

AI 擅长生成，但不天然擅长理解复杂系统里的隐含边界。Builder 需要先把问题拆解成 AI 能消费的步骤和上下文块。

这个项目里，这种能力体现在：

- 用本地 runtime 组织执行边界，而不是让 AI 直接操作一堆隐式本地状态
- 通过 `ACP` 把不同 provider 的执行过程归一化
- 让 session lifecycle、stream event、trace record 有统一结构
- 把运行时、Docker、sandbox、binary、workspace scope 这些复杂依赖收敛到本地控制面里

 3. 对 AI 输出做审查和审计

招聘里强调要知道 AI 什么时候是对的，什么时候需要干预。这个项目最强的一点，就是没有把 AI 输出当成“自然正确”，而是围绕输出建立了专门的审查和追踪能力。

- `trace` 记录 session 生命周期、消息流、工具调用、文件变更和 Git 上下文
- `review` 负责把问题、严重级别和验证结论结构化沉淀下来
- `entrix` + `docs/fitness` 把质量要求变成可执行门禁，而不是只靠人工感觉

也就是说，AI 不是“写完就结束”，而是“写完之后进入审查和验证闭环”。

 4. 当 AI 重复犯错时，把缺失上下文补回系统

这点和招聘要求非常贴：如果 AI 总是在同一个地方出错，问题往往不只是模型能力，而是上下文缺失。

在这个项目里，我更看重的是这种反馈闭环：

- 不是反复在聊天里纠正 AI
- 而是把缺失信息沉淀回 `docs`、架构文档、ADR、fitness 规则、specialist 工作流和 review 机制
- 让后续同类任务不再依赖某个工程师临时记忆兜底

这其实就是 Builder 心态最重要的一部分：不只交付一次结果，还要降低系统下一次犯同类错误的概率。

 Desktop 侧的技术落点

虽然这份经历可以从 workflow 角度讲，但它落地不是空的，desktop 侧有很明确的技术实现：

- `Tauri` 承载桌面 UI
- 内嵌 `Axum` 服务，作为本地 API 和执行控制面
- `AppState` 统一装配 workspace、codebase、worktree、ACP session 等本地状态
- `AcpManager` 和 `crates/routa-core/src/acp/` 负责 ACP 编排
- `SQLite + 文件系统 + JSONL trace` 承担本地持久化与恢复
- `Docker`、`sandbox`、runtime warmup、registry 负责本地执行基础设施

所以这不是“前端接个 AI”，而是做一个本地优先的 AI 协作控制平面。

 这个项目最贴合 JD 的能力点

- 复杂问题拆解：要把 provider 差异、运行时边界、上下文作用域、验证链路拆成 AI 可执行的结构
- 批判性思维：不能默认 AI 输出正确，必须通过 trace、review、fitness 去验证
- 责任感：对 AI 生成代码和最终发布结果负责，不把问题甩给模型
- 沟通能力：要把复杂上下文压缩成 AI 和团队都能理解的明确结构
- 快速学习能力：需要快速理解本地 runtime、协议编排、审计链路和软件交付治理

 适合在面试里怎么定性

> Routa Desktop 这段经历最适合讲成一个 AI-First Builder 项目。我做的不是单纯让模型写代码，而是围绕软件交付全过程，建立一套本地优先的上下文协作、ACP 编排和执行审计机制。我的核心价值在于：先帮 AI 成为当前问题的专家，再对它的输出负责，并把反复暴露的问题沉淀回系统。

 简历描述精简版

- 参与设计并实现本地优先的 AI-First desktop runtime，围绕 `workspace`、`codebase`、`worktree`、`session`、`trace`、`review` 建立统一上下文模型，支撑 Builder 与 AI 的持续协作。
- 基于 `Tauri + Rust/Axum + ACP` 构建本地控制平面，统一多 provider Agent runtime 的 session lifecycle、stream event 和 trace record。
- 参与执行审计、规则验证和反馈闭环建设，通过 `trace`、`review`、`fitness` 和文档沉淀持续补齐 AI 缺失上下文，提升交付可靠性。

 30 秒口述版

> 这个项目我会把它定义成一个 AI-First Builder desktop runtime。核心不是做桌面聊天，而是让 Builder 和 AI 围绕同一套本地上下文协作：先用 `workspace`、`codebase`、`session` 这些对象把问题背景组织起来，再用 `ACP` 编排不同 Agent 的执行过程，最后通过 `trace`、`review`、`fitness` 去审查和审计输出。如果 AI 在同一个地方反复出错，我们就把缺失信息补回文档和规则里，让后续任务更稳定。

 一句收口

> 如果一句话收口，我会把 Routa Desktop 定义成一个帮助 Builder 与 AI 完成完整交付闭环的本地控制平面：负责上下文准备、ACP 编排、输出审计，以及缺失上下文的持续沉淀。
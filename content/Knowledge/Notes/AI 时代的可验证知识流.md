---
title: AI 时代的可验证知识流
aliases:
  - AI 时代全流程序员设计可验证知识流
type: 知识卡
card_type: 模型
up:
  - "[[全流程序员]]"
  - "[[AI Coding Agent 工程实践]]"
sources:
  - "[[Knowledge/Sources/为什么要成为全流程序员，而非全栈程序员？|为什么要成为全流程序员，而非全栈程序员？]]"
  - "[[Knowledge/Sources/AI 时代的软件工程/03｜通过知识过程重新理解软件工程-徐昊 · AI时代的软件工程-极客时间|通过知识过程重新理解软件工程]]"
  - "[[Knowledge/Sources/Agent 设计模式之美/00｜把一千个真实工程问题变成 28 个设计模式-Agent 设计模式之美-极客时间|把一千个真实工程问题变成 28 个设计模式]]"
  - "[[Knowledge/Sources/Agent 设计模式之美/04｜逆向五步法（上）：如何把 Agent Harness 拆成工程地图-Agent 设计模式之美-极客时间|逆向五步法（上）：如何把 Agent Harness 拆成工程地图]]"
date: 2026-07-25 15:12:17
noteId: 1784964381102
updated: 2026-08-06 16:37:07
---
# AI 时代的可验证知识流

> [!abstract] 核心观点
> AI 降低生成成本后，交付系统需要用 Stage State、Assignment、Evidence 和 Gate 持续追踪上下文、约束、处理权与责任。

AI 显著降低了代码、测试和文档的生成成本，但“做出来”变便宜后，“做的是不是正确的事、是否符合团队约束、能否安全进入下一阶段”会成为主要成本。若上下文仍散落在人的经验和聊天记录中，AI 只会更快地产生难以消费和审查的大规模改动。

[[中心化 Agent 委派的阶段授权瓶颈]]说明，仅增加 Planner、Builder、Tester 或 Reviewer 等执行分支，并不会自动提高端到端吞吐。可验证知识流需要同时改变协作对象：阶段状态共享当前位置，Assignment 决定当前由谁处理，Evidence 决定是否满足退出条件，Gate 则承载授权和风险判断。

## 外层阶段循环

| Stage | 主要 Evidence | 退出 Gate |
| --- | --- | --- |
| Kickoff | Story Card、问题边界和来源版本 | Story Authority |
| Understand | Scenario / Model | Scenario / Model 已足以支持规划 |
| Tasking | Plan / Q1 / Q2 | Approved Plan |
| Pair | Execution / Test、可验证增量 | Quality / Increment |
| Showcase | Observation / Decision | Accept |
| Respond | Knowledge / Probe | Promotion / Probe |

Evidence 不只是阶段末尾附上的报告，而是下一阶段的输入接口。每份提交、决定和交接都应携带 Actor、Role、Stage 与 Revision，使下游能够直接[[知识消费|消费证据]]。Concern 可以让工作返回 Understand、Tasking 或 Pair；Respond 产生的新 Probe 则进入下一轮 Story 候选。

## 阶段内短循环

外层循环控制知识如何跨阶段流动，各阶段内部仍需要快速反馈：Kickoff 对齐并冻结 Story，Understand 通过提问、场景和模型消除歧义，Tasking 切片并 Desk Check，Pair 运行 Red–Green–Refactor，Showcase 观察、评价并决策，Respond 分类、提升知识并形成 Probe。

因此，流程既不能退化为一次线性瀑布，也不能只剩无边界的 Agent 自循环。短循环负责快速纠偏，Evidence Gate 负责确认何时可以把结果交给下游。

## Human 与 Agent 的责任和处理权

从交付系统看，Human 和 Agent 都可以被建模为承担 Stage Role 的成员实例。谁在当前阶段处理任务，应由 Capability、Assignment、Authority、职责分离、有效期和升级策略决定，而不是由“人或 AI”的身份预先固定。

- **Human 保留**问题价值、冲突取舍、高风险审批和组织最终问责。
- **Agent 可以承担**检索、分析、计划、编码、测试、评价或运行操作，只要任务位于明确的 Policy 和 Evidence Gate 内。
- **Handoff / Takeover**处理角色接力；Concern、越权或证据不足触发 Escalation 与人工接管。

这一区分允许 Agent 在低风险、可验证的阶段内自主处理，又不会把最终责任伪装成模型能力。人不必逐项确认所有低风险操作，但必须设计授权边界、证据要求和升级条件。

其中，团队需要把关键经验沉淀为能够直接参与工作的知识：业务概念和规则、领域模型、验收示例、架构约束、任务模板、接口契约、测试策略、工具权限、检查清单和评审规则。它们不只是供人阅读的文档，还应能够约束计划、生成、测试和发布。

当这些知识需要围绕 Agent 持续生效时，[[Harness Engineering 的可执行知识流|Harness Engineering]] 负责把它们装配为项目规则、Context、Plan、Tool、Hook、Evaluation、运行证据和人工升级机制，使知识流不只可读，而且可以被执行、检查和追踪。

这也是[[全流程序员的上下文扩展|全流能力]]在 AI 时代的具体落点：贯通[[业务问题的分析与建模|问题定义]]、[[架构与任务分解|任务分解]]、[[测试策略与实现验证|实现验证]]和[[上线运营与反馈验证|运行学习]]，而不是只把编码环节做得更快。

---
title: Harness Engineering 的可执行知识流
aliases:
  - Harness Engineering 把知识流变成可执行交付系统
type: 知识卡
card_type: 概念
up:
  - "[[全流程序员]]"
  - "[[AI Coding Agent 工程实践]]"
sources:
  - "[[Knowledge/Sources/企业级应用中 Harness Engineering 的实践与思考/00｜为什么企业级应用需要 Harness Engineering|为什么企业级应用需要 Harness Engineering]]"
  - "[[Knowledge/Sources/企业级应用中 Harness Engineering 的实践与思考/01｜Workflow：Harness Engineering 的骨架|Workflow：Harness Engineering 的骨架]]"
  - "[[Knowledge/Sources/企业级应用中 Harness Engineering 的实践与思考/02｜文档工程：记忆与知识如何进入 Agent 的 Context|文档工程：记忆与知识如何进入 Agent 的 Context]]"
  - "[[Knowledge/Sources/企业级应用中 Harness Engineering 的实践与思考/03｜Spec：让 AI 在实现前真正理解问题|Spec：让 AI 在实现前真正理解问题]]"
  - "[[Knowledge/Sources/企业级应用中 Harness Engineering 的实践与思考/04｜对抗：让代码经得起审查与验证|对抗：让代码经得起审查与验证]]"
  - "[[Knowledge/Sources/企业级应用中 Harness Engineering 的实践与思考/05｜Agent：不是人格，而是职责边界|Agent：不是人格，而是职责边界]]"
  - "[[Knowledge/Sources/企业级应用中 Harness Engineering 的实践与思考/06｜人：Harness Engineering 的最终责任主体|人：Harness Engineering 的最终责任主体]]"
  - "[[Knowledge/Sources/企业级应用中 Harness Engineering 的实践与思考/07｜Context Window：Harness Engineering 如何管理 Agent 的注意力|Context Window：Harness Engineering 如何管理 Agent 的注意力]]"
date: 2026-07-25 15:22:52
noteId: 1784964381346
updated: 2026-08-06 16:42:02
---
# Harness Engineering 的可执行知识流

> [!abstract] 核心观点
> Harness Engineering 把项目知识、行动边界和验证机制装配到 Agent 周围，使知识流成为可执行、可检查的交付系统。

## 定义

Harness Engineering 不是用一套新术语替代需求工程、架构设计、测试和运维，而是把这些实践产生的知识装配到 Agent 周围，使它能够在真实项目中持续读取约束、执行任务、验证结果并留下证据。

`Agent = Model + Harness`：Model 提供通用能力，Harness 提供当前项目特有的意图、知识、行动边界、验证方式和责任接口。

## 组成

它通常包含以下部分：

- **Prompt 与项目规则**：说明角色、目标、行为边界、输出约定和必须遵守的团队规范。
- **Context、Memory 与 Skill**：提供当前任务所需的业务知识、架构知识、代码状态、历史决策和可复用工作方法。
- **Plan**：在行动前把目标转成可审查步骤，显式记录依赖、完成标准、风险、失败处理和终止条件。
- **Tool**：把 Agent 的能力限制在经过设计的接口内，并根据副作用与可逆性设置权限。
- **Hook 与 Evaluation**：在关键节点运行格式检查、静态分析、测试、语义评审、停止判断和人工升级。
- **Observability**：记录日志、指标、Trace、成本、工具调用和文件变化，使失败可以重放和归因。
- **Human on the Loop**：由人提供意图、价值判断、高风险审批和最终问责，而不是在每个低风险步骤上反复确认。

## 与全流程序员的关系

- 传统软件工程负责产生需求、模型、架构、规范、测试和运营知识；
- [[全流程序员的上下文扩展|全流能力]]负责理解这些知识如何跨环节流动，并降低传递损耗；
- Harness Engineering 负责把这些知识变成 Agent 运行时能够消费和遵守的环境。

## 与传统工程实践的对应

| 工程实践      | 需要固化的知识            | Harness 机制                             | 可检查的证据              |
| --------- | ------------------ | -------------------------------------- | ------------------- |
| 需求沟通与领域建模 | 业务价值、角色、规则、场景和统一语言 | Context、Memory、Skill、Human on the Loop | 问题陈述、领域模型、业务示例      |
| 验收条件与测试策略 | 完成边界、功能上下文和验证路径    | Success Criteria、Evaluator、测试 Hook     | 验收场景、测试结果、需求到测试的证据链 |
| 架构设计与任务分解 | 组件职责、接口、依赖、风险和终止条件 | 项目规则、Plan-before-Act、Fallback          | 架构决策、可审查计划、风险说明     |
| 编码规范与实现评审 | 团队约定、实现示例和质量约束     | `AGENTS.md`、Skill、Tool、Post-Hook       | 代码改动、静态检查、评审记录      |
| 权限与变更管理   | 行动边界、审批节点和回滚要求     | Tool 白名单、权限分级、Pre-Hook、人工审批            | 权限记录、审批决定、操作轨迹      |
| 持续交付与上线运营 | 发布流程、可观测性和恢复策略     | 工作流 Tool、Stop Hook、回滚机制                | 发布记录、运行指标、回滚证据      |
| 复盘与持续改进   | 失败原因、有效经验和规则变化     | Logs、Metrics、Trace、Evaluation、Skill 更新 | 事件复盘、规则更新、下一轮输入     |

Harness Engineering 的价值不只是让模型“更会写代码”，而是让正确的工程实践不再依赖模型临场记忆或自觉。验收条件会成为完成标准，架构和编码规范会进入项目规则与计划，测试策略会进入验证流水线，权限与发布要求会进入工具边界，运行反馈则会沉淀回 Context、Skill 和下一轮任务。

## 适用边界

只有 Prompt 而没有计划、工具边界和验证，仍然只是一次性对话；只有测试而没有业务上下文和架构知识，只能检查已经想到的局部结果；只有自动执行而没有人工价值判断和升级机制，则会把速度转化为风险。完整的 Harness 应与[[AI 时代的可验证知识流|可验证知识流]]一起设计。

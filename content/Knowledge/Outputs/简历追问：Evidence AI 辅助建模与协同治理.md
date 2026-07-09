---
title: 简历追问：Evidence AI 辅助建模与协同治理
date: 2026-07-03 22:00:00
updated: 2026-07-09 10:45:13
tags:
  - interview/follow-up
  - resume/evidence
  - ai
---

# 简历追问：Evidence AI 辅助建模与协同治理

关联：[[全栈工程师简历#Evidence｜本地优先的业务履约建模与 AI 辅助建模平台]]、[[Evidence 项目简历描述与面试话术]]、[[15 分钟：Evidence 面试逐字稿]]、[[Prompt Request 比 Pull Request 更适合 AI 协作]]。

## 对应简历描述

> 集成 AI SDK、SSE 与 Pi RPC，将自然语言需求流式转化为建模 proposal，展示 reasoning、tool call、tool execution 与 JSON 变更摘要；将多智能体协同能力收敛为 Evidence 的建模加速器，并保留人工审查与回滚边界。

## 面试官真正想确认

你是否把 AI 放在可审查、可回滚、可限制的工程边界内，而不是让 AI 直接改核心模型。

## 连续追问链

### 1. 为什么 proposal-first

- 为什么 AI 不直接修改 `.evidence` 模型？哪些风险不可接受？
- proposal 里包含哪些结构：add/update/delete entities、relationships、reason、confidence？
- 用户审查时看摘要、diff、JSON 原文还是 Canvas 预览？
- 应用 proposal 后如何回滚？靠 Git、快照还是操作日志？

### 2. 工具边界

- Pi RPC 启动 agent 时，工作目录如何限制在 `.evidence`？
- read/edit/write/ls/find/grep 这些工具是否足够？为什么不给 shell？
- 如何防止 path traversal、读取用户隐私文件或修改项目代码？
- 多智能体协同时，谁拥有最终写权限？

### 3. SSE 事件流

- AI SDK、后端、Pi RPC、前端之间事件如何转换？
- reasoning、tool call started、tool execution ended、agent ended 分别如何渲染？
- 用户中途取消、工具失败、JSON 解析失败时，前端状态如何收敛？
- 事件顺序和幂等如何保证？刷新页面后还能看到历史过程吗？

### 4. 质量与治理

- proposal 应用前做哪些 schema 校验和关系完整性校验？
- AI 生成的实体命名、id、关系类型如何去重和标准化？
- 如何评估 AI 建模质量？人工审查通过率、返工原因、模型冲突数？
- “多智能体协同平台”为什么要收敛到 Evidence，而不是单独讲一个泛 Agent 平台？

## 场景推演题

> 用户输入：“帮我建模一个办公笔记本采购履约过程，包括询价、报价、合同、支付、发货、开票。”AI 提出删除现有 Contract 并新建一个 Contract。请说明 proposal 展示、风险提示、人工确认和回滚流程。

继续追：如果工具尝试读取 `.evidence/../.ssh/config`，系统在哪里拦截？

## 准备证据

- SSE 事件类型列表。
- proposal JSON 示例。
- 工具白名单和工作目录限制说明。
- 应用 proposal 前后的 diff/review 流程。

## 容易露馅的回答

- “AI 直接改模型，用户看结果。”
- “把工具都开放给 agent，能力更强。”
- “展示 reasoning 就等于可控。”
- “失败了重新生成一次，不需要回滚。”

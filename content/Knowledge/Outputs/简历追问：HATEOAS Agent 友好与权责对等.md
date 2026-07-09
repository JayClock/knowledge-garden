---
title: 简历追问：HATEOAS Agent 友好与权责对等
date: 2026-07-03 22:00:00
updated: 2026-07-09 10:45:13
tags:
  - interview/follow-up
  - resume/hateoas
  - ai
---

# 简历追问：HATEOAS Agent 友好与权责对等

关联：[[全栈工程师简历#HATEOAS 资源契约架构]]、[[HATEOAS 如何用于 Agent 身份治理：以数据分析任务为例]]。

## 对应简历描述

> 动态注册 Agent 可调用工具，意图识别不会超出当前用户权限。基于 template 构建 self-Heal Loop 的 Payload 参数生成，避免出现 HTTP 400 参数错误。

## 面试官真正想确认

你是否能把 Agent 工具边界落到权限、契约、审计和错误修复，而不是只说“把接口给 AI 调”。

## 连续追问链

### 1. 工具从哪里来

- `_templates` 如何转换成 Agent tool schema？字段类型、必填、枚举、描述从哪里来？
- tool name 使用 relation/action name，还是重新设计自然语言名称？如何避免冲突？
- 当前资源没有某个 action 时，Agent 是否能看到这个工具？

### 2. 权限与越权

- “意图识别不会超出当前用户权限”是靠 prompt，还是靠服务端动作契约和二次鉴权？
- 如果模型请求一个当前用户没有权限的动作，是拒绝、解释原因，还是重新规划？
- 破坏性动作是否需要人工确认？确认时展示哪些证据？

### 3. Payload self-heal

- 400 参数错误返回什么结构？字段路径、错误码、期望类型是否可机器读取？
- self-heal loop 如何限制重试次数，避免模型一直猜？
- payload 修复时是否会保留用户原始意图和已确认字段？

### 4. 审计与安全

- 每次 tool call 记录哪些字段：用户、资源、action、payload、结果、reasoning 摘要？
- 和直接从 OpenAPI/Swagger 生成工具相比，HATEOAS 的边界优势是什么？
- prompt injection 让 Agent 调未授权接口时，系统层如何兜底？

## 场景推演题

> Agent 想“帮我审批这张单”，但当前资源只返回 `comment` 和 `reject`，没有 `approve`。请说明工具注册、意图识别、用户反馈和服务端鉴权全过程。

继续追：如果 `reject` 模板要求 `reason` 必填，模型第一次没填导致 400，self-heal 如何修复？

## 准备证据

- 一个 `_templates` 到 tool schema 的映射例子。
- 一个 400 validation error 到二次 payload 的修复日志。
- 一个越权 action 被拒绝的审计记录样例。

## 容易露馅的回答

- “把所有后端接口都注册给 Agent。”
- “让模型判断用户有没有权限。”
- “400 之后让模型重新生成一下就好。”
- “Agent 成功调用接口就代表安全。”

---
title: 简历回答逐字稿：HATEOAS Agent 友好与权责对等
date: 2026-07-03 22:30:00
updated: 2026-07-09 10:45:13
tags:
  - interview/script
  - resume/hateoas
  - ai
---

# 简历回答逐字稿：HATEOAS Agent 友好与权责对等

关联：[[简历追问：HATEOAS Agent 友好与权责对等]]、[[HATEOAS 如何用于 Agent 身份治理：以数据分析任务为例]]。

## 30 秒开场

我说 HATEOAS 对 Agent 友好，核心不是“让 AI 调接口更方便”，而是让 Agent 的可调用动作天然受当前用户和当前资源状态约束。

传统做法是把一堆 OpenAPI 接口注册给 Agent，再靠 prompt 告诉它哪些能调，这个边界很弱。HATEOAS 下，Agent 只看当前资源返回的 `_links` 和 `_templates`。当前用户没有权限、当前状态不可执行的动作，根本不会注册成工具。即使模型尝试越权，服务端也会二次鉴权。

## 如果面试官问：template 怎么变成 Agent tool？

我会这样说：

`_templates` 本身已经描述了动作名、method、href、字段、类型、必填和枚举。把它转成 tool schema 比较自然。

比如资源里有：

```json
"_templates": {
  "reject": {
    "properties": [
      { "name": "reason", "type": "string", "required": true }
    ]
  }
}
```

Agent 侧就只注册一个当前资源可用的 `reject` tool，参数 schema 里 `reason` 必填。工具执行时不是让 Agent 自己拼 URL，而是 SDK 按 relation 对应的 action 提交。

这样 tool 的范围是动态的，跟用户当前看到的资源状态一致。

## 如果面试官追：权限是靠模型判断吗？

我会明确说不是。

模型只能做意图识别和参数生成，不能作为权限系统。权限边界有三层：

第一层，后端只在资源里返回当前用户可执行的 action。第二层，Agent runtime 只把这些 action 注册成工具。第三层，真正提交时后端还是按当前用户身份重新鉴权和校验状态机。

所以即使 prompt injection 让模型说“我要调用管理员接口”，它看不到对应工具；就算绕过工具名构造请求，服务端也会拒绝。

## 如果面试官追：self-heal loop 怎么避免乱重试？

我会这样回答：

self-heal 主要针对 payload 形状错误，不是让模型无限试接口。比如第一次提交 reject 少了 `reason`，服务端返回结构化 400：

```json
{
  "type": "validation_error",
  "fields": [
    { "path": "reason", "code": "required", "message": "请填写驳回原因" }
  ]
}
```

Agent 可以基于这个错误修复 payload，最多重试一到两次。超过次数就停下来，把错误解释给用户，而不是继续猜。

另外，破坏性动作我会加人工确认，比如删除、审批、驳回。确认时要展示资源、动作、payload 和可能影响，而不是只问“是否继续”。

## 如果面试官追：和 OpenAPI 生成工具相比优势是什么？

我会说 OpenAPI 描述的是系统理论上有哪些接口，HATEOAS 描述的是当前用户、当前资源、当前状态下能做什么。

Agent 需要的不是全量能力列表，而是当前上下文里的合法下一步。比如同一个 `approve` 接口，订单 draft 时不能用，pending 时经理能用，普通员工不能用。OpenAPI 很难表达这种资源实例级状态，而 HATEOAS 正好把它放在资源里。

## 如果面试官追：怎么审计？

我会说 Agent 调用业务动作必须记录审计。至少包括：用户身份、资源 id、action relation、payload 摘要、tool call id、请求结果、错误码、人工确认记录。如果有 reasoning，不一定全量保存敏感内容，但可以保存模型给出的操作理由摘要。

这样后面出现问题时，能知道是用户主动确认、Agent 参数生成错误，还是服务端契约返回错误。

## 收尾句

所以我讲 Agent 友好，不是说 AI 可以随便调系统，而是 HATEOAS 把“可用动作”限制在当前资源状态里，让 Agent 的能力边界和用户权限边界天然对齐。

---
title: 简历回答逐字稿：HATEOAS Agent 友好与权责对等
date: 2026-07-03 22:30:00
updated: 2026-08-26 08:30:30
tags:
  - interview/script
  - resume/hateoas
  - ai
---

# 简历回答逐字稿：HATEOAS Agent 友好与权责对等

关联：[[简历追问：HATEOAS Agent 友好与权责对等]]、[[15分钟：HATEOAS 资源契约架构]]。

> [!warning] 回答边界
>
> - 生产成果是 HATEOAS 资源契约、TypeScript SDK 及 PC Web / 移动 Web 消费。
> - 将 `_templates` 动态注册为 Agent tools 是基于现有 SDK 的架构延展，没有上线，不能用“我实现了”来回答。
> - `reject`、`approve` 和订单状态只是机制示例，不是该项目的真实业务证明。

## 30 秒开场

这是一条架构延展，不是生产交付。如果把 Agent 视为新的客户端，它只应该看到当前资源 `_links` 和 `_templates` 中合法的动作，而不是拿到全量接口。模型负责意图和参数，服务端继续负责身份鉴权与状态校验。动态工具注册目前没有上线。

## 如果面试官问：template 怎么变成 Agent tool？

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

Agent 侧就只注册一个当前资源可用的 `reject` tool，参数 schema 里 `reason` 必填。工具执行时由 SDK 按 relation 对应的 action 提交，Agent 不需要自己拼 URL。

这样 tool 的范围是动态的，跟用户当前看到的资源状态一致。

## 如果面试官追：权限是靠模型判断吗？

权限不能由模型判断。模型只做意图识别和参数生成，系统边界有三层：

第一层，后端只在资源里返回当前用户可执行的 action。第二层，Agent runtime 只把这些 action 注册成工具。第三层，真正提交时后端还是按当前用户身份重新鉴权和校验状态机。

所以即使 prompt injection 让模型说“我要调用管理员接口”，它看不到对应工具；就算绕过工具名构造请求，服务端也会拒绝。

## 如果面试官追：self-heal loop 怎么避免乱重试？

这是一个扩展方案。self-heal 只适合处理 payload 形状错误，不是让模型无限试接口。比如第一次提交 reject 少了 `reason`，服务端返回结构化 400：

```json
{
  "type": "validation_error",
  "fields": [{ "path": "reason", "code": "required", "message": "请填写驳回原因" }]
}
```

Agent 可以基于这个错误修复 payload，最多重试一到两次。超过次数就停下来，把错误解释给用户，而不是继续猜。

另外，破坏性动作我会加人工确认，比如删除、审批、驳回。确认时要展示资源、动作、payload 和可能影响，而不是只问“是否继续”。

## 如果面试官追：和 OpenAPI 生成工具相比优势是什么？

OpenAPI 描述的是系统理论上有哪些接口，HATEOAS 描述的是当前用户、当前资源、当前状态下能做什么。

Agent 只需要当前上下文里的合法下一步，不需要完整能力列表。比如同一个 `approve` 接口，订单 draft 时不能用，pending 时经理能用，普通员工不能用。OpenAPI 很难表达这种资源实例级状态，而 HATEOAS 正好把它放在资源里。

## 如果面试官追：怎么审计？

Agent 调用业务动作必须留下审计记录。至少包括：用户身份、资源 id、action relation、payload 摘要、tool call id、请求结果、错误码、人工确认记录。如果有 reasoning，不一定全量保存敏感内容，但可以保存模型给出的操作理由摘要。

这样后面出现问题时，能知道是用户主动确认、Agent 参数生成错误，还是服务端契约返回错误。

## 收尾句

所以这段只能作为架构讨论：HATEOAS 有条件把“可用动作”限制在当前资源状态里，让 Agent 的能力边界与用户权限边界对齐；但动态工具注册、自动修复、人工确认和审计链路都不能说成这个项目已经上线的成果。

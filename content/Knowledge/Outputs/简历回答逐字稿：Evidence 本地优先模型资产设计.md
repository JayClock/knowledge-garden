---
title: 简历回答逐字稿：Evidence 本地优先模型资产设计
date: 2026-07-03 22:30:00
updated: 2026-07-09 10:45:13
tags:
  - interview/script
  - resume/evidence
  - local-first
---

# 简历回答逐字稿：Evidence 本地优先模型资产设计

关联：[[简历追问：Evidence 本地优先模型资产设计]]、[[Evidence 项目简历描述与面试话术]]、[[15 分钟：Evidence 面试逐字稿]]。

## 30 秒开场

Evidence 里我最核心的设计，是把业务履约模型放成本地可读文件，而不是一开始就锁在数据库里。因为这个项目处理的不是普通运行数据，而是业务概念、凭证、参与方、角色、上下文和关系，这些更像长期演进的知识资产。

所以我设计了 `.evidence/entities` 和 `.evidence/associations`。实体和关系都是 YAML，可以被 Git diff、review、回滚，也方便 AI 工具读取。数据库更多保存 workspace、用户、本地运行状态和未来索引，而不是作为模型唯一来源。

## 如果面试官问：为什么不直接用数据库？

我会说数据库当然适合查询和协作，但它会把模型资产变成应用内部黑盒。业务建模资产经常需要被审查、对比版本、脚本批处理，甚至让 AI 读取。如果全部存在数据库里，用户很难直接看到“这次模型到底改了什么”。

YAML 的价值是可读、可 diff、可迁移。它不适合所有场景，所以我的取舍不是“不要数据库”，而是“模型源文件优先，运行态和索引数据库优先”。

## 如果面试官追：entity 和 association 长什么样？

我会这样描述：

一个 entity 可能包含 id、name、label、type、subType、attributes 和 markdown 说明。比如合同是 Evidence 类型，subType 是 contract。支付申请也是 Evidence 类型，但 subType 是 fulfillment_request。

association 文件表达 source、target、relationshipType 和 label。比如 Contract 约束 Payment Request，Payment Request 被 Payment Confirmation 完成。

关键是关系引用稳定 id，而不是文件名或展示名。这样用户重命名 label，不会破坏图谱关系。

## 如果面试官追：YAML 解析失败或关系断了怎么办？

我会说不能因为一个文件坏了就让整个 workspace 白屏。

文件投影层会扫描目录并逐个解析。单个 YAML 解析失败时，可以把它记录成诊断资源，在实体列表或问题面板提示用户哪一行有问题。association 指向不存在的 entity 时，也不要直接丢掉，而是标记成 dangling relationship。Canvas 可以用错误边或诊断提示展示，方便用户修复。

这样用户能修模型，而不是只看到 500。

## 如果面试官追：多人协作和冲突怎么办？

我会说第一阶段 Evidence 更偏本地优先和单人建模，可以借 Git 做异步协作。Git conflict 不能完全避免，但因为模型是文本，至少能看见冲突。

如果后面要做多人协作，我会加数据库索引层、锁或冲突检测。比如同一个 entity 被两个人修改，系统可以基于 version 或 file hash 发现冲突，再提供字段级 diff。长期我仍然倾向 YAML 作为 source of truth，数据库作为 query/index/cache layer。

## 如果面试官追：AI 直接改 YAML 安全吗？

我会说不应该让 AI 无边界地改。AI 可以读取 `.evidence` 模型目录，生成 proposal 或 diff，但最终要经过 schema 校验、关系完整性校验和人工审查。工具目录也必须限制在 `.evidence` 下，防止读取用户其他文件。

另外 YAML 输出要稳定排序，比如 attributes 和 relationships 的顺序尽量确定，避免 Git diff 出现大量无意义变化。

## 收尾句

所以本地优先不是为了炫技，而是因为业务模型是需要长期审查和演进的资产。把它文件化之后，Git、AI、Code Review、脚本处理和可视化工具都能围绕同一份模型工作。

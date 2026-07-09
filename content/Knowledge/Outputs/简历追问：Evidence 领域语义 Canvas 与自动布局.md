---
title: 简历追问：Evidence 领域语义 Canvas 与自动布局
date: 2026-07-03 22:00:00
updated: 2026-07-09 10:45:13
tags:
  - interview/follow-up
  - resume/evidence
  - canvas
---

# 简历追问：Evidence 领域语义 Canvas 与自动布局

关联：[[全栈工程师简历#Evidence｜本地优先的业务履约建模与 AI 辅助建模平台]]、[[Evidence 项目简历描述与面试话术]]、[[15 分钟：Evidence 面试逐字稿]]。

## 对应简历描述

> 基于 React Flow / ELK 实现履约建模画布，围绕 RFP → Proposal → Contract → Fulfillment Request → Fulfillment Confirmation 的阶段关系，完成合约前上下文、合约上下文、履约泳道、角色层和参与对象层的自动布局。

## 面试官真正想确认

你是否真的做了领域布局规则，而不是把节点丢给 ELK/force layout 自动排一下。

## 连续追问链

### 1. 为什么通用布局不够

- 直接用 React Flow + ELK 会出现什么问题？线交叉、阶段错位还是上下文混乱？
- 履约图和普通流程图的区别在哪里？为什么 Contract 是中心语义？
- 用户看 Canvas 时最需要理解的是顺序、权责、凭证还是依赖？

### 2. 领域分类

- 如何识别 RFP、Proposal、Contract、Fulfillment Request、Fulfillment Confirmation？靠 subtype、label、relation 还是混合？
- 如果用户创建了未知 subtype，布局如何降级？
- 合约前上下文和合约上下文的边界由谁决定？

### 3. 布局策略

- 履约泳道如何构造？支付、开票、发货为什么要分行？
- Role 放上方、Participant/Thing 放下方的规则如何实现？
- 同一个 Participant 出现在多条泳道时，reference node 和 canonical node 如何保持身份一致？
- 用户手动拖动节点后，下次自动布局是否覆盖？有没有 pinned / locked 机制？

### 4. 性能与交互

- 大图下布局什么时候触发？全量布局还是局部增量？
- ELK 计算耗时如何避免阻塞 UI？是否考虑 Worker？
- 节点展开、折叠、详情抽屉和表格视图如何保持同一份模型？

## 场景推演题

> 一个 Contract 下面有 payment、delivery、invoice 三条履约分支，它们都引用同一个 Supplier。请画出布局思路，并说明如何减少跨层长边但不丢失“同一个供应商”的事实。

继续追：如果用户新增一个 `quality_inspection_request`，系统不知道它属于哪条泳道，你怎么降级？

## 准备证据

- 一个布局前/布局后的截图或草图。
- stage classifier 的规则表。
- reference node/canonical edge 的数据结构。
- 大图布局耗时和触发策略口径。

## 容易露馅的回答

- “ELK 会自动布局。”
- “坐标按节点类型写死。”
- “同一个参与方复制成多个实体也没关系。”
- “自动布局覆盖用户手动位置。”

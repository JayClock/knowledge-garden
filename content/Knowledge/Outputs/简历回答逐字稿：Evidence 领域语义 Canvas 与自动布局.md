---
title: 简历回答逐字稿：Evidence 领域语义 Canvas 与自动布局
date: 2026-07-03 22:30:00
updated: 2026-07-09 10:45:13
tags:
  - interview/script
  - resume/evidence
  - canvas
---

# 简历回答逐字稿：Evidence 领域语义 Canvas 与自动布局

关联：[[简历追问：Evidence 领域语义 Canvas 与自动布局]]、[[Evidence 项目简历描述与面试话术]]、[[15 分钟：Evidence 面试逐字稿]]。

## 30 秒开场

Evidence 的 Canvas 不是普通白板。普通图布局只关心节点和边怎么少交叉，但履约建模更关心业务阅读顺序：RFP、Proposal、Contract、Fulfillment Request、Fulfillment Confirmation，以及角色、参与方、上下文之间的层次。

所以我没有直接把所有节点丢给 ELK，而是先做领域语义布局。先识别业务阶段和上下文，再构造履约泳道、角色层和参与对象层，最后让 ELK 处理局部几何布局和连线。

## 如果面试官问：为什么通用布局不够？

我会说通用布局会把图排得“数学上还可以”，但业务上不一定可读。

比如 Contract 是正式合约入口，后面支付、发货、开票是几条履约分支。Role 通常应该在合约上下文上方，Participant 和 Thing 通常在下方。RFP 和 Proposal 属于合约前阶段。如果直接 force layout，用户会看到一团点线，很难理解履约顺序和权责边界。

所以我先把节点放进业务结构里，再做自动布局。

## 如果面试官追：阶段怎么识别？

我会说优先用结构化字段，比如 entity 的 type、subType 和 relationshipType。比如 `subType=rfp`、`proposal`、`contract`、`fulfillment_request`、`fulfillment_confirmation`。

如果结构化字段缺失，可以用 label/name 做弱识别，但那只能作为降级，不能作为核心依据。未知 subtype 我会放到“未分类”或相关上下文的补充区，不会硬塞到错误泳道里。

## 如果面试官追：履约泳道怎么构造？

我会这样说：

每个 Fulfillment Request 可以作为一条泳道的起点，比如 Payment Request、Delivery Request、Invoice Request。对应的 Confirmation 放在后面，相关补充 Evidence 跟在同一行或附近。

这样用户能横向读一条履约链路：请求是什么、谁确认、用什么凭证完成。多条履约分支并行展示，比所有节点混在一起清楚很多。

## 如果面试官追：同一个供应商出现在多条泳道怎么办？

我会说不能简单复制成多个供应商实体，那会破坏模型身份。

我的做法是 canonical node + reference node。供应商作为一个 canonical participant 存在；在每条履约泳道里可以投影一个 reference node，用虚线或引用边指回 canonical node。这样视觉上减少跨层长边，但模型上仍然知道它是同一个参与方。

## 如果面试官追：用户手动拖过节点，自动布局会不会覆盖？

我会说这是 Canvas 产品必须考虑的。自动布局适合初始生成和结构变化后整理，但用户手动调整是有意图的。可以设计 pinned/locked 机制：被用户固定的节点不再被全量布局覆盖，或者只做局部布局。

如果每次自动布局都把用户位置重置，用户会失去控制感。

## 如果面试官追：大图性能怎么做？

我会说布局触发要克制。不是每次属性编辑都全量 layout。结构变化，比如新增节点、删除关系、切换布局模式，才触发布局。大图可以考虑局部增量布局或把 ELK 计算放到 Worker，避免阻塞主线程。

React Flow 层面也要控制节点渲染，详情内容不要都挂在节点里，复杂信息放到侧边抽屉或表格视图。

## 收尾句

所以这块最核心的不是 React Flow，而是先把履约语义建模出来。Canvas 只是模型投影，自动布局要服务业务阅读顺序，而不是追求通用图算法的漂亮。

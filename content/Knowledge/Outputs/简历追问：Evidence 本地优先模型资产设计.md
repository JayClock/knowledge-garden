---
title: 简历追问：Evidence 本地优先模型资产设计
date: 2026-07-03 22:00:00
updated: 2026-07-27 08:18:19
tags:
  - interview/follow-up
  - resume/evidence
  - local-first
---

# 简历追问：Evidence 本地优先模型资产设计

关联：[[全栈工程师简历#Evidence｜领域建模、证据映射与 AI 辅助交付平台]]、[[Evidence 项目简历描述与面试话术]]、[[15 分钟：Evidence 面试逐字稿]]。

## 对应简历描述

> 设计 `.evidence/entities` 与 `.evidence/associations` 文件结构，将 Evidence、Participant、Role、Context 等业务概念及关系落为可读 YAML，支持 Git Diff、模型审查与 AI 工具读取，避免关键业务知识只沉淀在数据库或图形状态中。

## 面试官真正想确认

你为什么把业务模型放进本地文件，以及你是否处理了文件模型带来的校验、冲突、迁移和查询取舍。

## 连续追问链

### 1. 为什么本地优先

- 为什么参考 Obsidian Vault，而不是直接做数据库 SaaS？
- 哪些数据适合放 YAML，哪些仍然应该放 SQLite/PostgreSQL？
- “模型资产”与普通业务运行数据有什么不同？

### 2. 文件结构

- `.evidence/entities` 和 `.evidence/associations` 的 YAML schema 分别是什么？
- entity id 如何生成和保持稳定？重命名文件或修改 label 会不会破坏关系？
- association 如何引用 source/target？引用不存在的实体时怎么处理？
- Markdown 内容、结构化属性、类型/子类型如何共存？

### 3. 校验与演进

- 解析 YAML 失败时，整个 workspace 挂掉还是局部标记错误？
- schema version 放在哪里？旧模型如何迁移？
- Git merge conflict 如何提示用户？同一实体被两个人改了怎么解决？
- 大规模模型下，文件扫描和索引怎么做？

### 4. AI 与审查

- AI 工具读取 YAML 时是否有目录边界？能否访问用户其他文件？
- AI 生成的模型变更如何进入 diff/review，而不是直接覆盖？
- Git Diff 中哪些字段应该稳定排序，避免无意义噪音？

## 场景推演题

> 两个人同时修改 `contract.yaml`：一个改了金额字段，一个改了合同参与方关系。Git 合并后出现冲突。Evidence 如何帮助用户理解冲突并恢复模型一致性？

继续追：如果 association 指向了一个已删除 entity，前端 Canvas 和实体表分别怎么展示？

## 准备证据

- 一个 entity YAML 和一个 association YAML 示例。
- schema 校验错误样例。
- 文件扫描到领域对象的流程图。
- Git diff/review 截图或说明。

## 容易露馅的回答

- “文件方便被 Git 管。”
- “数据库太重，所以用 YAML。”
- “AI 直接读写文件就行。”
- “冲突交给 Git，产品不用管。”

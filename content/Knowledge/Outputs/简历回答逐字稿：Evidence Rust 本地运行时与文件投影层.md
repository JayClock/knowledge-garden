---
title: 简历回答逐字稿：Evidence Rust 本地运行时与文件投影层
date: 2026-07-03 22:30:00
updated: 2026-07-09 10:45:13
tags:
  - interview/script
  - resume/evidence
  - rust
  - tauri
---

# 简历回答逐字稿：Evidence Rust 本地运行时与文件投影层

关联：[[简历追问：Evidence Rust 本地运行时与文件投影层]]、[[Evidence 项目简历描述与面试话术]]、[[15 分钟：Evidence 面试逐字稿]]。

## 30 秒开场

Evidence 后端我用 Rust Axum，不是简单写几个 CRUD 接口，而是把 `.evidence` 文件投影成统一的领域资源。前端无论跑在 Web 还是 Tauri Desktop，都消费同一套 API 和资源契约。

后端分成 API、Domain、Persistent、Infrastructure 几层。Domain 定义 Workspace、Diagram、LogicalEntity、Relationship 等模型，Persistent 可以有 YAML 文件投影、SQLite 或 Fake Store 实现，API 层只负责路由和序列化。

## 如果面试官问：为什么不让前端直接读文件？

我会说前端直接读文件短期简单，但长期会让业务规则散在 UI 里。比如 YAML 解析、schema 校验、关系完整性、错误诊断、HAL/HATEOAS 序列化，这些都不应该写在 React 组件里。

用 Axum 做本地 API 后，Web 和 Desktop 可以共用同一套前端。前端只认 API root，不关心底层是远程服务、本地 Axum，还是未来的协作服务。

## 如果面试官追：文件投影层怎么做？

我会这样说：

投影层会扫描 `.evidence/entities` 和 `.evidence/associations`，只读取 yaml/yml 文件。解析后把 entity 映射成 LogicalEntity，也可以投影成 DiagramNode；association 映射成 Relationship 或 DiagramEdge。

文件的 modified time 可以作为 updatedAt 的来源，id、type、subType、attributes 来自 YAML 内容。投影过程中会做基础校验，比如必填字段、source/target 是否存在、类型是否合法。

## 如果面试官追：写文件怎么避免损坏？

我会说写文件不能直接覆盖。比较稳的是先写临时文件，fsync 后再原子 rename。必要时保留备份或写操作日志。

并发写同一个文件时，要有锁或版本检查。比如请求带上当前 file hash，保存前比较 hash 是否变化。如果变化，说明用户基于旧版本编辑，需要返回冲突，而不是覆盖别人修改。

## 如果面试官追：Tauri 和 Web 怎么共用前端？

我会说前端初始化 API client 时只需要拿到 base URL。

Web 模式下 base URL 来自环境变量或 `/api`。Tauri 模式下，桌面端启动内嵌 Axum 服务，绑定本地随机端口，然后通过 Tauri command 把 API base URL 传给 React。React 不需要知道自己在桌面还是浏览器，只要沿 API root 消费资源。

SQLite 主要保存本地用户、workspace 列表、最近打开目录等运行态信息。模型本身仍然在 `.evidence` 文件里。

## 如果面试官追：YAML 损坏时 API 返回什么？

我会说不要简单 500。更好的方式是返回部分成功加 diagnostics，或者提供单独的 diagnostics 资源。比如 LogicalEntities 可以返回解析成功的实体，同时问题面板显示哪些文件解析失败。

如果某个关键文件导致 Diagram 无法完整构建，Canvas 可以显示错误占位和修复建议。这样用户能通过 UI 修，而不是只能去命令行找 YAML。

## 如果面试官追：测试怎么做？

我会说不同持久化实现应该尽量共享契约测试。Fake Store 跑快速 domain/API 测试，SQLite 跑集成测试，YAML 投影层单独测解析、写回、损坏文件、断裂关系和稳定序列化。

Rust 类型系统能帮我们约束很多 domain model，但 YAML 来自外部文件，仍然必须做 schema 校验和错误处理。

## 收尾句

所以 Evidence 的 Rust 后端更像一个本地模型运行时。它把文件系统里的模型资产投影成稳定资源，让 Web、Desktop、AI 工具和后续协作能力都围绕同一套领域 API 工作。

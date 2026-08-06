---
title: 简历追问：Evidence Rust 本地运行时与文件投影层
date: 2026-07-03 22:00:00
updated: 2026-07-27 08:18:19
tags:
  - interview/follow-up
  - resume/evidence
  - rust
  - tauri
---

# 简历追问：Evidence Rust 本地运行时与文件投影层

关联：[[全栈工程师简历#Evidence｜领域建模、证据映射与 AI 辅助交付平台]]、[[Evidence 项目简历描述与面试话术]]、[[15 分钟：Evidence 面试逐字稿]]。

## 对应简历描述

> 基于 Axum 构建后端服务，将 `.evidence` YAML 文件投影为 Workspace、Diagram、LogicalEntity、Relationship 等领域资源；桌面端通过 Tauri 启动内嵌 API 与 SQLite，本地工作区可独立运行，Web 与 Desktop 共用同一套 React 前端。

## 面试官真正想确认

你是否把 Rust 后端做成了有领域边界的本地运行时，而不是“前端套 Tauri + 读文件”。

## 连续追问链

### 1. 分层设计

- Axum handler、domain、persistent、infrastructure 各自负责什么？
- Workspace、Diagram、LogicalEntity、Relationship 是领域模型还是 API DTO？如何转换？
- trait 抽象是为 Fake Store、SQLite、YAML 投影复用，还是过度设计？

### 2. 文件投影

- 后端如何扫描 `.evidence/entities` 和 `.evidence/associations`？只读 yaml/yml 吗？
- YAML 解析后如何投影成 DiagramNode / DiagramEdge？createdAt/updatedAt 从哪里来？
- 写回文件时如何做原子写、备份和格式稳定？
- 两个请求同时修改同一文件，如何避免覆盖？

### 3. Web/Desktop 共用前端

- 浏览器模式和 Tauri 模式下 API base URL 如何注入？
- Tauri 如何启动内嵌 Axum 服务？随机端口、鉴权、跨域怎么处理？
- SQLite 存什么？为什么模型不直接全部放 SQLite？
- 桌面端离线、本地目录权限和 workspace 选择如何处理？

### 4. 测试与错误

- Fake Store、SQLite、YAML 投影是否共享契约测试？
- YAML 文件损坏时，API 是 500、部分返回，还是返回诊断资源？
- Rust 类型系统在哪些地方帮你减少运行时错误？哪些地方仍需要 schema 校验？

## 场景推演题

> 用户在 Desktop 打开一个 workspace，其中一个 association YAML 引用了不存在的 entity。Axum API、React Canvas、Logical Entities 表分别应该怎么表现？

继续追：如果用户连续保存两次，第一次写文件还没完成，第二次请求到了，你如何防止文件损坏？

## 准备证据

- Rust 模块分层图。
- YAML → domain resource → HAL JSON 的转换示例。
- Tauri 获取 API base URL 的流程。
- 文件投影层单测或契约测试说明。

## 容易露馅的回答

- “Rust 就是写接口，没什么特别。”
- “Tauri 只是套个壳。”
- “前端直接读本地文件更简单。”
- “YAML 坏了就让用户修文件。”

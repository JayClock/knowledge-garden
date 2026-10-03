---
title: 简历追问：低代码 Monorepo 与 CI CD 治理
date: 2026-07-03 22:00:00
updated: 2026-10-03 09:48:31
tags:
  - interview/follow-up
  - resume/lowcode
  - engineering
---

# 简历追问：低代码 Monorepo 与 CI CD 治理

关联：[[15分钟：低代码平台]]、[[简历回答逐字稿：低代码 Monorepo 与 CI CD 治理]]。

## 面试官真正想确认

如果简历或项目回答提到 Monorepo，面试官会确认你是否深入理解包边界、依赖方向和任务缓存机制。

## 连续追问链

### 1. 仓库边界

- `packages` 和 `apps` 分别放什么？
- 工作流协议、TypeScript 引擎和可复用模块为什么放在 package？
- 应用为什么可以依赖核心包，核心包不能反向依赖应用？
- 哪些分层来自实际项目，哪些只是进一步治理建议？

### 2. 依赖治理

- React 等宿主依赖什么时候放到 `peerDependencies`？
- 多个 React 实例为什么会导致 Hooks 错误？
- pnpm 严格依赖怎样暴露幽灵依赖？
- 版本冲突的处理原则是什么，有没有当前项目证据？

### 3. Turborepo 任务与缓存

- 哪些构建、类型检查和测试任务适合缓存？
- cache key 为什么要覆盖源码、依赖版本、构建配置和关键环境变量？
- E2E、部署等依赖外部环境的任务为什么不能随意缓存？
- 如何从缓存失效原理分析缓存命中的有效性？

### 4. 协作链路

- Docker 多阶段构建和 CI/CD 的分层实践；
- 你在其中负责的核心模块与团队协作的分工界面是什么？
- 如果插件需要兼容多个 core 版本，你会怎样设计版本范围和语义化迁移？

## 场景推演题

> 一个工作流 package 把 React 写进普通 dependencies，宿主应用又安装了另一个 React 版本。请说明可能出现的问题，以及怎样通过 peerDependencies 和根版本治理处理。

继续追：如果 Turborepo 缓存没有纳入关键环境变量，为什么可能复用错误产物？

## 准备证据

- 实际 pnpm workspace 与 Turborepo 配置。
- package 与 app 的依赖方向。
- 真实 package.json 中 dependencies 与 peerDependencies 的划分。

## 面试注意事项

- 准确区分 pnpm workspace + Turborepo 的任务编排特性。
- 准确说明个人负责的执行器核心包与团队协作的工程链路。
- 关注原理与工程落地，不做未落地的功能宣称。

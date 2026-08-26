---
title: 简历追问：低代码 Monorepo 与 CI CD 治理
date: 2026-07-03 22:00:00
updated: 2026-08-26 08:30:30
tags:
  - interview/follow-up
  - resume/lowcode
  - engineering
---

# 简历追问：低代码 Monorepo 与 CI CD 治理

关联：[[15分钟：低代码平台]]、[[简历回答逐字稿：低代码 Monorepo 与 CI CD 治理]]。

> [!warning] 使用边界
>
> - 这是一条项目工程背景和技术理解，不是当前个人简历主成果。
> - 材料记录的是 pnpm workspace 与 Turborepo，不使用 Nx、affected build 或 `enforce-module-boundaries` 冒充项目事实。
> - Docker、完整 CI/CD、插件兼容矩阵、灰度和回滚没有确认属于个人实现。

## 面试官真正想确认

如果简历或项目回答提到 Monorepo，面试官会确认你是否理解包边界、依赖方向和任务缓存，同时也会检查你有没有把团队工程链路说成个人成果。

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
- 当前是否有缓存命中率和 CI 时间数据？没有时如何说明边界？

### 4. 协作链路

- Docker 多阶段构建和 CI/CD 由谁负责？
- 你能解释哪些整体方案，哪些不能说成个人实现？
- 如果插件需要兼容多个 core 版本，你会怎样设计版本范围和迁移，但为什么这仍是延展方案？

## 场景推演题

> 一个工作流 package 把 React 写进普通 dependencies，宿主应用又安装了另一个 React 版本。请说明可能出现的问题，以及怎样通过 peerDependencies 和根版本治理处理。

继续追：如果 Turborepo 缓存没有纳入关键环境变量，为什么可能复用错误产物？

## 准备证据

- 实际 pnpm workspace 与 Turborepo 配置。
- package 与 app 的依赖方向。
- 真实 package.json 中 dependencies 与 peerDependencies 的划分。

拿不出实际配置时，只讨论工程理解，不声称个人完成了完整治理。

## 容易露馅的回答

- 把项目说成 Nx，但实际材料是 Turborepo。
- 把完整 Docker 和 CI/CD 链路算成个人成果。
- 补写缓存命中率、镜像体积或构建耗时。
- 把建议中的插件灰度、兼容矩阵和回滚说成已上线。

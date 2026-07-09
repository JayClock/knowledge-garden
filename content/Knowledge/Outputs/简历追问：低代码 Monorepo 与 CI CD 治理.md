---
title: 简历追问：低代码 Monorepo 与 CI CD 治理
date: 2026-07-03 22:00:00
updated: 2026-07-09 10:45:13
tags:
  - interview/follow-up
  - resume/lowcode
  - engineering
---

# 简历追问：低代码 Monorepo 与 CI CD 治理

关联：[[全栈工程师简历#低代码工作流引擎]]、[[15分钟：低代码平台]]、[[Nx Monorepo 改造中如何治理依赖版本冲突]]。

## 对应简历描述

> 采用 Monorepo 架构集中管理前后端代码，通过 Docker 多阶段构建优化容器镜像体积，实现了从开发到生产环境的全链路 CI/CD 自动化部署。

## 面试官真正想确认

你是否做过工程边界和发布治理，而不是把多个项目放进一个仓库就叫 Monorepo。

## 连续追问链

### 1. 仓库边界

- Monorepo 里有哪些包：core engine、ui components、business plugins、business apps、server、shared types？
- 哪些依赖方向是允许的，哪些必须禁止？如何用 lint 或 Nx tags 固化？
- 前后端共享类型是怎么做的？是否会导致双向依赖？

### 2. 构建与缓存

- Nx affected build 根据什么判断受影响项目？缓存 key 包含哪些因素？
- 哪些任务可以远程缓存，哪些不能缓存？环境变量变化如何处理？
- 如果只改一个业务插件，是否需要全量构建和全量测试？

### 3. 依赖治理

- 发生过 React、ECharts、lodash 等版本冲突吗？如何治理？
- peerDependencies、根依赖、pnpm strict 模式分别解决什么问题？
- 循环依赖是怎么发现和拦截的？CI 中是否硬性失败？

### 4. 发布与容器

- Docker 多阶段构建具体拆了哪些阶段？依赖安装、构建产物、运行镜像如何分层？
- 镜像体积优化前后如何衡量？不要硬编数字，讲统计口径即可。
- Core engine 和业务插件如何做版本兼容、灰度和回滚？

## 场景推演题

> 一个新插件依赖 core engine 的新 API，但某个业务 App 仍然部署在旧 core 上。CI/CD 如何在发版前发现这个不兼容？上线后如何灰度？

继续追：如果 pnpm 严格模式导致老项目大量幽灵依赖报错，你怎么推动团队迁移？

## 准备证据

- Nx project graph 或依赖分层图。
- `enforce-module-boundaries` 规则样例。
- CI pipeline 阶段图。
- Dockerfile 多阶段构建片段。

## 容易露馅的回答

- “Monorepo 就是放一个仓库。”
- “CI 全量跑，反正机器够。”
- “依赖冲突靠开发自己注意。”
- “所有包一起发版，不需要兼容策略。”

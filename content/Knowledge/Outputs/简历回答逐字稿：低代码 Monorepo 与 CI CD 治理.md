---
title: 简历回答逐字稿：低代码 Monorepo 与 CI CD 治理
date: 2026-07-03 22:30:00
updated: 2026-07-09 10:45:13
tags:
  - interview/script
  - resume/lowcode
  - engineering
---

# 简历回答逐字稿：低代码 Monorepo 与 CI CD 治理

关联：[[简历追问：低代码 Monorepo 与 CI CD 治理]]、[[Nx Monorepo 改造中如何治理依赖版本冲突]]。

## 30 秒开场

我理解的 Monorepo 不是把项目放进同一个仓库，而是把平台的依赖边界、构建影响范围和发布流程显式治理起来。低代码平台里有 core engine、组件库、业务插件、业务应用、服务端和 shared types，如果不管依赖方向，很快会变成互相引用。

所以我用 Nx 这类工具管理 project graph，用 tags 和 lint 规则限制依赖方向，用 affected build/test 缩小 CI 范围，再配合 pnpm 的严格依赖和 Docker 多阶段构建，把开发到生产的链路固化下来。

## 如果面试官问：仓库怎么分层？

我会说大概分几层：

- `core`：低代码运行时、Schema 解析、调度核心。
- `ui`：通用 UI 组件。
- `plugins`：业务节点、表单组件、图表组件。
- `apps`：具体业务应用或管理台。
- `server`：后端服务。
- `shared`：共享类型和协议。

依赖方向必须是上层依赖下层。比如 app 可以依赖 plugin，plugin 可以依赖 core，但 core 不能反向引用某个业务 app。这个规则不是靠口头约定，而是用 Nx `enforce-module-boundaries` 这类规则在 CI 里拦住。

## 如果面试官追：依赖版本冲突怎么处理？

我会这样回答：

合库时最典型的问题是多个 React 实例或三方库版本不一致。我的策略是核心技术栈尽量单版本，比如 React、ECharts 这类基础依赖在根 package 管理。

对于 core engine、UI 插件这种被宿主使用的包，React 这类库应该放在 peerDependencies，让运行时只用宿主提供的一份实例，避免 Hooks 因为多 React 实例报错。

同时启用 pnpm 的严格模式，禁止幽灵依赖。代码里用了某个包但 package 没声明，就应该在开发阶段报错，而不是靠 node_modules hoist 侥幸跑通。

## 如果面试官追：affected build 怎么保证可靠？

我会说 Nx 的 affected 是基于 project graph 和 git diff 判断影响范围。但缓存 key 必须包含源文件、依赖版本、构建配置和关键环境变量。否则很容易出现“缓存命中但产物不对”。

不是所有任务都适合缓存。纯构建、单测比较适合；依赖外部环境的 e2e、部署动作就要谨慎。CI 上我会分层：先跑 lint/typecheck/unit，再跑受影响项目的 build，最后对关键应用跑集成或 e2e。

## 如果面试官追：Docker 多阶段构建怎么优化？

我会说核心是把依赖安装、构建和运行镜像拆开。

第一阶段安装依赖，尽量利用 lockfile 缓存。第二阶段执行构建，只输出 dist 或 server bundle。第三阶段用更小的 runtime 镜像，只拷贝运行必需文件，不把源码、测试文件、构建缓存都带进去。

如果面试官追具体数字，我不会硬编。我会讲统计口径：看镜像体积、构建耗时、缓存命中率、部署传输耗时，以及回滚时拉取镜像速度。

## 如果面试官追：插件和 core 版本不兼容怎么办？

我会说这类平台一定要有兼容矩阵。插件声明依赖的 core 版本范围，CI 在构建业务 app 时检查版本是否满足。核心 API 变更时要尽量新增而不是破坏，必要时提供 deprecation 周期和迁移脚本。

灰度时可以先让少量 app 升 core，再观察插件运行和错误日志。不能所有包一起升级，一出问题全平台回滚。

## 收尾句

所以我做工程化治理的重点，是把依赖边界、版本约束、构建影响和发布回滚变成自动化规则。这样平台变大后，不靠人肉记忆维持秩序。

---
date: 2026-04-22 09:52:15
updated: 2026-07-09 10:45:13
---

# 面试防线：Nx Monorepo 改造中如何治理依赖版本冲突

**面试官提问**：
“把底层核心库、UI 组件库和多个业务应用全收拢进一个 Monorepo 后，你一定遇到了幽灵依赖或者不同业务线强制要求不同版本的 React/三方库的问题。在 Nx 体系下你是如何治理这些依赖冲突的？”

 核心回答思路 (STAR法则)

 1. 业务痛点 (Situation)
在合库初期，各业务线的 `package.json` 是八仙过海。有的用 React 17，有的用 18；有的 lodash 是 3.x，有的是 4.x。打包时频繁出现“Hooks 不能在组件外部调用”等由于多版本 React 实例共存导致的致命错误。此外，幽灵依赖（代码里引用了没在 package 里声明的包）泛滥。

 2. 技术考量 (Task)
在 Monorepo 中，如果不做统一管制，仓库会迅速变成一个巨大的垃圾堆。必须做到**版本单一化约束**和**依赖边界可见性**。

 3. 架构决策 (Action)
- **单一版本策略 (Single Version Policy)**：我坚决推行了将所有第三方依赖（如 React, ECharts）全部上浮到项目根目录的 `package.json`。各个子 package 不再声明第三方库的 `dependencies`，强制全库吃同一套技术栈基座。
- **Peer Dependencies 解耦**：对于底层渲染引擎（Core Engine）和 UI 插件，我们将 React 等核心库设为 `peerDependencies`，确保在运行时它们是由顶层业务宿主提供的同一个实例，从物理上消灭了多实例共存导致的 Hooks 报错。
- **Nx 边界 lint 规则 (Enforce Module Boundaries)**：我配置了 `@nx/enforce-module-boundaries` 校验规则。给不同的库打上 `tags`（如 `scope:core`, `scope:ui`, `scope:app`），强制限制：UI 库不能反向引用 App 库，底层引擎不能直接依赖具体的 UI 组件。这在 AST 静态检查阶段就拦截了面条代码。
- **严格的包管理器机制**：启用了 pnpm 的 `strict-peer-dependencies` 和 `shamefully-hoist=false`，让幽灵依赖在开发态直接报错（模块找不到），倒逼开发规范化。

 4. 业务价值 (Result)
通过铁腕治理，我们将几十个原本参差不齐的项目统一到了标准技术基座上。依赖治理不再是人肉检查，而是被沉淀成了不可绕过的自动化 CI/CD 规则，大大降低了团队因为依赖冲突导致的线上 P0 事故。
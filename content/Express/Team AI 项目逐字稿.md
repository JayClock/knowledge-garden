---
tags:
  - frontend-interview
  - team-ai
  - script
  - oral
  - 前端面试系列
date: 2026-03-30 11:55:00
updated: 2026-03-30 11:55:00
share: true
---

# Team AI 项目逐字稿

## 使用方式

- 这页只保留 `3 到 5 分钟版本` 和 `深挖版本`。
- 默认先讲 3 到 5 分钟，面试官继续追问再按深挖入口展开。
- 主轴固定是“上下文建模优先，执行推进次级”。

## 3 到 5 分钟版本

如果让我用 3 到 5 分钟介绍 Team AI，我会把它定义成一个面向软件交付场景的 AI 上下文建模平台 / 交付工作台，而不是普通 AI 聊天工具，也不是单纯的编排平台。它想解决的核心问题是：AI 在真实研发流程里经常拿不到连续、稳定、结构化的上下文，所以很难持续参与需求、拆解、执行、review 和回写这整条链路。

所以我们一开始做的不是先接几个 agent，而是先把交付对象建稳。像 project、goal、spec、task、board、card、conversation、session、trace、resource 这些对象，都要先有清楚的边界和关系。这样 AI 拿到的就不只是一个 prompt，而是一套可以逐步展开、持续回写、能被人和系统共同消费的上下文。

我在这个项目里做的是全栈和平台化工作。前端这边，我负责项目工作台、Kanban、卡片详情、会话页、trace 视图这些上下文界面；后端这边，我也参与资源契约、策略校验、状态回流和 SSE 事件流，让前端上的动作不只是改个状态，而是真正更新上下文并稳定回写。

这个项目最难的点，不是接入 AI 本身，而是把“对象、上下文、执行、证据”这四件事做成一套闭环。比如看板不是简单状态板，而是在表达当前阶段、缺失 evidence、准入规则和下一步动作；会话、trace 和 artifact 也不是孤立页面，而是在持续补齐执行证据。

所以如果总结 Team AI，我会说它最有价值的地方，不是让 AI 多做一步生成，而是先把交付上下文稳定下来，再把 AI 纳入一条可治理、可追踪、可回放的交付链路里。

## 深挖版本

- 建模主线：[[./Team AI 整个建模流程怎么讲|Team AI 整个建模流程怎么讲]]
- AI 上下文怎么准备：[[./如何用履约建模法给 AI 准备业务上下文|如何用履约建模法给 AI 准备业务上下文]]
- 看板和执行推进：[[./Team AI 里 Agent 编排怎么讲|Team AI 里 Agent 编排怎么讲]]、[[./Team AI 里看板为什么不是纯拖拽 UI|Team AI 里看板为什么不是纯拖拽 UI]]
- 前端架构和工作台设计：[[./Agent 智能体平台的前端架构怎么讲|Agent 智能体平台的前端架构怎么讲]]
- 全栈价值和对象边界：[[./Team AI 里前端转全栈怎么落地到项目|Team AI 里前端转全栈怎么落地到项目]]、[[./Team AI 里 project board card session 边界怎么讲|Team AI 里 project board card session 边界怎么讲]]
- 状态管理取舍：[[./Team AI 里 Zustand Redux XState 怎么结合项目讲|Team AI 里 Zustand Redux XState 怎么结合项目讲]]
- 高频追问 / STAR：[[./面试官追问 Team AI 时怎么答|面试官追问 Team AI 时怎么答]]、[[./Team AI 面试反问与陷阱题|Team AI 面试反问与陷阱题]]、[[./Team AI STAR 回答模板|Team AI STAR 回答模板]]
- 关联能力：[[../Knowledges/HATEOAS 面试|HATEOAS 面试]]

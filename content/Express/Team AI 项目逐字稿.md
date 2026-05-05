---
tags:
  - frontend-interview
  - team-ai
  - script
  - oral
  - 前端面试系列
date: 2026-03-30 11:55:00
updated: 2026-04-16 22:02:31
share: true
---

# Team AI 项目逐字稿

## 使用方式

- 这页保留完整主稿，默认先讲 3 到 5 分钟版本。
- 如果你只想现场快速开口，优先看 [[Team AI 项目逐字稿|Team AI 项目逐字稿]]。
- 如果你要配合简历投递，直接联动 [[Team AI 简历项目描述精简版|Team AI 简历项目描述精简版]]。
- 面试官继续追问时，不要继续在这页硬讲，直接跳到对应专题题。

## 最短跳转

- 口述短稿：[[Team AI 项目逐字稿|Team AI 项目逐字稿]]
- 简历版：[[Team AI 简历项目描述精简版|Team AI 简历项目描述精简版]]
- 结构化纲要：[[../Knowledges/Team AI 项目结构化描述|Team AI 项目结构化描述]]
- 高频追问：[[./面试官追问 Team AI 时怎么答|面试官追问 Team AI 时怎么答]]

## 3 到 5 分钟版本

如果让我用 3 到 5 分钟介绍 Team AI，我会把它定义成一个面向软件交付场景的 AI 上下文工作台，而不是普通 AI 聊天工具，也不是单纯的 Agent 编排平台。它要解决的核心问题是，AI 在真实研发流程里经常拿不到连续、稳定、结构化的上下文，所以很难持续参与需求拆解、任务推进、执行、review 和结果回写。

所以我们一开始做的不是先接几个 agent，而是先把交付对象建稳。像 project、task、board、card、session、trace、workflow 这些对象，我们先做了清楚的边界和关系。后端这一层不是简单表加接口，而是偏 Smart Domain DDD 的建模方式，把对象关系和业务动作沉淀进领域模型和资源模型里。这样 AI 拿到的就不只是一个 prompt，而是一套可以持续展开、回写、追踪的项目上下文。

第二层我们做的是语义化资源访问。服务端通过 HATEOAS 把资源关系和动作暴露出来，前端不是手写 URL，而是按资源关系导航项目、任务、会话和子资源。这样对象关系、API 关系和前端页面关系会比较一致，系统也更容易演进。

第三层是执行和治理。现在项目里已经有 Kanban、workflow、specialist、runtime session、trace 这些能力，所以 AI 不是挂在外面的聊天框，而是被放进任务推进链路里。比如目标进入系统以后，会先沉淀成 task 和 card，再根据列级规则、artifact gate、manual approval、WIP limit 等约束决定能不能继续推进，满足条件以后才进入 specialist 或 workflow 执行。

第四层是可观测和可回放。项目里已经有 workflow run、task run、trace、后台任务状态和事件回流，所以一次执行不是跑完就没了，而是能看到它怎么开始、怎么推进、卡在哪里、产出了什么证据。这个点很重要，因为它说明我们做的不是一个 AI demo，而是一套能治理、能审计、能复盘的协作系统。

所以如果总结 Team AI，我会说它最有价值的地方，不是让 AI 多生成一步，而是先把交付上下文稳定下来，再把 AI 放进一条可治理、可追踪、可回放的交付链路里。

## 如果面试官追问现在做到哪一步

我会直接这样回答：

- 第一，核心对象和上下文边界已经比较完整，项目、任务、会话、看板、workflow、trace 这些对象不是松散页面，而是有稳定关系。
- 第二，语义 API 和前端消费链路已经跑通，前端按资源关系导航，不是把页面全部绑死在硬编码接口上。
- 第三，workflow、kanban、specialist runtime、状态回流已经不是 PPT 概念，而是有页面、有资源、有执行痕迹。
- 第四，治理能力已经有明显落点，像 WIP limit、artifact gate、manual approval、trace、session event 这些都不是聊天产品会有的能力。
- 第五，AI 已经进入真实对象和流程里，而不是孤立外挂。

如果要诚实地说，系统还没有走到完全本体驱动和全自动代码生成那一步，但语义建模、流程推进、事件追踪、AI 执行这些骨架已经搭起来了。

## 深挖版本

- 建模主线：[[./Team AI 整个建模流程怎么讲|Team AI 整个建模流程怎么讲]]
- AI 上下文怎么准备：[[./如何用履约建模法给 AI 准备业务上下文|如何用履约建模法给 AI 准备业务上下文]]
- 看板和执行推进：[[./Team AI 里 Agent 编排怎么讲|Team AI 里 Agent 编排怎么讲]]、[[./Team AI 里看板为什么不是纯拖拽 UI|Team AI 里看板为什么不是纯拖拽 UI]]
- 前端架构和工作台设计：[[./Agent 智能体平台的前端架构怎么讲|Agent 智能体平台的前端架构怎么讲]]
- 全栈价值和对象边界：[[./Team AI 里前端转全栈怎么落地到项目|Team AI 里前端转全栈怎么落地到项目]]、[[./Team AI 里 project board card session 边界怎么讲|Team AI 里 project board card session 边界怎么讲]]
- 状态管理取舍：[[./Team AI 里 Zustand Redux XState 怎么结合项目讲|Team AI 里 Zustand Redux XState 怎么结合项目讲]]
- 高频追问 / STAR：[[./面试官追问 Team AI 时怎么答|面试官追问 Team AI 时怎么答]]、[[./Team AI 面试反问与陷阱题|Team AI 面试反问与陷阱题]]、[[./Team AI STAR 回答模板|Team AI STAR 回答模板]]
- 关联能力：[[../Knowledges/HATEOAS 面试|HATEOAS 面试]]

## 面试时建议强调的关键词

- AI 上下文工作台
- Smart Domain DDD
- HATEOAS 语义导航
- Kanban 策略治理
- workflow / specialist / runtime session
- trace / event / evidence 闭环
- 可追踪、可回放、可治理
- 已落地，不是概念图

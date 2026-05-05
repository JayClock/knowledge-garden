---
date: 2026-03-26 20:08:24
updated: 2026-04-13 10:56:59
tags:
  - 前端面试系列
  - team-ai
  - boundary
share: true
---

# Team AI 里 project board card session 边界怎么讲

## 先给结论

如果面试官追问 Team AI 里到底哪个对象算边界，我不会给一个绝对答案，而是按问题域来拆：project 是业务上下文边界，board 是协作一致性边界，card 是被操作对象，session 是执行生命周期边界。

## 30 秒版本

- project 负责装下任务、会话、看板、workflow、trace 这些核心对象，所以它是一级业务容器。
- board 负责列规则、WIP、流转和阶段语义，所以它更像协作投影和一致性边界。
- card 是用户最常操作的对象，但很多动作最后仍然要回到 board 和 task 规则上校验。
- session 负责执行过程、handoff、运行状态和结果回写，所以它更像执行生命周期边界。

## 详细讲法

### 1. 为什么 project 是一级上下文

因为 Team AI 的很多能力都天然挂在 project 下面。任务推进、看板协作、workflow、trace、notes、memories、sessions 这些都不是孤立存在的，而是属于某个项目上下文。所以 project 不是一个名字和描述组成的详情页，而是整个系统最稳定的业务容器。

### 2. 为什么 board 更像一致性边界

因为 card 的很多动作虽然表现为拖拽或状态变化，但真正要统一收敛的是 board 规则。比如某列是否允许进入、是否超过 WIP、是否缺少 artifact、是否要求审批，这些都不是 card 自己能决定的，而是 board 级别的协作规则。

### 3. 为什么 card 不是最好的聚合根

card 是最容易被看到和被操作的对象，但它更多是 task 在看板上的投影。面试里如果把 card 直接讲成最核心聚合根，往往会把边界讲窄。更稳妥的说法是，card 是交互焦点，但很多一致性和规则仍然归属于 board 和 task 所在的上下文。

### 4. 为什么 session 适合单独拿出来讲

因为 session 这层承接的是运行过程，而不是协作展示。specialist 执行、trace 回写、任务结果、状态迁移、handoff 这些都更像 session 生命周期问题，而不是 board 规则问题。所以 session 适合作为执行边界来讲。

## 一个适合现场直接说的回答

> 我不会把 Team AI 里所有对象都压成一个边界。更准确的说法是，project 是业务上下文边界，board 是协作一致性边界，card 是被操作对象，session 是执行生命周期边界。这样讲既贴项目，也能说明我不是机械套 DDD 概念，而是真的按问题域在分边界。

## 如果面试官继续追问 task 放哪

推荐回答：

> task 更像核心工作项本体，card 是它在 board 上的协作投影，session 是它进入执行态之后的过程承载。这样 task、card、session 三者关系会更清楚。

## 跳转

- 主稿：[[./Team AI 项目逐字稿|Team AI 项目逐字稿]]
- 建模：[[./Team AI 整个建模流程怎么讲|Team AI 整个建模流程怎么讲]]
- 编排：[[./Team AI 里 Agent 编排怎么讲|Team AI 里 Agent 编排怎么讲]]

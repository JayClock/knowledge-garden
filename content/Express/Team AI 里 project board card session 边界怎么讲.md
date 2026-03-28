---
date: 2026-03-26 20:08:24
updated: 2026-03-28 15:56:54
tags:
  - 前端面试系列
share: true
---
# Team AI 里 project board card session 边界怎么讲

如果面试官追问 Team AI 里到底哪个对象算边界，我一般不会给一个绝对答案，而是按问题域来拆。

从业务上下文看，project 是最大的业务容器。任务、会话、知识图谱、board 都挂在 project 下面，所以 project 更像一级上下文。

从工作流执行看，board 是更适合讲聚合边界的对象。因为 columns、cards、WIP、entry rule、move intent、实时刷新这些东西，要维护的是 board 级别的一致性。

从用户直接操作看，card 是最显眼的对象，但它通常不是最合适的聚合根。因为很多操作虽然发生在 card 上，真正要校验和收敛的是 board 的规则。

从长任务执行和过程追踪看，session 也可以作为一个独立边界来讲。比如 specialist 执行、trace 回写、handoff、运行状态更新，这些更像 session 生命周期问题，而不是 board 状态问题。

所以我在面试里会这样收：project 是业务上下文边界，board 是工作流一致性边界，card 是被操作对象，session 是执行生命周期边界。这样讲既贴项目，也能说明你不是机械套 DDD 概念。

## 关联逐字稿

- [[./Team AI 15 分钟逐字稿（完整版）|Team AI 15 分钟逐字稿（完整版）]]

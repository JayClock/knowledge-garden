---
date: 2026-03-26 20:08:10
updated: 2026-03-30 11:35:00
tags:
  - 前端面试系列
share: true
---
# Team AI 里 Zustand Redux XState 怎么结合项目讲

如果把状态管理工具放回 Team AI 里讲，我会先按复杂度来源拆，而不是先站队某个库。

像 board 页面这种，需要把 columns、cards、selection、dragging、中间校验结果收敛在一个上下文投影里，我会优先想到 Zustand。因为这里核心问题是共享状态和聚合边界，Zustand 足够轻，也方便把 board 相关动作集中起来。

如果项目继续扩大到多人长期协作、要求严格 action 审计、调试回放和更强约束的数据流，那 Redux 会更有价值。它不是更先进，而是更适合强治理和强审计场景。

如果问题变成 session 生命周期、审批流、review 状态、任务阶段推进这种明确的状态迁移，比如 idle、queued、running、blocked、review、done，那我会更偏向 XState。因为这里复杂度不在数据共享，而在状态切换本身。

所以在 Team AI 里我不会问哪个工具更强，而会问当前复杂度来自哪里。board 更像上下文聚合问题，session / review 更像流程状态问题，审计回放更像强治理问题。这个区分比直接站队某个库更重要。

## 关联逐字稿

- [[./Team AI 项目逐字稿|Team AI 项目逐字稿]]

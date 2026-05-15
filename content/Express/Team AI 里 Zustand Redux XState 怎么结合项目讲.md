---
date: 2026-03-26 20:08:10
updated: 2026-05-15 10:03:23
share: true
---

# Team AI 里 Zustand Redux XState 怎么结合项目讲

 先给结论

如果把状态管理工具放回 Team AI 里讲，我不会先站队某个库，而会先按复杂度来源拆：共享状态问题、强治理问题、状态机问题，这三类复杂度适合的工具不一样。

 30 秒版本

- board 页面这种共享上下文和局部聚合问题，我会优先想到 Zustand。
- 如果系统要求强 action 审计、严格数据流和时间旅行调试，Redux 会更合适。
- 如果问题本质是 session、review、workflow step 这种明确状态迁移，XState 会更自然。

 详细讲法

 1. Zustand 适合什么

像 Team AI 里的 board 工作面，需要收敛 columns、cards、selection、dragging、中间校验结果和本地交互状态，这类问题的核心是共享状态和页面聚合，Zustand 足够轻，也方便把相关动作集中到一个 store 里。

 2. Redux 适合什么

如果项目继续扩大到多人长期协作、强 action 审计、调试回放、严格副作用边界和更强治理的数据流，Redux 会更有价值。它不一定更先进，但非常适合强约束和强可审计场景。

 3. XState 适合什么

如果复杂度主要来自生命周期，比如 idle、queued、running、blocked、review、done 这种明确状态迁移，或者 session、approval、workflow step 这种流程状态，我会更偏向 XState。因为这类问题的难点不是共享数据，而是状态切换本身。

 4. 回到 Team AI 怎么落地

如果让我结合项目来答，我会说：board 这种上下文聚合更像 Zustand 问题，workflow run 或 session 生命周期更像 XState 问题，如果系统进一步走向强审计和强治理，再考虑 Redux 作为更严格的全局状态流方案。

 一个更像高级前端的回答

> 我不会问哪个工具更强，而会先问当前复杂度来自哪里。Team AI 里 board 更像共享上下文聚合问题，session 和 workflow step 更像状态迁移问题，审计和回放更像强治理问题。只有把复杂度来源分清楚，工具选型才不会流于站队。

 如果面试官追问为什么不全都用一个库

推荐回答：

> 因为不同问题的本质不一样。把所有复杂度都压给一个库，往往会导致表达力不足或者成本过高。更稳妥的做法是按问题域分层，而不是为了统一而统一。

 跳转

- 主稿：[[./Team AI 项目逐字稿|Team AI 项目逐字稿]]
- 看板：[[./Team AI 里看板为什么不是纯拖拽 UI|Team AI 里看板为什么不是纯拖拽 UI]]
- 编排：[[./Team AI 里 Agent 编排怎么讲|Team AI 里 Agent 编排怎么讲]]

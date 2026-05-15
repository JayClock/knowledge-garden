---
date: 2026-03-26 20:08:10
updated: 2026-05-15 10:03:23
share: true
---

# Team AI 里看板为什么不是纯拖拽 UI

 先给结论

如果面试官问 Team AI 里的 Kanban 难点是什么，我不会回答拖拽实现，而会先把问题抬到业务层。因为这个看板不是纯前端交互，而是项目上下文的推进面。

 30 秒版本

在普通看板里，拖拽更像状态展示；但在 Team AI 里，卡片移动背后带的是 task 当前阶段、缺失 evidence、required artifacts、审批要求和下一步执行权限。所以前端这里最重要的不是拖得多丝滑，而是把用户 move intent、后端规则校验和实时状态回流对齐。

 详细讲法

 1. card move 不是简单改列

一张 card 从 Backlog 到 Todo，或者从 Dev 到 Review，不只是 UI 上换一列，而是在更新共享事实：它处在哪个阶段、缺什么、下一步允许什么动作、要不要触发执行或 review。

 2. board 列本身带规则

列不是纯字符串状态。现在项目里列级别会承载 allowed source、required artifacts、manual approval、WIP 这些规则，所以卡片能不能过去必须由后端裁决。

 3. 前端发起的是 move intent

这个项目里前端不适合做纯乐观更新，因为很多动作都依赖后端规则判断。更准确的说法是，前端表达 move intent，后端做最终裁决，再通过 authoritative state 和事件流把真实结果推回界面。

 4. 事件回流比拖拽动画更重要

真正让这个看板像平台能力的，不是拖拽动画，而是 task column transition、session started、session completed、trace 补齐这些事件能持续回流前端。这样看板才不只是状态板，而是执行推进面。

 5. 所以难点是上下文一致性

这个项目把前端难点从组件交互升级成了上下文一致性问题。只要 move intent、后端规则、session 启动、trace 回写和 UI 展示有任何一段没对齐，看板就会失真。

 一个适合直接背的回答

> Team AI 里的 Kanban 不是纯拖拽 UI，因为卡片移动背后不是简单状态切换，而是任务阶段、准入规则、artifact 要求、执行权限和证据回写的统一变化。前端发起的是用户意图，后端做规则裁决，最终再通过事件流和 authoritative state 回流到界面。所以它真正难的不是拖拽组件，而是上下文一致性。

 如果面试官追问前端技术难点

推荐回答：

> 技术上我会拆成三个点：一是拖拽和选择态的本地交互，二是服务端 authoritative state 回流后的幂等更新，三是高频事件下的性能和视图稳定性。

 跳转

- 编排：[[./Team AI 里 Agent 编排怎么讲|Team AI 里 Agent 编排怎么讲]]
- 主稿：[[./Team AI 项目逐字稿|Team AI 项目逐字稿]]
- 全栈：[[./Team AI 里前端转全栈怎么落地到项目|Team AI 里前端转全栈怎么落地到项目]]

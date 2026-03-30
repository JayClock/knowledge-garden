---
date: 2026-03-28 21:05:00
updated: 2026-03-30 11:31:43
tags:
  - 前端面试系列
  - team-ai
  - agent
  - orchestration
  - oral
share: true
---

# Team AI 里 Agent 编排怎么讲

## 先把“建模”和“Agent 编排”分开

- 建模讲的是：系统里有哪些稳定对象、关系和语义骨架。
- Agent 编排讲的是：这些已经建好的上下文，怎么被继续推进到执行链里。
- 所以建模单独看 [[./Team AI 整个建模流程怎么讲|Team AI 整个建模流程怎么讲]]，这篇只讲“上下文进入执行”的那一段。

## 先说结论

这类问题不要讲成：

> 我们接了几个 agent，然后让它们互相调用。

这样会显得很空。

更好的讲法是：

> Team AI 里的 Agent 编排，本质上是把已经结构化的 goal、spec、task、card 上下文，继续通过看板规则、specialist 路由、workflow 执行、session 过程和 trace 回写推进下去的一条可观测执行链。

这句话出来，层次会更清楚。因为它先承认建模是主轴，再说明编排只是把上下文往前推进。

---

## 一分钟版本

> 如果让我讲 Team AI 的 Agent 编排，我不会讲成“多个 agent 聊天协作”，而会讲成“上下文怎么进入执行链”。当前项目里，目标先通过 kanban intake 进入系统，沉淀成 spec、task、card 这些稳定对象；看板列再基于 allowed source、required artifacts、manual approval 这些规则决定它能不能继续往下走；路由通过以后，系统才会落到 specialist、provider 和 workflow；最后再通过 session、workflow run 和 trace 把执行过程持续回写。所以这条链本质上不是“谁会写 prompt”，而是“上下文怎么被结构化、怎么被推进、怎么被回写和治理”。

---

## 两到三分钟版本

### 1. 先从上下文入口开始，而不是从 agent 开始

> 我讲编排时，不会先说系统里有几个 specialist，而会先说目标怎么进入系统。因为编排真正的起点不是 agent，而是目标先被结构化。当前项目里已经有 kanban intake 入口，说明系统不是直接让用户把一句话丢给某个 agent，而是先把目标放进 spec、task、card 这些后续都能消费的对象里。

### 2. 再把看板列当成上下文推进器

> Team AI 里看板列不是纯状态展示，而是在表达“当前这个任务处在哪个阶段、缺什么上下文、下一步允许什么动作”。一个 card 从一列进入下一列，不只是 UI 上换了位置，而是要经过 allowed source、WIP、required artifacts、manual approval 这些规则判断。也就是说，列本身带有阶段语义、准入语义和治理语义。

### 3. specialist / provider / workflow 才是执行层

> 路由通过以后，系统才会决定由哪个 specialist、哪个 provider、哪条 workflow 去执行。当前项目里这部分不是抽象概念，已经有 specialists 资源、flows / workflows / flow templates 这些能力，所以它更像一套建立在上下文之上的可配置执行层，而不是把逻辑写死在某个页面里。

### 4. session / run / trace 是过程证据层

> 真正难的不是触发执行，而是让过程透明。当前项目里已经有 session、workflow run、trace、background worker 这些执行痕迹，所以编排不是“发出去就算了”，而是能持续看到任务迁移、会话启动、步骤推进、失败重试和结果回写。换句话说，编排不仅要能跑，还要把证据带回来。

### 5. 最后再补治理边界

> 编排如果没有治理，很快就会退化成黑盒自动化。所以我会重点讲几类边界：WIP limit、entry rule、required artifacts、manual approval、auto advance。这些规则的意义不是把流程做复杂，而是让系统知道什么时候该继续推进，什么时候必须停下来等人工确认。

---

## 结合当前项目功能讲，会更像真项目

### 1. 现在已经有 intake 入口

> 当前项目里已经有 `kanban/intake` 这条入口，所以你可以很自然地讲：目标不是直接交给 agent，而是先进入项目上下文，变成后续 spec / task / card / session 能消费的对象。

### 2. 现在已经有列级自动化配置

> 当前项目里看板列已经不是简单 name + position，还带 automation 配置。像 `specialistId`、`provider`、`allowedSourceColumnIds`、`requiredArtifacts`、`manualApprovalRequired`、`autoAdvanceOnSuccess` 这些字段，本身就很适合拿来讲“上下文如何被继续推进”的语义。

### 3. 现在已经有 specialist 和 workflow 页面

> 当前项目里已经有 specialists 资源，也有 workflows、flows、flow templates、trigger 这些能力。这个点很加分，因为它说明编排不是停留在口头设计，而是已经有明确的配置和工作台入口。

### 4. 现在已经有实时事件和痕迹回流

> 当前项目里已经有 kanban event stream，前端也在消费像 `task.column-transition`、`background-task.session-started`、`task.session-completed` 这类事件。你可以很自然地说：前端不是只等一个最终结果，而是沿着事件流持续看到上下文和执行过程怎么变化。

### 5. 现在已经有 orchestration 快照页

> 当前项目里 orchestration 页面已经把 artifact gate、background worker、workflow runs、recent traces 这些东西放在同一个视图里。这很适合拿来证明：我们讲的不是“抽象调度”，而是真正把执行证据和治理信息放进了同一个工作台里。

---

## 如果面试官问“为什么这不是普通 chat UI”

### 推荐回答

> 因为 chat UI 只解决消息输入输出，但这里还要解决目标怎么结构化、任务怎么进入上下文、谁来执行、规则是否允许、过程怎么回写、失败怎么治理。当前项目里你能看到的 board、specialist、workflow、trace、artifact gate，这些都不是普通聊天页会有的能力。

---

## 如果面试官问“为什么不做纯前端乐观更新”

### 推荐回答

> 因为 Team AI 里很多动作不是前端自己说了算。比如卡片能不能进入某一列，要不要人工审批，artifact 是否齐全，这些都要靠后端规则判断。所以前端更像工作台：表达用户意图、展示中间态、等待 authoritative state 回流，而不是先抢着宣布结果。

---

## 如果面试官问“编排里最难的点是什么”

### 推荐回答

> 我觉得最难的不是拉起一个 session，而是让“上下文、执行、证据、治理”四件事保持一致。因为只要其中有一段断掉，系统就会退化成“看起来很智能，但实际上不好控”的 demo。

---

## 一个适合直接背的收口版本

> 所以如果让我总结 Team AI 的 Agent 编排，我会说它不是多开几个 agent，而是先把目标放进 intake 和项目上下文，再通过列级规则把任务路由到 specialist、provider 和 workflow，最后把 session、run、trace 和 artifact 持续回写到工作台里。这样系统不是只会自动执行，而是具备可观测、可治理、可复盘的执行能力。

## 相关拆解

- [[./Team AI 整个建模流程怎么讲|Team AI 整个建模流程怎么讲]]
- [[./Team AI 里看板为什么不是纯拖拽 UI|Team AI 里看板为什么不是纯拖拽 UI]]
- [[./Agent 智能体平台的前端架构怎么讲|Agent 智能体平台的前端架构怎么讲]]
- [[./Team AI 项目逐字稿|Team AI 项目逐字稿]]

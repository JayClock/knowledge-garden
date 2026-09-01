---
date: 2026-08-31 08:26:15
updated: 2026-08-31 08:27:45
---

# Evidence 项目：项目级与 Agent 级双层循环

> [!warning] 事实边界
>
> - [Evidence](https://github.com/JayClock/Evidence) 是本人公开维护的项目；本文核对版本为 `b4b9ace5badf7e4c37b13bd1e19f3499073bfff6`。
> - Evidence 是独立公开项目，不冒充上海鼎歆内部领域建模平台的公司源码或生产结果。
> - 当前已经实现 Story／Scenario／Tasking／Pair／Showcase／Respond 的权威状态与 Agent 执行循环，但完整 Modeling Profile 和“模型变更直接进入 modelRefs 再指导实现”的路径尚未完成；现有 Tasking 明确采用 `no_model_required`。
> - GitHub Actions 的最新核对结果不是全绿：Desktop 的 37 个测试文件、143 项测试和 Java Server build 通过，但整条 CI 因一个 Web UI 测试失败而失败。

## 核心观点

Evidence 不是让一个 Agent 从需求一路自由运行到提交代码，而是把软件交付拆成两个相互连接的循环：项目外层保存业务权威、阶段状态和人工决定，Agent 内层只在当前批准的任务边界内执行、检查和修正。两层通过不可变 Revision、Approved Plan、唯一 `nextAction` 和 append-only Evidence 交换信息。

```text
项目外层：Inbox → Kickoff → Understand → Tasking → Pair → Showcase → Respond
                              ↓ Approved Tasking Plan
Agent 内层：Guides → Test／Production／Refactor Driver → Sensors → Steer
                              ↓ Manifest／Observation／Exception
项目外层：人工批准、返回上游阶段或结束本轮
```

## 30 秒项目表达

我在公开项目 Evidence 中实现了一套项目级与 Agent 级双层循环。外层从 Inbox、需求澄清、任务规划一直管理到编码、价值验收和知识响应，并把关键决定保留给人；内层则由批准后的精确 Tasking Plan 驱动多个短生命周期 Agent，按 Red、Green、Refactor 和质量门执行。Server 每次只发布一个合法的 `nextAction`，失败会按证据返回测试、实现或 Tasking，而不是让 Agent 自己改变范围或直接提交代码。

## 2～3 分钟项目介绍

Evidence 是一个领域建模与证据映射平台，也是一套把人类判断和 Agent 执行分开的交付系统。项目外层从来源进入 Inbox 开始：来源形成不可变 Revision，Agent 只能提出 Candidate，人类选择后才冻结 Intake；Kickoff 仍要人工确认，确认以后才建立 Story。接着 Agent 可以提出澄清问题和 Scenario 草案，但 Scenario、任务计划和编码入口都要经过人工决定。

进入 Pair 前，系统会锁定精确 Story Revision、confirmed Scenario、Approved Tasking Plan、Git baseline、Nx 项目目录、测试工序和命令哈希。内层不再让一个 Agent 同时写测试、实现并判断自己是否正确，而是拆成 Test、Production 和 Refactor Driver，再用独立 Red Reviewer 判断失败是否真的是预期业务行为缺失。命令由 Controller 按批准计划执行，Agent 本身没有命令、提交、合并和推送权限。

如果出现 unexpected Green、pseudo-Red、Green 失败、路径越界、Git HEAD 变化或 evidence hash 不一致，Server 只开放与当前证据匹配的返回路径，例如回测试、回实现、重试质量门或回 Tasking。超过 Agent 调用、检查点和执行时间预算时会 fail closed，等待人工决定。

编码通过也不等于项目完成。人工确认完整 diff 后只创建本地 commit，Showcase 还会在 approved commit 上重新执行全部 Q2，并要求人记录实际产品观察和 Q3／Q4 风险。独立 Reviewer 给出建议后，领域专家才能接受、修改或拒绝；如果问题属于 Story、Scenario、模型、架构或测试策略，系统会返回对应阶段，而不是只让 Coding Agent 再试一次。

## 外层循环：管理项目权威和下一步

外层不是简单的阶段列表，而是显式保存“谁有权做什么”：

| 阶段       | Agent 可以做                                | 必须由人决定                        | 固化结果                        |
| ---------- | ------------------------------------------- | ----------------------------------- | ------------------------------- |
| Inbox      | 引用精确来源 Revision 提出 Candidate        | 选择、延期或拒绝 Candidate          | Frozen Intake                   |
| Kickoff    | 根据 Frozen Intake 提出替代方案             | confirm／revise／split／defer／stop | Story 与 baseline Revision      |
| Understand | 每轮提出一个问题或完整 Scenario Set         | 回答与确认 Scenario                 | 不可变 Story Revision、`SC-xxx` |
| Tasking    | 提出完整 Tasking Candidate                  | Desk Check approve 或返回知识缺口   | Approved Tasking Plan           |
| Pair       | 执行批准计划内的 Test／Production／Refactor | 处理异常并审批完整 diff             | Manifest 与本地 commit          |
| Showcase   | 重新执行 Q2、生成独立 Review                | 记录产品观察并接受／修改／拒绝      | Showcase Decision               |
| Respond    | 提出知识响应和 next Probe                   | 批准或要求修订                      | Respond Decision                |

因此，外层循环解决的是任务分解、WIP、阶段进度、权威归属和失败回流，而不是把这些决定留给 Agent 临场规划。

## 内层循环：控制一次 Agent 执行

### Guides

Pair 的输入不是完整仓库和一句高层目标，而是锁定后的执行包：

- 精确 Story Revision 与 Scenario；
- Approved Tasking Plan；
- 当前 TASK／TEST／process step；
- Git baseline 与允许修改的测试／生产路径；
- 已物化且经过语法校验的命令；
- 质量门、超时和最大 Agent 调用／检查点预算。

### Action

系统按职责启动独立的短生命周期 Agent：

- Test Driver 只能修改当前测试根；
- Production Driver 不能改测试，只完成最小实现；
- Refactor Driver 只能在当前已确认生产范围内重构；
- Red Reviewer 只有观察和分类能力，没有文件与命令工具。

### Sensors

- 锁定的 Red／Green 命令及退出状态；
- 独立 Red Review，区分行为失败与配置、依赖、网络、timeout 等 pseudo-Red；
- changed paths、before／after worktree hash 和 diff hash；
- lint、test、build、typecheck、API contract 和 package smoke；
- Showcase 中重新执行的 Q2、产品观察与 Q3／Q4 风险评价。

### Steer

Server 根据 append-only Evidence 计算唯一 `nextAction`。实现偏差可以回到测试或实现；计划、项目归属或证据边界错误返回 Tasking；产品价值和知识缺口则在 Showcase 中返回 Story、Scenario、模型、架构或测试策略阶段。Agent 不能自行扩大预算、绕过 Gate 或把建议升级成人工决定。

## 状态子系统如何连接两层

双层循环能够工作，关键不只是 Prompt，而是状态对象的接力：

```text
Frozen Intake
→ Story Revision
→ Scenario Set
→ Approved Tasking Plan
→ PairRun Checkpoint／Observation／Exception
→ Manifest／Diff Hash／Commit SHA
→ ShowcaseRun／Product Observation／Review
→ Respond Candidate／Decision
```

这些对象锁定对应版本和哈希，旧证据不覆盖、不删除。Desktop 可以中断和恢复，但重新开始时仍要从 Server 的权威资源重建当前上下文，并继续执行 Server 发布的下一步。

## 模型怎样进入实现：当前做到哪里

Evidence 当前已经把上游判断逐层压缩为 Story、Scenario 和 Approved Tasking Plan，再作为 Pair 的 Guides。它解决了“当前为什么做、要观察什么、执行哪些 TEST、允许改哪里和怎样验收”。

但是当前实现选择了一条明确的无模型影响路径：人工确认 `tool / none / false` 后，Tasking 中的 `modelRefs` 必须为空。因此不能声称已经完成：

```text
领域模型变更
→ confirmed model refs
→ TASK／TEST
→ 代码与回归测试
```

这一边界反而说明系统没有用空引用或 Agent 推断冒充已经完成的模型驱动交付。后续若实现完整 Modeling Profile，应让模型版本、不变条件和关系引用进入 Tasking，并在模型变化时使下游 Plan 和 Pair authority 失效。

## 职业能力表达

> 公开维护 Evidence 领域建模与证据映射平台，将软件交付建模为项目外层与 Agent 内层双层循环：外层以不可变 Revision、Approved Plan、append-only Decision 和人工 Gate 管理业务权威与阶段回流；内层以受限 Test／Production／Refactor Agent、独立 Red Review、锁定命令、质量门和有限预算完成可恢复的自我纠正，并由 Server 根据证据发布唯一下一步。

这段经历支持的不是“会调用大模型”，而是以下能力组合：

- 把业务判断、Agent 候选和人工权威分层；
- 把模型、Scenario、任务、测试、代码和价值反馈组织成可追踪状态；
- 分离推断型 Agent 与确定性命令、哈希和质量门；
- 根据失败所属层级返回正确阶段，而不是无边界重试；
- 同时实现 React／Electron、Java Domain／REST、PostgreSQL 和本地 Agent Runtime。

## 高频追问

1. 为什么 Candidate selection 不能直接创建 Story？
2. Frozen Intake、Story Revision 和 Approved Tasking Plan 分别冻结什么？
3. 为什么 Test、Production、Refactor Driver 要拆成不同 Session？
4. 如何判断一次 Red 是业务行为缺失，而不是 pseudo-Red？
5. Server 发布唯一 `nextAction` 与普通前端状态机有什么区别？
6. 哪些失败留在 Agent 内层修正，哪些必须返回 Tasking 或 Understand？
7. 为什么 Pair 全绿后还要重新执行 Showcase Q2？
8. 当前为什么只能声称 `no_model_required`，完整模型驱动实现还缺什么？
9. 为什么只创建本地 commit，而不允许 Agent 自动 merge／push？
10. 最新 CI 为什么失败？哪些子系统验证已通过，哪些不能说成全绿？

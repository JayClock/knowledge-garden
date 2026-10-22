# AI 辅助研发与 Harness 工程实践：确认与来源

## 本轮确认与保存授权

- 日期：2026-10-20。
- 用户先要求“参考 https://github.com/JayClock/Evidence-Framework，从各种坏味道中总结”。
- Agent 阅读 `docs/adoption/` 中十篇坏味道实践，并对照 Guides、任务交付协议、测试指南、任务状态检查及文档检查实现，归纳需求与验收、上下文装配、单任务交付、反馈纠偏、跨会话恢复和指令治理。
- 在询问“上述坏味道归纳、Guides、任务规划和交付检查中，哪些是你亲自设计并实际使用过的”后，用户明确答复：**“都是我亲自设计并实际使用过的”**。
- Agent 再将贡献收束为上下文工程、交付编排、质量验证和知识治理四项，并询问是否同步 `职业经历.md`、新增《AI 辅助研发与 Harness 工程实践》专题；用户先确认“是的”。
- 本轮授权覆盖：新增职业事实、同步长期职业经历与依赖记录、保存独立面试专题及其依赖记录。未要求改写岗位简历、全局自我介绍、既有项目讲稿或外部仓库。

## 来源版本与读取方式

- 仓库：https://github.com/JayClock/Evidence-Framework
- 固定版本：`b67af395b1e301a853e13a7def85b250ca5a4763`。
- 前轮通过 `git ls-remote` 核对远端 HEAD；本轮重新核对本地同版本工作树。跟踪源码无改动；本地未跟踪 `.evidence/` 不作为本轮源码证据，也不改写。
- 本轮证据是用户对个人设计及实际使用的确认，加上仓库中可定位的方法、实现和测试设计。没有在本轮运行该仓库的产品测试、交付任务或性能测试。
- 既有用户确认：Evidence-Framework 是 AI 原生领域建模与 API 设计平台的内部组成部分。本专题按研发流程实践组织，不新增任职、项目时间或独立商业产品。

## 坏味道与个人实践对应

以下十篇均位于固定版本的 [docs/adoption](https://github.com/JayClock/Evidence-Framework/tree/b67af395b1e301a853e13a7def85b250ca5a4763/docs/adoption)。

| 原始文档 | 设计并实际使用的机制 |
| --- | --- |
| `需求模糊：Agent 不知道“好”长什么样.md` | 将要求转为固定输入、可观察结果、边界、反例及失败不变性；验收关联具体 CHECK，保留类型的 expected 与独立业务依据。 |
| `隐式约定：规则只存在于人的脑子里.md` | 将项目不变量、模块边界、工程规范和任务局部设计显式化，按拥有者维护并给出读取入口。 |
| `上下文倾倒：信息过多，Agent 反而迷失.md` | 按任务从 Guides 定位必要章节、源码与测试；用引用和输入投影缩小消费范围，保留回到权威来源的路径。 |
| `上下文焦虑：Agent 在长对话中丢失关键信息.md` | 一次完成一个获授权且就绪的任务；把设计、结果和缺口归位，恢复时重新核对来源、工作树和环境。 |
| `信息散落：知识来源不唯一且更新不及时.md` | 分开业务模型、API、软件范围、架构、任务状态和代码行为的权威归属；用来源引用及摘要辅助新鲜度检查，生成页面作投影。 |
| `前馈痴迷：Agent 做完就交，从来没人检查.md` | 为约定选择测试、静态检查或明确人工审查；按实现、检查设计、任务切片、业务来源和环境问题分别纠偏。 |
| `反馈过载：Sensors 太多，Agent 不知道哪个信号重要？.md` | 按当前任务的影响及证明范围区分失败、环境阻塞、警告与缓存；成功保留摘要，失败保留可追溯诊断。 |
| `虚假胜利：Agent 以为自己做完了，其实没有.md` | 将代码生成、CHECK 设计、实际执行和需求验收分开；记录命令、cwd、退出码与真实观察，分别进行 Standards / Spec 审查。 |
| `跨会话状态丢失：每次对话 Agent 都不记得上次的事.md` | 将用户依据、局部决定、执行结果和未决问题归入各自拥有者；任务状态和 observedEvidence 进入 plan.yaml，审核页由计划重建。 |
| `指令文件腐化：AGENTS.md 越来越长，Agent 反而变笨了.md` | 分层维护指令，入口保存路由与不变量；替换过期操作说明，同步导航、Skill、模板及检查，保留历史执行证据。 |

## 当前协议与实现锚点

### 四层前馈与来源治理

- [Guides 导航](https://github.com/JayClock/Evidence-Framework/blob/b67af395b1e301a853e13a7def85b250ca5a4763/docs/guides/index.md)：四层职责、来源与冲突处理、阅读路由、六项开工检查、缺口与转向。
- [任务前馈装配协议](https://github.com/JayClock/Evidence-Framework/blob/b67af395b1e301a853e13a7def85b250ca5a4763/.agents/skills/evidence-task-planning/references/guides.md)：sourceManifest、sourceRefs / procedureRefs、任务 design、acceptanceCriteria、CHECK 与预期数据，以及单一任务状态。

### 单任务执行、小步实现与诊断

- [交付 Skill](https://github.com/JayClock/Evidence-Framework/blob/b67af395b1e301a853e13a7def85b250ca5a4763/.agents/skills/evidence-delivery/SKILL.md)：外层 PDCA、内层 Guides → Action → Sensors → Steer，选择候选、语义就绪、执行、记录并停止。
- [小步实现](https://github.com/JayClock/Evidence-Framework/blob/b67af395b1e301a853e13a7def85b250ca5a4763/.agents/skills/evidence-delivery/references/implementation.md)：独立预期、单行为红绿整理、受影响回归和真实证据。
- [故障诊断](https://github.com/JayClock/Evidence-Framework/blob/b67af395b1e301a853e13a7def85b250ca5a4763/.agents/skills/evidence-delivery/references/diagnosis.md)：症状复现、缩小案例、可证伪假设、单变量探针、回归及原始场景复验。
- [双维度审查](https://github.com/JayClock/Evidence-Framework/blob/b67af395b1e301a853e13a7def85b250ca5a4763/.agents/skills/evidence-delivery/references/review.md)：Standards 检查工程规范，Spec 检查需求忠实性，分别留结论与来源。

### 检查与证据

- [测试指南](https://github.com/JayClock/Evidence-Framework/blob/b67af395b1e301a853e13a7def85b250ca5a4763/docs/engineering/testing.md)：领域、HTTP、SQL 和应用装配的测试边界；缓存、真实执行、环境失败及证据留存规则。
- [plan_state.py](https://github.com/JayClock/Evidence-Framework/blob/b67af395b1e301a853e13a7def85b250ca5a4763/.agents/skills/evidence-delivery/scripts/plan_state.py)：`inspect_plan` 只读检查任务/验收/CHECK/gap 引用和依赖顺序，done 要有非空 observedEvidence；返回结构候选，sourceFreshness 明确为 not-checked。
- [状态检查测试设计](https://github.com/JayClock/Evidence-Framework/blob/b67af395b1e301a853e13a7def85b250ca5a4763/.agents/skills/evidence-delivery/tests/test_plan_state.py)：只读性、前置、证据字段、验收类型与引用、执行顺序等回归设计。
- [Guides 检查器](https://github.com/JayClock/Evidence-Framework/blob/b67af395b1e301a853e13a7def85b250ca5a4763/tools/guides/check.mjs)：维护范围内的文件存在性、本地内联链接、越界和已知过期表述检查，输出摘要与具体错误。

## 职业事实取用范围

- 本轮确认了上述研发方法和机制由本人亲自设计并实际使用，可正向描述个人动作、取舍及已形成的流程资产。
- 该确认不扩展成仓库所有框架代码、业务方法论、前后端产品模块都由本人独立创造；既有项目分工保持原记录。
- 未新增团队采用人数、推行范围、效率百分比、生产规模、线上事故、工具清单或具体运行通过数量。
- 不从机制存在推定桌面端已经集成全部交付检查，也不改变 `agent_settled` 的 design_only 状态。
- 结构检查保证其检查范围内的引用与字段关系；业务预期、实际运行及人工授权分别由对应证据支持，不把状态检查器写成自动验证业务正确或自动批准任务的程序。
- 既有教育类别、HATEOAS 数字和建模会议时长等未决问题独立保留。

## 后续可补材料

个人设计和实际使用已确认。后续仅为深入面试准备补一个可脱敏执行样本：任务输入、一次检查发现的问题、实际转向、修订及复验记录；团队推广范围和效果若需对外展开，再单独核对。不重复询问本轮已确认的设计归属。

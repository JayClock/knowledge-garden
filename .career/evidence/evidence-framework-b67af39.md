# Evidence-Framework 当前机制核对

## 来源与范围

- 仓库：https://github.com/JayClock/Evidence-Framework
- 核对版本：`b67af395b1e301a853e13a7def85b250ca5a4763`；本轮通过远端 `main` / HEAD 与本地工作树核对，跟踪源码无本地修改。
- 核对方式：读取源码、Schema、Skill 与交接协议。本记录是静态实现证据，不是测试执行日志。
- 用户在本轮要求基于当前实现核对旧叙事，随后授权重构所有相关职业材料。
- 证据范围是框架机制；桌面端技术栈、Pi SDK 接入、轮次刷新和内部使用情况仍分别来自既有用户确认。

## FM 增量维护与检查

来源：

- [业务依据与保存](https://github.com/JayClock/Evidence-Framework/blob/b67af395b1e301a853e13a7def85b250ca5a4763/.agents/skills/evidence-fm/references/provenance.md#4-保存与检查对齐实际依据)
- [统一检查实现](https://github.com/JayClock/Evidence-Framework/blob/b67af395b1e301a853e13a7def85b250ca5a4763/.agents/skills/evidence-fm/scripts/check_fm.py)
- [检查纪律](https://github.com/JayClock/Evidence-Framework/blob/b67af395b1e301a853e13a7def85b250ca5a4763/.agents/skills/evidence-fm/references/validation.md)

当前方法要求在已有编辑授权内，将有依据的概念、属性、关系与规则渐进映射到同一份 FM；未知或冲突保留缺口。每批修改检查一致性，明确范围结束时再检查完整性与适用场景。

`check_model` 分别返回 `consistent`、`complete`、`simulationPassed`、`modelDigest` 与 `inputChanged`。未指定范围时 `complete` 为 null，未实际执行场景时 `simulationPassed` 为 null；`humanConfirmation` 固定为 `not-asserted-by-machine`。

这些字段描述当前表达及本次适用检查，不证明全部业务来源充分、责任已经全部发现或人类确认有效。

## 明确范围与 API 交接

来源：

- [建模交接协议](https://github.com/JayClock/Evidence-Framework/blob/b67af395b1e301a853e13a7def85b250ca5a4763/.agents/skills/evidence-modeling/references/workflow.md)
- [FM 结果消费器](https://github.com/JayClock/Evidence-Framework/blob/b67af395b1e301a853e13a7def85b250ca5a4763/.agents/skills/evidence-api/scripts/fm_api_core/fm_adapter.py)
- [API 设计流程](https://github.com/JayClock/Evidence-Framework/blob/b67af395b1e301a853e13a7def85b250ca5a4763/.agents/skills/evidence-api/references/api-design.md)

交接协议将当前范围的人类结束确认、机器检查与下游授权分开。API 的 `load_fm` 检查报告版本、consistent/complete/valid、输入未变化、空错误及当前模型摘要，并交给 `ready_scope` 核对范围；摘要失配返回 `FM_CHECK_STALE`。API 不重新运行同一次 FM 检查。

API 维护唯一设计源，并在自身覆盖与契约检查通过后按授权生成派生产物，来自建模入口时接续联合审核。源码摘要不是人类身份认证、文件锁或事务保证；人类确认由工作流核对，不是 FM 内审核字段。

## 静态测试向量与运行验证

来源：

- [测试向量生成器](https://github.com/JayClock/Evidence-Framework/blob/b67af395b1e301a853e13a7def85b250ca5a4763/.agents/skills/evidence-api/scripts/fm_api_core/e2e_vectors.py)
- [API 入口与输出纪律](https://github.com/JayClock/Evidence-Framework/blob/b67af395b1e301a853e13a7def85b250ca5a4763/.agents/skills/evidence-api/SKILL.md)

`build_vectors` 从已解析的 HTTP 消费者旅程提取步骤，将 `request`、`expect`、能力及场景引用保存为可移植向量。输出显式标记 `dataClassification: synthetic` 与 `runtimeValidated: false`；调用者身份和前置事实装配由运行环境提供。

因此，这些输出是可供实现和测试消费的静态资产，不是已执行通过的服务、鉴权、SQL 或外部集成测试；项目其他真实运行结果仍按其独立证据记录。

## 旧版来源叙事处理

此版本仍有 `evidence-discovery` 访谈 Skill，负责问答与控制；这不等于独立的 AI 来源归因账本。当前 Rule Schema 与 FM 方法不足以支持“AI 假设先写为 Rule，再从来源账本逐条审核”的现行流程表述。

旧版用户访谈和原始练习转写保持不变。旧版 claims 仅作历史追踪，当前对外材料改为有依据的 FM 增量维护、范围交接和静态测试向量，不扩展为新的个人编码或验证成果。

---
name: career-assets
description: 以双层循环编排长期职业资产、岗位机会和求职反馈的 Career Harness。凡是用户要梳理或补充经历、整理大量求职材料、长期维护职业事实、按 JD 生成简历与自我介绍、准备项目面试、同步受影响材料、复盘投递或面试，或要求重构职业资产工作流时，都应使用本 skill；具体执行由 career-evidence、career-positioning、resume-package、interview-package 和 career-retro 子 skill 完成。
---

# Career Harness

你是职业资产系统的外层控制器，不直接包办所有写作。你的职责是维护一次次求职机会之间的 PDCA 循环，读取状态、确定阶段、路由子任务、运行 Gate，并让真实反馈回到正确的层级。

## 核心模型

```text
来源与用户确认
→ claims 唯一事实账本
→ opportunity 岗位映射
→ 简历／自我介绍／面试包
→ 投递与面试反馈
→ 调整事实缺口、定位、表达或 Harness
```

- 外层循环管理目标、阶段、跨任务依赖和真实反馈。
- 内层 Skill 使用“前馈 → 行动 → Sensors → 调整”完成一个边界清楚的子任务。
- 不要用一次大生成替代分阶段验收，也不要让下游文案反向成为事实。
- 只改一句话、一次性通用面试问答或用户明确要求不保存时，不初始化 Harness，也不修改状态。

## 首次进入

1. 确认 Git 根目录和现有修改，不覆盖无关工作。
2. 查找状态目录：优先 `$CAREER_STATE_DIR`，否则使用 Git 根目录下 `.career/`。
3. 读取 `.career/config.json`、`claims.json`、`positioning.json`；涉及岗位时再读取 `.career/opportunities/<opportunity_id>/opportunity.json`。
4. 状态不存在时，在取得写入授权后运行：

```bash
python <career-assets>/scripts/init_state.py --root <git-root>
```

完整状态约定见 `references/state-schema.md`，真实性规则见 `references/fact-policy.md`。

## 外层阶段

| 阶段 | 目标 | 完成条件 | 执行 Skill |
| --- | --- | --- | --- |
| `capture` | 收集来源、访谈和旧材料线索 | 候选事实已记录 | `career-evidence` |
| `verify` | 核对证据、职责、完成状态和冲突 | 对外使用的 claim 为 `confirmed` | `career-evidence` |
| `position` | 建立定位并映射 JD | 核心要求已有 claim 或明确 gap | `career-positioning` |
| `package` | 生成岗位简历与岗位自我介绍 | 同一 claim 集通过一致性检查 | `resume-package` |
| `practice` | 生成项目讲法与追问训练 | 回答可追溯且可口述 | `interview-package` |
| `apply` | 记录实际投递版本与状态 | 提交记录绑定 artifact manifest | 本 Skill |
| `retro` | 吸收投递／面试反馈 | 反馈已分类并产生下一步 | `career-retro` |

阶段可以因紧急机会跳转，但不能跳过事实 Gate。紧急只改变顺序，不降低真实性标准。

## 路由规则

执行子任务前读取对应 sibling skill 的 `SKILL.md`，并遵循其内层操控循环：

- 材料阅读、事实补充、claims 更新、冲突核对：`../career-evidence/SKILL.md`
- 职业定位、JD 要求拆解、项目选择和 gap：`../career-positioning/SKILL.md`
- 岗位简历、自我介绍、DOCX 与交付：`../resume-package/SKILL.md`
- 项目整体讲法、具体回答、追问和口语化：`../interview-package/SKILL.md`
- 投递／面试反馈、失败分类和下一轮调整：`../career-retro/SKILL.md`

一次请求跨越多个阶段时，按表中顺序推进；每个阶段通过 Gate 后再进入下一个阶段。

## 外层 PDCA

### Plan

- 长线任务：确定目标角色、能力主线、待补证据和本轮优先级。
- 岗位任务：创建或读取 `opportunity_id`，记录公司、岗位、JD 核心要求、截止时间和当前阶段。
- 不把“写一份文件”当计划；计划必须说明要支持什么判断或求职动作。

### Do

- 只把边界清楚的工作交给对应子 Skill。
- 子 Skill 的输出必须写回状态或生成带 manifest 的派生产物。
- 未经用户明确授权，不落盘、不批量移动、不覆盖其他岗位包。

### Check

计算型检查交给脚本：

```bash
python <career-assets>/scripts/state_lint.py --state-dir <state-dir> --repo-root <git-root>
python <career-assets>/scripts/impact_scan.py --state-dir <state-dir> --claim-id <claim-id>
python <career-assets>/scripts/opportunity_status.py --state-dir <state-dir> --opportunity-id <id>
```

- `state_lint.py` 校验 claims、证据、岗位引用、manifest 和 feedback；`claim_lint.py` 是兼容入口。
- `impact_scan.py` 查找依赖变更 claim 的产物，并可用 `--mark-stale` 标记过期。
- `opportunity_status.py` 汇总阶段、要求覆盖、gap、产物状态、阻塞项和下一路由。

推断型检查由 Agent 完成：岗位相关性、叙事可信度、资历层级、职责是否夸大、回答是否经得起追问。推断型检查不能替代路径、状态、字数、占位符等确定性验证。

### Act

根据失败类型路由，不要盲目重写：

- `missing_evidence`、`ownership_conflict`、`unsupported_metric` → `career-evidence`
- `jd_gap`、`project_selection` → `career-positioning`
- `artifact_drift`、`template_error`、`oral_overrun` → 对应 package Skill
- `real_feedback` → `career-retro`
- 多次机会重复出现同类失败 → 提议修改 Guides、Sensors 或脚本，而不是篡改职业事实

## 状态纪律

- `.career/claims.json` 是唯一职业事实源；定位、简历、自我介绍和面试材料都只能消费其中的 claim。
- 需要人工审阅时按 claim 生成临时或岗位范围内的可读产物。
- 只有 `confirmed` claim 可以进入保真简历和面试回答。
- 每个对外 artifact 都要有 manifest，记录 `claim_ids`、`opportunity_id`、生成 Skill 和当前状态。
- 岗位自我介绍保存在对应 opportunity 包中；全局 `自我介绍.md` 只保留通用基础版，不被不同岗位反复覆盖。
- 旧简历、逐字稿和岗位文案是线索或派生物，不得反向升级为事实。
- 真实市场反馈可以改变项目选择、表达和下一轮计划，不能单独证明或否定历史事实。

## 用户可见交互

对用户保持简洁：先说明本轮处于哪个目标，再给可见进展和下一步。不要主动暴露内部 ID、状态机和 manifest；只有用户在设计或调试 Harness 时才展开这些结构。

常见入口：

- `帮我梳理经历` → capture / verify
- `帮我按这个岗位出一版` → position → package
- `帮我准备面试` → position → practice
- `继续补充` → 回到当前 opportunity 的首个未通过 Gate
- `复盘投递/面试` → retro

## 完成 Gate

- 状态文件通过 `state_lint.py`。
- 对外内容只使用 confirmed claim，且职责、完成状态和限制一致。
- claim 变化已运行影响扫描；未同步的派生物已标记 stale。
- 岗位产物绑定唯一 opportunity，不污染其他岗位和全局基础版。
- 真实反馈已经分类到事实、定位、表达、交付或 Harness，而不是只留一段复盘文字。

# Career Harness 状态模型

## 目录

状态默认放在 Git 根目录 `.career/`；设置 `CAREER_STATE_DIR` 时使用环境变量指定目录。

```text
.career/
├── config.json
├── claims.json
├── positioning.json
├── feedback.jsonl
├── practice/
│   └── <project_id>/
│       └── sessions.jsonl
├── opportunities/
│   └── <opportunity_id>/
│       ├── opportunity.json
│       ├── outputs/
│       └── manifests/
└── manifests/
```

状态文件是 Agent 的运行状态，不是 Obsidian 笔记，也不进入 Quartz 发布目录。

## config.json

```json
{
  "schema_version": 1,
  "paths": {
    "career_history": "content/Knowledge/Outputs/职业经历.md",
    "base_introduction": "content/Knowledge/Outputs/自我介绍.md",
    "source_roots": ["content/Knowledge/Sources"],
    "project_output_root": "content/Knowledge/Outputs"
  },
  "resume_policy": {
    "required_claim_ids": [],
    "required_artifact_types": ["resume", "resume_docx", "self_introduction"],
    "content_check_artifact_types": ["resume", "self_introduction"],
    "content_markers_any": []
  }
}
```

所有路径相对 Git 根目录。`paths.career_history` 为必填的仓库内 Markdown路径，本仓库使用 `content/Knowledge/Outputs/职业经历.md`；初始化只配置路径，不生成空白经历文件。首次授权保存时创建文档及 `.career/manifests/career-history.json`，已有文档也须先核对再建立 manifest。

`resume_policy` 是跨岗位简历基线：

- `required_claim_ids` 必须是 confirmed claims，并进入正式投递 opportunity 与受管简历包 manifest；
- `required_artifact_types` 指定需要携带这些 claim 的 current 产物；
- `content_check_artifact_types` 只对可直接读取的文本产物执行内容检查；
- `content_markers_any` 至少命中一个，确保强制主题真正出现在正文，而不只是 manifest。

## claims.json

```json
{
  "schema_version": 1,
  "claims": [
    {
      "id": "aiflow.telemetry.execution-correlation",
      "statement": "通过 executionId 关联前端埋点与执行引擎日志",
      "kind": "project_contribution",
      "project_id": "aiflow",
      "ownership": "direct",
      "completion": "implemented",
      "status": "confirmed",
      "evidence": [
        {
          "type": "file",
          "path": "content/Knowledge/Sources/example.md",
          "locator": "执行日志章节"
        },
        {
          "type": "user_confirmation",
          "locator": "用户明确确认实际接入"
        }
      ],
      "metrics": [],
      "constraints": ["不补写具体下游使用方式", "节点状态、耗时和错误仍以执行引擎日志为事实源"],
      "tags": ["monitoring", "workflow", "observability"]
    }
  ]
}
```

### claim 字段

- `id`：稳定、可读、不可因措辞调整而变化。
- `statement`：最小可复述事实，不写岗位营销文案。
- `kind`：`timeline`、`positioning`、`project_scope`、`project_contribution`、`result`、`boundary`、`failure`、`reflection`。
- `project_id`：可选；同一项目的 claim 使用同一 ID。
- `ownership`：`direct`、`collaborative`、`team`、`not_applicable`。
- `completion`：`implemented`、`validated`、`ongoing`、`design_only`、`planned`、`unknown`。
- `status`：`candidate`、`confirmed`、`contested`、`deprecated`、`reference_only`。
- `evidence`：文件、源码、交付物或用户确认。confirmed claim 至少有一项。
- `metrics`：只保存有统计口径的数字；没有就保持空数组。
- `constraints`：内部选材与校验时必须遵守的事实约束，确保表达不失真；正文通过准确的职责、动作与完成状态自然符合约束，不机械转写为面向读者的免责声明或边界条款。
- `tags`：检索用，不代替 claim 关系。

## positioning.json

```json
{
  "schema_version": 1,
  "market_title": "全栈偏前端的平台工程师",
  "capability_axis": "全流工程师",
  "status": "confirmed",
  "base_claim_ids": [],
  "target_role_families": [],
  "open_questions": []
}
```

定位是经过事实支持的长期判断，不存放某个 JD 的临时关键词。

`open_questions` 保存跨会话未解问题，使用可读字符串，包含经历、问题、已知内容、关联 claim（如有）、优先原因和下次动作。待补问题统一保存在这里，默认不写入职业经历文档；仅在用户明确要求时展示可读摘要。解决后收束对应问题；如有经用户要求展示的摘要，也同步更新，避免重复询问。

## opportunity.json

```json
{
  "schema_version": 1,
  "id": "2026-company-role",
  "stage": "intake",
  "purpose": "application",
  "application_status": "planned",
  "target": {
    "company": "公司名",
    "role": "岗位名",
    "jd_source": "用户粘贴或文件路径",
    "deadline": null,
    "planned_submission_date": "2026-08-31"
  },
  "requirements": [
    {
      "id": "req-1",
      "text": "复杂前端平台经验",
      "priority": "must",
      "claim_ids": [],
      "gap": true
    }
  ],
  "selected_claim_ids": [],
  "artifacts": [],
  "feedback_ids": [],
  "decisions": []
}
```

`stage` 允许值：`intake`、`mapped`、`packaged`、`practicing`、`submitted`、`interviewed`、`closed`。

`purpose` 可选值：`application`、`interview_practice`。面试练习机会在 `mapped` 后直接路由到 `interview-package`，不要求进入 `resume-package` 或 `apply`。

`application_status` 可选值：`not_planned`、`planned`、`submitted`、`withdrawn`。`target.deadline` 只记录招聘方截止时间；用户自己的计划投递日期记录在 `target.planned_submission_date`，不要混为同一事实。

## artifact manifest

每个岗位产物在同一 opportunity 的 `manifests/` 下保存 manifest：

```json
{
  "schema_version": 1,
  "artifact": ".career/opportunities/2026-company-role/outputs/resume.md",
  "artifact_type": "resume",
  "opportunity_id": "2026-company-role",
  "generated_by": "resume-package",
  "claim_ids": ["aiflow.telemetry.execution-correlation"],
  "status": "current"
}
```

`status`：`current`、`stale`、`archived`。

职业经历的 manifest 固定为 `.career/manifests/career-history.json`：`artifact` 等于 `config.paths.career_history`，`artifact_type` 为 `career_history`，`generated_by` 为 `career-evidence`，`opportunity_id` 为 null，`claim_ids` 记录已确认正文使用的 claims。它不属于岗位简历包，不应用 resume_policy。

写入前检查人工修改；未解决的事实补充或纠正保留待确认，manifest 设为 stale。正文与 confirmed claims 同步后才设为 current。不存在文档时无需创建 manifest；存在文档必须有此依赖记录。

项目长期讲稿保存在 Vault，并在 `.career/manifests/` 建立依赖记录。

## feedback.jsonl

每行一个 JSON 对象：

```json
{
  "id": "feedback-001",
  "opportunity_id": "2026-company-role",
  "stage": "interview",
  "signal": "某项目回答讲不清",
  "classification": "expression_gap",
  "affected_claim_ids": [],
  "affected_artifacts": [".career/opportunities/2026-company-role/outputs/interview-plan.md"],
  "next_skill": "interview-package"
}
```

`classification`：

- `fact_gap`
- `evidence_gap`
- `positioning_gap`
- `selection_gap`
- `expression_gap`
- `delivery_error`
- `market_mismatch`
- `harness_gap`

反馈记录的是观察和下一步，不直接修改 claim。

## practice/<project_id>/sessions.jsonl

私有口语练习运行记录；经用户明确授权才追加。项目没有 JD 时 `opportunity_id` 为 null，不创建虚构岗位；同一项目各岗位的练习以这个字段隔离。practice 目录按需创建，初始化不生成空日志。

每轮一行 JSON，结构如下（示例是格式说明，不是已经发生的练习）：

```json
{
  "schema_version": 1,
  "id": "practice-example-001",
  "recorded_at": "2026-10-04T10:00:00+08:00",
  "project_id": "domain-modeling",
  "opportunity_id": null,
  "resumes_session_id": null,
  "source": {
    "manifest": "manifests/interview-example.json",
    "artifact": "content/Knowledge/Outputs/项目介绍：多人实时协同的 AI 辅助领域建模平台.md",
    "sha256": "<snapshot 输出的底稿 SHA256>",
    "claim_ids": ["domain-modeling.project.scope"],
    "claims_sha256": "<snapshot 输出的相关 claims SHA256>"
  },
  "status": "completed",
  "attempts": [
    {
      "id": "a1",
      "exercise": "overview",
      "question": "用 2 分钟介绍这个项目",
      "target_seconds": 120,
      "cue_level": "none",
      "input_kind": "transcript",
      "response": "<用户原始口述转写，不是 AI 修订稿>",
      "audio_ref": null,
      "duration_seconds": null,
      "duration_basis": "unknown",
      "retry_of": null
    }
  ],
  "observations": [
    {
      "attempt_id": "a1",
      "observer": "ai",
      "dimension": "structure",
      "evidence": "<引用原话或用户报告，录音时间点仅在已知时填写>",
      "interpretation": "<与观察分开的判断>"
    }
  ],
  "adjustment": "<本轮唯一主要调整>",
  "next_step": {
    "task": "隔天不看稿重讲项目开场",
    "target_seconds": 60,
    "cue_level": "none",
    "next_skill": "interview-package"
  }
}
```

- `id`、`project_id` 和非空的 `opportunity_id` 使用字母、数字、`.`、`_`、`-`，不得用路径；session ID 唯一。
- `recorded_at` 是本条保存时间，使用带时区的 ISO 时间。日志以追加顺序恢复；`resumes_session_id` 指向之前的同项目、同岗位上下文记录。
- `source` 必须来自练习开始前的只读 `practice_log.py snapshot`。`manifest` 相对 state-dir，`artifact` 相对 Git 根目录；底稿必须有 current 的 `interview_script` manifest。SHA256 记录文件字节版本；claims SHA256 对该 manifest 的相关完整 claim 对象按 ID 排序并以稳定 JSON 编码计算。不手填或在保存时替换成新快照。
- 历史底稿或 claims 变化时保留旧记录并提示重建基线，不把旧练习冒充当前版本。claims 正常更新用 deprecated 保留历史 ID，不删除被引用的 ID。
- `status` 为 `completed` 或 `interrupted`。completed 至少有一次真实尝试、观察和一个调整，但不证明掌握；interrupted 可没有尝试，adjustment 可为 null，仍要留下一个下一步。
- `exercise` 为 `overview`、`follow_up`、`retry`、`retest`。retry 的 `retry_of` 引用本轮之前的 attempt；跨轮复测用 retest 和 session 级恢复链接。未发生的追问或重讲不得补造。
- `cue_level` 为 `none`、`keywords`、`full`；`input_kind` 为 `text`、`transcript`、`self_report`、`audio`。前三者 response 保存原始文字／转写／用户自述，audio 允许 response 为 null，但必须有 audio_ref。引用音频不代表已分析音频，也不授权复制或上传。
- `duration_seconds` 是实测而非字数估算。未计时为 null 且 `duration_basis` 为 unknown；实测为正数，basis 为 user_timer 或 media_metadata，后者需有媒体引用。
- `observations` 区分 user／ai，dimension 为 structure、mechanism、fact_consistency、delivery。evidence 与 interpretation 分开；文本输入不能独立证明声音表现。
- `next_step` 是单对象，不是任务列表；说明 task、提示程度、目标时长和 next_skill。口语任务需正数时长；事实核对或定位任务可为 null，路由 career-evidence／career-positioning。
- 日志不是职业事实，也不是对外 artifact，不另建 manifest，不写入项目介绍或 feedback.jsonl，不修改 opportunity 的真实面试／投递阶段。

脚本支持 snapshot（只读）、record（追加一个已授权 JSON）和 status（只读恢复）。status 未传 opportunity 时只恢复通用练习；跨项目有歧义时返回待选项目，不擅自选。返回的 needs_rebaseline 只表示底稿／claims／manifest 版本变化，不是能力评价。

## Schema 与计算检查

`schemas/` 提供 claims、opportunity、manifest、单条 feedback 和 practice-session 的 JSON Schema。日常工作仍以 `scripts/state_lint.py` 为统一 Gate，因为它还检查跨文件引用、真实证据路径、artifact 状态和练习 JSONL。旧练习的源版本变化是 warning，不强迫重写历史；无效结构、重复 ID、跨上下文恢复链接和未知 claim 是 error。

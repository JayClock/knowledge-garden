# Career Harness 状态模型

## 目录

状态默认放在 Git 根目录 `.career/`；设置 `CAREER_STATE_DIR` 时使用环境变量指定目录。

```text
.career/
├── config.json
├── claims.json
├── positioning.json
├── feedback.jsonl
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
- `constraints`：对外表达时必须保留的事实边界。
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

`open_questions` 保存跨会话未解问题，使用可读字符串，包含经历、问题、已知内容、关联 claim（如有）、优先原因和下次动作。职业经历中的待补问题是它的可读摘要；解决后同步收束，不重复询问。

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

## Schema 与计算检查

`schemas/` 提供 claims、opportunity、manifest 和单条 feedback 的 JSON Schema。日常工作仍以 `scripts/state_lint.py` 为统一 Gate，因为它还检查跨文件 claim 引用、真实证据路径、artifact 状态和 JSONL。

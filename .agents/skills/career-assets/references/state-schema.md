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
    "base_introduction": "content/Knowledge/Outputs/自我介绍.md",
    "source_roots": ["content/Knowledge/Sources"],
    "project_output_root": "content/Knowledge/Outputs"
  }
}
```

所有路径相对 Git 根目录。迁移到其他仓库时只改配置，不改 Skill 指令。

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
      "constraints": [
        "不补写具体下游使用方式",
        "节点状态、耗时和错误仍以执行引擎日志为事实源"
      ],
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

## opportunity.json

```json
{
  "schema_version": 1,
  "id": "2026-company-role",
  "stage": "intake",
  "target": {
    "company": "公司名",
    "role": "岗位名",
    "jd_source": "用户粘贴或文件路径",
    "deadline": null
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

项目长期讲稿可以继续保存在现有 Vault，但必须在 `.career/manifests/` 建立同样的依赖记录。

## feedback.jsonl

每行一个 JSON 对象：

```json
{"id":"feedback-001","opportunity_id":"2026-company-role","stage":"interview","signal":"某项目回答讲不清","classification":"expression_gap","affected_claim_ids":[],"affected_artifacts":[".career/opportunities/2026-company-role/outputs/interview-plan.md"],"next_skill":"interview-package"}
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

# Learning Harness 状态约定

## 唯一事实链

```text
plan.json + events.jsonl → reducer → snapshot.json → projections
```

- `plan.json`：用户确认的学习目标、来源单元和完成政策。
- `events.jsonl`：唯一追加式进度事实源。
- `snapshot.json`：由 plan 与 events 生成的缓存；可以删除重建。
- `sessions/`：用户原始表达及检索／应用尝试正文。
- `projections/`：TaskNote 等派生视图的同步元数据。

不允许 `progress.json`、手工 current phase、手工 next action 或可变 workflow 状态文件。

## 目录

```text
.learning/
├── config.json
└── projects/<project_id>/
    ├── plan.json
    ├── events.jsonl
    ├── snapshot.json
    ├── sessions/
    └── projections/
        └── tasknote.json
```

所有路径相对 Git 根目录。`.learning` 不发布到 Quartz，也不属于知识正文。

## plan.json

`plan.json` 只保存相对稳定的人类决定：

- `focus_question`：学习要帮助回答的持续问题；
- `sources` 与 `units`：可恢复的来源边界；
- `completion_policy.unit`：每个来源单元默认只要求阅读覆盖；
- `completion_policy.claim`：实际出现的用户命题需要的沉淀决定；
- `completion_policy.project`：至少一个关键理解的来源核验，以及项目级检索和应用证据；
- `constraints`：用户明确不允许改变的范围。

计划调整通过 `record_progress.py plan` 执行，并追加 `plan_adjusted` 事件。不要通过直接编辑 snapshot 改计划。

## events.jsonl

每个事件包含：

```json
{
  "seq": 7,
  "id": "evt-00000007",
  "at": "...",
  "actor": "user",
  "type": "expression_captured",
  "project_id": "...",
  "subject": {"kind": "unit", "id": "lesson-04"},
  "payload": {},
  "evidence_refs": [
    {"type": "file", "path": ".learning/.../sessions/...md", "locator": null}
  ],
  "caused_by": []
}
```

事件必须顺序连续、只追加、有 actor、有明确 subject。语义结果必须携带可回查证据。

### 事件类别

| 作用域 | 事件 |
|---|---|
| 项目 | `project_initialized`、`project_status_changed`、`plan_adjusted` |
| 来源单元 | `coverage_recorded`、`expression_captured`、`expression_qualified`、`evidence_checked` |
| 用户命题 | `claim_registered`、`distillation_decided` |
| 使用 | `attempt_recorded` |
| 控制 | `blocker_added`、`blocker_resolved`、`workflow_updated` |

未进入语义动作时，单元的 expression/evidence 状态保持 `not_requested`。`expression_captured` 只证明用户留下了文字；是否构成认知起点由 `expression_qualified` 单独表达。`attempt_recorded` 保存每次成功、部分成功或失败，不覆盖历史。

## snapshot.json

Reducer 从事件计算：

- 当前来源单元；
- 每个单元的 coverage、expression status 和 evidence status；
- 用户命题及沉淀决定；
- 全部检索／应用尝试；
- 开放和已解决 blocker；
- workflow 恢复游标；
- 来源覆盖、关键核验、命题、检索和应用信号；
- 唯一下一步及原因。

`snapshot.derived_from_seq` 必须等于最后事件序号。`state_lint.py` 会重放全部事件并比较 snapshot；不一致即错误。

## Human First 证据

Human First 只在进入语义动作时创建，不是每个来源单元的必填进度。用户原始表达保存在 `sessions/*.md`：

```markdown
# Learning Session

- project: `...`
- subject: `lesson-04`
- recorded_at: `...`

## 用户原始表达

用户原文……
```

`expression_captured` 引用该文件。AI 分析、来源核对和润色不得覆盖这份原文。

## Workflow

长流程不再维护独立可变 JSON。每次恢复信息变化时追加 `workflow_updated`：

```json
{
  "mode": "concept-visualization",
  "unit_id": "lesson-04",
  "status": "in_progress",
  "step": "step-4-preview",
  "data": {"preview_status": "needs_regeneration"}
}
```

Reducer 只保留每个 workflow 的最新状态。临时 `/tmp` 路径和一次性写入授权不得持久化。

## 写入原子性

`append_events()` 使用项目锁：

1. 读取最后 seq；
2. 为整批事件分配连续 ID；
3. append + flush + fsync；
4. 重放并原子替换 snapshot。

事件写入成功但 snapshot 生成失败时，运行 `rebuild_snapshot.py` 即可恢复；不得回写或删除已提交事件。

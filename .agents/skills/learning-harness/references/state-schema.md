# Learning Harness 状态约定

## 唯一事实链

```text
plan.json + events.jsonl → Reducer → snapshot.json → projections
                              └────→ next_command
```

- `plan.json`：用户确认的学习目标、来源单元和完成政策。
- `events.jsonl`：唯一追加式学习事实源。
- `snapshot.json`：由 plan 与 events 生成的缓存，可以删除重建。
- `sessions/`：用户原始表达及检索／应用尝试正文。
- `projections/`：TaskNote 等派生视图的同步元数据。

不允许第二套进度文件、手工当前阶段、手工命令或独立可变 workflow 状态。

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
- `completion_policy.project`：关键理解核验、检索和应用证据；
- `constraints`：用户明确不允许改变的范围。

计划调整只能由外层根据用户决定执行，并追加 `plan_adjusted`。内层 action result 无权修改计划。

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

未进入语义动作时，单元的 expression/evidence 保持 `not_requested`。`expression_captured` 只证明用户留下文字；是否构成认知起点由 `expression_qualified` 单独记录。每次尝试都追加，不覆盖历史。

## snapshot.json

Reducer 从事件计算：

- 当前来源单元；
- 每个单元的 coverage、expression 和 evidence 状态；
- 用户命题及沉淀决定；
- 全部检索／应用尝试；
- 开放和已解决 blocker；
- workflow 恢复游标；
- 来源覆盖、关键核验、命题、检索和应用信号；
- 唯一 `next_command` 及原因。

`snapshot.derived_from_seq` 必须等于最后事件序号。`state_lint.py` 会重放全部事件并比较 snapshot；不一致即错误。

## next_command

Reducer 根据快照生成：

```json
{
  "id": "cmd-00000007",
  "based_on_seq": 7,
  "skill": "visual-pkm",
  "mode": "deep-reading",
  "action": "verify-expression",
  "subject": {"kind": "unit", "id": "lesson-04"},
  "instruction": "对照来源核验用户表达、条件、边界和可能误读并报告证据",
  "reason": "该语义动作尚未完成来源核验"
}
```

命令不是事实源，不单独持久化，也不能手工编辑。任何新事件都会令旧 command ID 和 state seq 失效。

## Human First 证据

用户原始表达保存在 `sessions/*.md`：

```markdown
# Learning Session

- project: `...`
- subject: `lesson-04`
- recorded_at: `...`

## 用户原始表达

用户原文……
```

`expression_captured` 引用该文件。AI 分析、来源核对和润色不得覆盖原文。

## Workflow

长流程通过 `workflow_updated` 事件保存最小恢复状态：

```json
{
  "mode": "concept-visualization",
  "unit_id": "lesson-04",
  "status": "in_progress",
  "step": "step-4-generate",
  "data": {
    "target_note_path": "Knowledge/Notes/示例.md",
    "visual_id": "example-visual",
    "framework": "过程式",
    "style_expression_ref": "evt-00000012"
  }
}
```

Reducer 只保留每个 workflow 的最新状态。临时路径和一次性授权不得持久化。活跃 workflow 由外层生成 `resume-workflow` 命令；内层只返回新的局部 checkpoint。

## Action Result 与并发边界

内层结果必须引用当前：

- `command_id`；
- `based_on_seq`；
- skill、mode、action；
- subject。

`apply_action_result.py` 在项目锁内重新读取当前状态。任一字段过期或不一致，整批结果拒绝，避免旧执行覆盖新状态。

## 写入原子性

`append_events()` 使用项目锁：

1. 读取最后 seq；
2. 为整批事件分配连续 ID；
3. append、flush、fsync；
4. 重放事件并原子替换 snapshot。

事件写入成功但 snapshot 生成失败时，运行 `rebuild_snapshot.py` 恢复；不得回写或删除已提交事件。

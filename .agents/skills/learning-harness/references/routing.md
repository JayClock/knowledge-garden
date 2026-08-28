# Learning Harness 路由与 Handoff

## 路由单位

外层不再路由“缺哪个 Gate”，而是路由一个明确学习动作：

| 当前事实 | Skill | Mode | Action |
|---|---|---|---|
| 来源尚未完成阅读覆盖 | `visual-pkm` | `deep-reading` | `record-coverage` |
| 用户准备核验意义但尚无自己的表达 | `visual-pkm` | `deep-reading` | `capture-expression` |
| 已有表达，待判断是否有效 | `visual-pkm` | `deep-reading` | `qualify-expression` |
| 已有有效表达，待来源核验 | `visual-pkm` | `deep-reading` | `verify-expression` |
| 用户命题尚未决定沉淀 | `visual-pkm` | `deep-reading` | `decide-distillation` |
| 来源已读但项目尚无关键核验 | `visual-pkm` | `deep-reading` | `select-and-verify-key-understanding` |
| 单一命题需要视觉正面 | `visual-pkm` | `concept-visualization` | workflow 当前 step |
| 用户已有粗图，需要检查空间语法 | `visual-pkm` | `spatial-mapping` | workflow 当前 step |
| 长期项目需要 IIB | `visual-pkm` | `idea-integration` | workflow 当前 step |
| 需要闭卷复述、比较或反例 | `visual-pkm` | `knowledge-exploration` | `run-retrieval` |
| 用户已有立场和第一版故事 | `visual-pkm` | `narrative-composition` | workflow 当前 step |
| 缺真实应用 | `learning-harness` | — | `record-application` |

一次只执行一个 action。Mode 仍是渐进披露边界，action 是恢复游标，不注册为新 Skill。

## Learning Handoff

`visual-pkm` 返回：

```yaml
learning_handoff:
  project_id: agent-harness-engineering
  unit_id: lesson-04
  skill: visual-pkm
  mode: deep-reading
  action: verify-expression
  observations:
    - type: evidence_checked
      subject:
        kind: unit
        id: lesson-04
      payload:
        result: supported_with_boundary
        open_questions: []
      evidence_refs:
        - type: file
          path: content/Knowledge/Sources/...
          locator: "## 与状态子系统的整合"
      caused_by:
        - evt-00000005
  artifact_paths: []
  open_questions: []
  workflow: null
  suggested_next: null
  needs_user_decision: false
```

完整 JSON 约束见 `schemas/handoff.schema.json`。

## Handoff 纪律

- `observations` 只报告本次动作真实观察到的状态变化。
- 来源核验必须引用真实来源；成功检索／应用必须引用用户实际回答或真实产物。
- `artifact_paths` 只能列出已经存在的文件。
- `suggested_next` 只供解释，`apply_handoff.py` 会忽略；Reducer 重新计算唯一下一步。
- `visual-pkm` 不直接写 `.learning`。
- 外层把 handoff 保存成 JSON，再由 `apply_handoff.py` 一次性校验和追加整批事件。
- 没有 observation 时不伪造状态写入；只返回自然语言结果。
- workflow 只保存恢复所需的 mode、step、status 和最小 data。

## 事件映射

| Observation | 何时产生 |
|---|---|
| `coverage_recorded` | 当前动作确认了真实阅读范围 |
| `expression_qualified` | 已判断用户原始表达是否足以成为核对起点 |
| `evidence_checked` | 已对照来源得出支持、边界、部分支持或冲突结果 |
| `claim_registered` | 用户明确提出候选命题 |
| `distillation_decided` | 用户决定 new／update／skip，且产物写入另有授权 |
| `attempt_recorded` | 真实完成一次检索、比较、反例、输出或应用 |
| `blocker_added/resolved` | 阻塞出现或已被验证解决 |

Human First 的原文应先通过 `record_progress.py expression` 保存；Handoff 通常只追加 qualification 或后续证据结果。

# Learning Harness 命令路由与 Action Result

## 权责边界

外层 `learning-harness` 是唯一决策者：它读取计划和事件状态，生成一个命令，校验内层结果，提交事件并重新计算。内层 `visual-pkm` 只执行命令，不选择全局后续动作，不修改计划，不直接写 `.learning`。

```text
Reducer → next_command → visual-pkm → action_result → validator → events → Reducer
```

## 全局优先级

Reducer 严格按以下顺序生成命令：

1. 已完成或归档：不生成命令；
2. 已暂停：`resume-project`；
3. 开放 blocker：`resolve-blocker`；
4. 未完成 workflow：`resume-workflow`；
5. 缚定当前单元的 coverage、表达核验和命题沉淀；
6. 其他未完成来源单元；
7. 项目级来源核验；
8. 项目级闭卷检索；
9. 项目级真实应用；
10. 用户确认完成。

只有外层可以改变这个优先级。

## 命令表

| 当前事实 | Skill | Mode | Action |
|---|---|---|---|
| 项目暂停 | `learning-harness` | — | `resume-project` |
| 存在开放阻塞 | `learning-harness` | — | `resolve-blocker` |
| 存在未完成 workflow | `visual-pkm` | workflow mode | `resume-workflow` |
| 项目没有来源单元 | `learning-harness` | — | `add-source-unit` |
| 来源尚未完成阅读覆盖 | `learning-harness` | — | `record-coverage` |
| 已保存表达但尚未判断有效性 | `visual-pkm` | `deep-reading` | `qualify-expression` |
| 已有有效表达但尚未完成来源核验 | `visual-pkm` | `deep-reading` | `verify-expression` |
| 用户命题尚未决定沉淀 | `learning-harness` | — | `record-distillation-decision` |
| 已读完但没有关键理解核验 | `learning-harness` | — | `capture-key-understanding` |
| 缺少闭卷检索证据 | `visual-pkm` | `knowledge-exploration` | `run-retrieval` |
| 缺少真实应用证据 | `learning-harness` | — | `record-application` |
| 完成政策已经满足 | `learning-harness` | — | `confirm-completion` |

一次只执行一个命令。视觉化、空间地图、IIB 和叙事作为 workflow 进入 `resume-workflow`；它们的局部 step 存在命令的 `workflow` 中，不改变全局路由权。

## Command

`next_command` 是 Reducer 从当前 event seq 确定性生成的执行指令：

```yaml
id: cmd-00000012
based_on_seq: 12
skill: visual-pkm
mode: deep-reading
action: verify-expression
subject:
  kind: unit
  id: lesson-04
instruction: 对照来源核验用户表达、条件、边界和可能误读并报告证据
reason: 该语义动作尚未完成来源核验
```

约束：

- `id` 由当前 event seq 生成；同一状态只有一个有效命令；
- `action` 是稳定机器标识，`instruction` 是本轮执行说明；
- `subject` 限定本轮可以处理的项目、单元、命题或 workflow；
- 内层不得修改命令或把命令扩展成多个全局动作；
- 完整 JSON 约束见 `schemas/command.schema.json`。

## Action Result

内层返回当前动作的事实报告：

```yaml
command_id: cmd-00000012
based_on_seq: 12
project_id: agent-harness-engineering
skill: visual-pkm
mode: deep-reading
action: verify-expression
subject:
  kind: unit
  id: lesson-04
status: passed
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
      - evt-00000011
gaps: []
artifact_paths: []
open_questions: []
workflow_checkpoint: null
needs_user_decision: false
```

`status` 只能描述本次动作：

- `passed`：当前动作完成；
- `partial`：产生了真实结果，但仍有 gap；
- `blocked`：无法继续，必须附 blocker observation 或 blocked workflow checkpoint；
- `needs_user_decision`：当前动作等待用户作意义或授权决定。

完整 JSON 约束见 `schemas/action-result.schema.json`。

## 提交纪律

`apply_action_result.py` 提交前必须确认：

- command ID 等于当前 `snapshot.next_command.id`；
- `based_on_seq` 等于当前 `derived_from_seq`；
- skill、mode、action 和 subject 与当前命令完全一致；
- observation 类型、作用域、证据和状态转换有效；
- artifact path 已真实存在；
- blocked 结果有可追踪阻塞；
- 整批事件可以原子追加。

任何一项不匹配都拒绝整个结果。没有 observation 或 workflow checkpoint 时不伪造状态变化。

## 内层允许报告什么

| Observation | 真实发生时报告 |
|---|---|
| `expression_qualified` | 已判断用户原始表达是否构成核验起点 |
| `evidence_checked` | 已对照来源得出支持、边界、部分支持或冲突 |
| `attempt_recorded` | 真实完成一次检索、比较、反例、输出或应用 |
| `blocker_added` | 当前执行发现了真实阻塞 |
| workflow checkpoint | 当前 workflow 的局部 step、status 和最小恢复数据变化 |

Coverage、用户原文、候选命题、沉淀决定、阻塞解除、计划与项目状态都由外层根据用户输入记录。内层只报告语义 Sensors、尝试结果、执行阻塞和局部 workflow checkpoint。

## 明确禁止

内层结果不得包含或隐含：

- 修改 `plan.json`；
- 修改项目状态；
- 指定下一个 mode 或 action；
- 宣布项目完成；
- 直接追加 `.learning/events.jsonl`；
- 用 artifact 数量、coverage 或非空文本推断掌握；
- 把临时路径或一次性授权持久化为学习事实。

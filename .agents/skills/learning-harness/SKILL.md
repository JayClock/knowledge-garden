---
name: learning-harness
description: "以事件溯源的外层控制循环编排跨会话学习。凡用户要开始／继续一项学习、记录读到哪里和自己的复述、恢复中断的课程或书籍、查看当前命令、记录闭卷检索或真实应用结果、同步 Obsidian 学习进度卡，或保存学习失败并调整计划时，都必须使用本 Skill。它维护 Git 根目录 `.learning/`，由 Reducer 根据事实生成唯一命令，再调用 `visual-pkm` 执行一个内层认知动作；不把阅读覆盖、笔记数量或 AI 总结误作掌握。"
compatibility: "需要 Python 3.11+、Git 仓库和可写 `.learning/`；TaskNotes 投影需要 Obsidian Vault。状态默认位于 `$LEARNING_STATE_DIR` 或 Git 根目录 `.learning/`。"
---

# Learning Harness

你是学习系统的外层大脑。你拥有计划、全局状态、命令路由和完成判断；`visual-pkm` 是内层执行器，只执行当前命令并报告结果。不要让内层选择全局后续动作或修改学习计划。

## 外层控制循环

```text
plan.json + events.jsonl
→ Reducer 重建 snapshot.json
→ Policy 生成唯一 next_command
→ 调用内层执行一个 command
→ 校验 action_result
→ 原子追加 observations
→ Reducer 重新生成状态与命令
```

外层独占：

- 学习目标、来源、完成政策和约束；
- 当前来源单元与全局动作优先级；
- blocker、workflow 恢复、计划调整和项目状态；
- 事件提交、状态重放和完成判断；
- 是否允许进入另一个 mode 或结束项目。

用户独占核心意义、稳定计划变更、知识产物写入和最终完成确认。规则明确的状态计算与命令生成可以自动执行。

## 状态模型

```text
plan.json         稳定的人类目标、来源、完成政策
+ events.jsonl    唯一追加式学习事实源
→ snapshot.json   可删除、可重建的当前状态与 next_command
→ TaskNote/Base   可删除、可重建的 Obsidian 投影
```

- 不直接编辑 `snapshot.json`。
- 不保留第二套进度文件、手工命令或独立可变 workflow 文件。
- 所有语义进度先记录成事件，再由 Reducer 计算当前单元、完成信号和命令。
- 设计或调试状态时完整读取 `references/state-schema.md`。

## 三个事实作用域

1. **来源单元**：coverage 始终可记录；只有进入语义核验时才附加用户表达与证据核对。
2. **用户命题**：用户提出的候选命题及 `new/update/skip` 沉淀决定。
3. **尝试**：闭卷复述、比较、反例、输出和真实应用的逐次结果。

不要把三个作用域压成单一百分比，也不要要求每个来源文件都提交表达、证据核对、检索或应用。

## 进入工作流

1. 运行 `git status --short`，保护用户已有修改。
2. 确认 Git 根并读取 `.learning/config.json`。
3. 用户说“继续／学到哪里”时运行：

```bash
python <skill>/scripts/learning_status.py --repo-root <git-root> --markdown
```

4. 状态不存在且用户明确要求开始跟踪时初始化：

```bash
python <skill>/scripts/init_state.py --root <git-root>
python <skill>/scripts/record_progress.py --repo-root <git-root> init-project ...
```

`init-project` 默认创建 `TaskNotes/Tasks/学习 - <title>.md` 和投影元数据。只有用户明确要求不生成 TaskNote 时才传 `--no-tasknote`。

5. 只执行 `snapshot.next_command` 指向的一个命令。完整优先级和动作表见 `references/routing.md`。

## Human First Expression

Human First 是语义动作的入口条件，不是每个来源单元的完成要求：

- Orient 时只记录一次用户的学习问题。
- 来源阅读只有准备核验意义时才要求表达：人类先读并留下复述、疑问或候选命题，AI 才读取来源进行核验。
- 没有进入语义核验的单元只记录 coverage；expression 和 evidence 保持 `not_requested`。
- 同一份 qualified expression 可以供来源核验、候选命题检查和沉淀决定复用。
- Retrieval 与 Application 保存新的真实使用结果，不叫 Human First Expression。
- 概念视觉需要新的文字视觉意图与成品反馈；地图、IIB 和叙事需要新的关系、摆放或立场。
- AI 的证据解释、反例和建议标记为 `AI 建议，待确认`。

## 自然语言记录

| 用户表达 | 外层记录 |
|---|---|
| “03 读完了” | `coverage_recorded` |
| “我的理解／疑问是……” | `expression_captured`，语义判断另记 `expression_qualified` |
| “请对照来源核验” | 当前命令必须是 `verify-expression`，结果记录 `evidence_checked` |
| “这个观点更新已有卡” | `claim_registered`；独立 Vault 授权后记录 `distillation_decided` |
| “闭卷讲失败，卡在……” | `attempt_recorded(result=failure)`，保留真实回答和 gap |
| “这个阻塞解决了” | `blocker_resolved` |

命令入口：

```bash
python <skill>/scripts/record_progress.py --help
```

一次操作可以原子追加多个同一动作产生的 observation，但不得跨越多个全局命令。

## 调用内层执行器

外层把 Reducer 生成的完整 command 交给 `visual-pkm`：

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

内层只返回当前命令的 `action_result`：

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
observations: []
gaps: []
artifact_paths: []
open_questions: []
workflow_checkpoint: null
needs_user_decision: false
```

外层保存结果为 JSON 后机械提交：

```bash
python <skill>/scripts/apply_action_result.py \
  --repo-root <git-root> \
  --file <action-result.json>
```

提交器必须确认 command ID、state seq、skill、mode、action 和 subject 全部匹配当前命令；过期或越权结果直接拒绝。内层不能提交计划变更、项目状态或全局路由决定。完整契约见 `references/routing.md`、`schemas/command.schema.json` 和 `schemas/action-result.schema.json`。

## Sensors 与行动

计算型检查：

```bash
python <skill>/scripts/state_lint.py --repo-root <git-root>
python <skill>/scripts/rebuild_snapshot.py --repo-root <git-root> --project-id <id>
```

语义判断包括：

- 用户表达是否真是用户的认知起点；
- 来源是否支持表达及其边界；
- 命题是否原子并值得沉淀；
- 检索或应用是否真的暴露理解；
- 失败属于理解、证据、组织、表达、应用还是 Harness。

内层只报告局部结果、证据和 gap。外层根据事件重新决定返回来源、重做比较、修复检索入口、执行真实应用或调整计划。完成政策见 `references/completion-gates.md`。

## TaskNotes 投影

TaskNote 不是事实源。新建项目默认创建投影；旧项目缺少投影或需要重建时运行：

```bash
python <skill>/scripts/sync_tasknote.py --repo-root <git-root> --project-id <id>
python <skill>/scripts/sync_tasknote.py --repo-root <git-root> --project-id <id> --apply
```

投影启用后，每次事件提交并通过 lint 后刷新同一 TaskNote。只有用户明确要求同步 `## 进度收件箱` 时，先 dry-run，再执行 `ingest_tasknote.py --apply`，最后重新同步。详细规则见 `references/tasknotes-projection.md`。

## 写入边界

- 新建计划默认创建并维护对应 TaskNote；这是唯一默认 Vault 写入例外。
- 状态记录或 TaskNote 投影不授权修改 Knowledge Note、Map、Output、Canvas 或 Excalidraw。
- 不在知识卡添加学习状态、阶段、Gate 或百分比。
- Knowledge Note 只保存已确认知识；原始学习过程保存在 `.learning/sessions/` 和事件中。
- 任何知识产物写入继续遵守对应格式 Skill 和独立授权。

## 用户可见输出

默认只报告：

```markdown
## 学习状态

- 学习对象：
- 当前单元：
- 学习信号：来源覆盖／关键核验／命题／检索／应用
- 当前阻塞：
- 当前命令：
- 为什么执行它：
```

只有用户明确设计或调试 Harness 时才展示事件、Schema、Reducer 和命令协议。

## 完成检查

- `events.jsonl` 能独立重建 `snapshot.json`；
- 事件序号连续，所有证据路径存在；
- coverage 没有自动变成理解或掌握；
- 用户命题与 AI 建议可区分；
- 每个成功检索／应用都有真实证据；
- blocker 可以显式关闭；
- 当前命令由 Reducer 生成，不由内层或人工手写；
- action result 与当前 command、state seq 严格匹配；
- TaskNote 投影与当前 event seq 一致；
- 用户确认后才把满足政策的项目标为 complete。

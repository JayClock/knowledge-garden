---
name: learning-harness
description: "以事件溯源的双层循环编排跨会话学习。凡用户要开始／继续一项学习、记录读到哪里和自己的复述、恢复中断的课程或书籍、查看下一步、记录闭卷检索或真实应用结果、同步 Obsidian 学习进度卡，或保存学习失败并调整计划时，都必须使用本 Skill。它维护 Git 根目录 `.learning/`，把用户自然语言记录成可重放事件，再以 `visual-pkm + mode + action` 执行一个内层认知动作；不把阅读覆盖、笔记数量或 AI 总结误作掌握。"
compatibility: "需要 Python 3.11+、Git 仓库和可写 `.learning/`；TaskNotes 投影需要 Obsidian Vault。状态默认位于 `$LEARNING_STATE_DIR` 或 Git 根目录 `.learning/`。"
---

# Learning Harness

你是学习系统的事件驱动编排器。你不直接包办所有阅读、绘图和写作；你负责读取事件状态、恢复唯一下一步、路由 `visual-pkm`、记录真实观察，并让检索与应用结果影响后续行动。

## 状态模型

```text
plan.json         稳定的人类目标、来源、完成政策
+ events.jsonl    唯一追加式学习事实源
→ snapshot.json   可删除、可重建的当前状态
→ TaskNote/Base   可删除、可重建的 Obsidian 投影
```

- 不直接编辑 `snapshot.json`。
- 不保留第二套 `progress.json`、可变 workflow 文件或手工 next action。
- 所有语义进度先记录成事件，再由 reducer 计算当前单元、完成情况和下一步。
- 完整结构见 `references/state-schema.md`；设计或调试状态时完整读取。

## 三个进度作用域

1. **来源单元**：coverage 始终可记录；只有进入语义核验时才附加用户表达与证据核对。
2. **用户命题**：用户提出的候选命题及 `new/update/skip` 沉淀决定。
3. **尝试**：闭卷复述、比较、反例、输出和真实应用的逐次结果。

不要把三个作用域压成单一百分比，也不要要求每个来源文件都提交表达、证据核对、检索或应用。

## 进入工作流

1. 运行 `git status --short`，保护用户已有修改。
2. 确认 Git 根；读取 `.learning/config.json`。
3. 用户说“继续／学到哪里”时运行：

```bash
python <skill>/scripts/learning_status.py --repo-root <git-root> --markdown
```

4. 状态不存在且用户明确要求开始跟踪时初始化全新状态：

```bash
python <skill>/scripts/init_state.py --root <git-root>
python <skill>/scripts/record_progress.py --repo-root <git-root> init-project ...
```

5. 只执行 `next_action` 指向的一个动作。完整路由见 `references/routing.md`。

## Human First Expression

Human First 是**语义动作的入口条件**，不是每个来源单元的完成要求：

- Orient 时，用户给出的学习问题只记录一次。
- 来源阅读只在准备执行 `verify-expression` 时要求表达：人类先读并留下复述、疑问或候选命题，AI 才读取来源进行意义核验。
- 没有进入语义核验的单元只记录 coverage；其 expression 和 evidence 保持 `not_requested`，不制造文本。
- 同一份 qualified expression 可供来源核验、候选命题检查和沉淀决定复用，不要求机械重述。
- Distillation 复用已有表达；Retrieval 保存新的真实回答；Application 保存真实任务结果；这两者是使用证据，不叫 Human First Expression。
- 概念视觉、地图、IIB 和叙事需要新的关键词、关系、摆放或立场，因为它们引入了新的意义决定。
- 项目默认只要求至少一个由用户选择的关键理解完成来源核验，不要求每个文件都表达。
- AI 的证据解释、反例和建议标记为 `AI 建议，待确认`。

## 自然语言记录协议

用户不需要说 Gate、phase 或 status。把日常表达映射为事件：

| 用户表达 | 记录 |
|---|---|
| “03 读完了” | `coverage_recorded` |
| “我的理解／疑问是……” | `expression_captured`，必要时同时 `expression_qualified` |
| “请对照来源核验” | 路由 `deep-reading / verify-expression`，再记录 `evidence_checked` |
| “这个观点更新已有卡” | `claim_registered` + 经独立 Vault 授权后的 `distillation_decided` |
| “闭卷讲失败，卡在……” | `attempt_recorded(result=failure)`，保存真实回答和 gap |
| “这个阻塞解决了” | `blocker_resolved` |

命令入口：

```bash
python <skill>/scripts/record_progress.py --help
```

一次记录可以追加多个事件，但必须原子应用。不要直接让用户提供内部字段。

## 内层调用

外层向 `visual-pkm` 传入：

```yaml
project_id: ...
unit_id: ...
mode: deep-reading
action: verify-expression
source_paths: []
expression_refs: []
workflow: null
```

`visual-pkm` 返回 `learning_handoff`，只包含可回查 observations，不直接写 `.learning`。外层先保存为 JSON，再机械执行：

```bash
python <skill>/scripts/apply_handoff.py \
  --repo-root <git-root> \
  --file <handoff.json>
```

`apply_handoff.py` 忽略 `suggested_next`；唯一下一步始终由 reducer 从事件重算。完整契约见 `references/routing.md` 和 `schemas/handoff.schema.json`。

## 状态校验与行动

计算型校验：

```bash
python <skill>/scripts/state_lint.py --repo-root <git-root>
python <skill>/scripts/rebuild_snapshot.py --repo-root <git-root> --project-id <id>
```

语义判断：

- 用户表达是否真是用户的认知起点；
- 来源是否支持表达及其边界；
- 命题是否原子并值得沉淀；
- 检索或应用是否真的暴露理解；
- 失败属于理解、证据、组织、表达、应用还是 Harness。

每次只执行一种行动：返回来源、重做比较、修复检索入口、执行真实应用或调整计划。完成政策见 `references/completion-gates.md`。

## TaskNotes 投影

TaskNote 不是事实源。首次同步需要明确 Vault 写入授权：

```bash
python <skill>/scripts/sync_tasknote.py --repo-root <git-root> --project-id <id>
python <skill>/scripts/sync_tasknote.py --repo-root <git-root> --project-id <id> --apply
```

启用投影后，每次成功写入事件并通过 lint，刷新同一 TaskNote。用户可以在 `## 进度收件箱` 写：

```markdown
- [ ] lesson-03 | coverage=read
- [ ] lesson-03 | expression=我自己的复述或疑问
```

只有用户明确要求同步收件箱时，先 dry-run、再 `ingest_tasknote.py --apply`，最后重新同步 TaskNote。详细规则见 `references/tasknotes-projection.md`。

## 写入边界

- 记录 `.learning` 状态不等于授权修改 Knowledge Note、Map、Output、Canvas 或 Excalidraw。
- 不在知识卡添加 `learning_status`、phase、Gate 或百分比。
- Knowledge Note 只保存已确认的知识；原始学习过程保存在 `.learning/sessions/` 和事件中。
- TaskNote 删除后可以重建，不得反向覆盖事件；进度收件箱只能追加新事件。
- 任何 Vault 写入继续遵守对应格式 Skill 和授权边界。

## 用户可见输出

默认只报告：

```markdown
## 学习状态

- 学习对象：
- 当前单元：
- 学习信号：来源覆盖／关键核验／命题／检索／应用
- 当前阻塞：
- 唯一下一步：
- 为什么是这一步：
```

只有用户明确设计或调试 Harness 时才展示事件、Schema 和 reducer。

## 完成检查

- `events.jsonl` 能独立重建 `snapshot.json`；
- 事件序号连续，所有证据路径存在；
- coverage 没有自动变成理解或掌握；
- 用户命题与 AI 建议可区分；
- 每个成功检索／应用都有真实证据；
- blocker 可以显式关闭；
- 下一步不是手写状态，而是可解释的派生结果；
- TaskNote 投影与当前 event seq 一致；
- 用户确认后才把满足政策的项目标为 complete。

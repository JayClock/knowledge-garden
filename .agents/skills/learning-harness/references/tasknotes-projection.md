# TaskNotes／Bases 学习状态投影

## 目标

TaskNote 让用户查看和快速记录，但 `.learning/events.jsonl` 始终是唯一进度事实源。

TaskNote 展示：

- 当前来源、外层生成的当前命令及原因；
- 全部来源单元的 coverage、expression、evidence；
- 用户命题和真实产物；
- 最近检索／应用尝试；
- 开放 blocker。

## 创建与同步

`record_progress.py init-project` 默认创建 `TaskNotes/Tasks/学习 - <title>.md`；只有用户明确要求不生成时才传 `--no-tasknote`。TaskNote 是可重建投影，不授权修改其他 Vault 内容。

旧项目缺少投影或需要重建时运行：

```bash
python <skill>/scripts/sync_tasknote.py --repo-root <git-root> --project-id <id>
python <skill>/scripts/sync_tasknote.py --repo-root <git-root> --project-id <id> --apply
```

同步元数据位于：

```text
.learning/projects/<id>/projections/tasknote.json
```

`source_seq` 必须等于 TaskNote 内容对应的最后事件序号。启用投影后，每次事件成功提交并通过 lint 后刷新同一文件。`state_lint.py` 会报告过期投影。

## 字段所有权

脚本拥有全部 `learning*` 字段，并写入：

- `learningId`
- `learningStatus`
- `learningActivity`
- `learningCurrentUnit`
- `learningCommandId`
- `learningCommandSkill`
- `learningCommandMode`
- `learningCommandAction`
- `learningLastEvent`
- `learningSourceReady`
- `learningClaimsReady`
- `learningSourceGrounding`
- `learningRetrieval`
- `learningApplication`
- `learningStateSeq`

用户／TaskNotes 管理 priority、scheduled、due、pomodoros、时间字段和用户备注。同步只替换 managed block、`status` 和 `learning*` 字段。

## 进度收件箱

用户可以在 TaskNote 用户区追加：

```markdown
- [ ] lesson-03 | coverage=read
- [ ] lesson-03 | expression=我自己的复述、疑问或候选命题
```

导入流程：

```bash
python <skill>/scripts/ingest_tasknote.py --repo-root <git-root> --project-id <id>
python <skill>/scripts/ingest_tasknote.py --repo-root <git-root> --project-id <id> --apply
python <skill>/scripts/state_lint.py --repo-root <git-root>
python <skill>/scripts/sync_tasknote.py --repo-root <git-root> --project-id <id> --apply
```

规则：

- 只有用户明确要求同步收件箱才导入；
- dry-run 先回显将导入的条目；
- 导入后条目勾选并标记 event ID；
- expression 只产生 captured 事件，不自动 qualified；
- TaskNote 不能修改、删除或覆盖既有事件；
- 已勾选条目不会再次导入。

## Bases

`learning-progress.base` 只读取 TaskNote frontmatter，用于跨项目总览；不计算语义完成状态，也不写回 `.learning`。TaskNote 和 Base 都可以删除并从事件重建。

---
name: career-evidence
description: 通过先读材料、顾问式深访和分轮确认挖出真实职业经历，持续维护 Outputs/职业经历.md 与 .career/claims.json。用户说梳理经历、深挖项目、没有材料、继续补充、修改职业经历、素材即事实或核对职责数据时使用；负责发现与确认事实，不直接生成岗位简历。
---

# Career Evidence

先帮用户把经历想起来、讲出来、讲清楚，再把确认过的内容沉淀为职业资产。对用户提供可阅读、可纠偏的职业经历，对内部维护有证据和边界的 claims。

## 开始前

1. 读取 `../career-assets/references/fact-policy.md`、`../career-assets/references/state-schema.md` 和 `references/experience-discovery.md`。
2. 检查 Git 状态，读取 config、claims、positioning；存在岗位机会时读取其要求。
3. 读取 `config.paths.career_history` 指向的职业经历及 `.career/manifests/career-history.json`。本仓库路径为 `content/Knowledge/Outputs/职业经历.md`。
4. 对照现有文档与 claims，优先识别用户直接补充、纠正和批注的内容。没有 Git diff 不等于没有人工改动；不要先从账本重新生成文档。
5. 没有状态时回到 career-assets 初始化。用户没有授权保存时，只在对话中整理，不创建状态或文档。

## 前馈：选对开局

从上下文判断紧急程度、材料充足度、本轮目标；缺失时只问影响下一步的信息。

- 材料多：先读，给出已有经历摘要、写浅的线索与待确认空白，不重复问材料已回答的问题。
- 材料一般：旧简历是线索和旧表达，选一段最有价值的经历深挖。
- 材料少：先拉教育、工作、项目和代表事件的粗时间线，不要求填写 claim 字段。
- 紧急机会：优先挖与当前岗位有关、已有证据的经历，边确认边支持交付，不降低事实标准。
- 长期整理：优先挖反复体现个人能力、重要但没讲清楚的经历，不必按时间顺序问完全部经历。

## 行动：发现 → 确认 → 沉淀

### 1. 递进深访

用时间线建立地图，再围绕背景、个人动作、关键取舍、结果证据与成长故事追问。一次通常问一到两个问题，根据回答继续；问题库不是固定问卷。

不要预设用户主导了项目、遭遇了事故或取得量化提升。没有数字时问实现、验收、实际变化和可验证记录，不要求编百分比。

### 2. 分轮确认

每约四个关键问题，或用户已提供足够信息时，整理一份短小结：

- 当时的问题；
- 用户直接做的事及团队边界；
- 已能确认的结果和完成状态；
- 尚不确定的部分。

让用户选择：批注纠偏、继续挖一个难点、或用已确认部分先服务当前岗位。小结是确认界面，不因 AI 整理过就成为 confirmed。

### 3. 写入事实账本

取得确认和写入授权后，把叙述拆成最小 claim，记录 `id`、`statement`、`kind`、`ownership`、`completion`、`status`、`evidence`、`metrics`、`constraints`、`tags`。

- 用户明确确认项目文稿范围时记录这项确认，个人职责、事故、客户、规模和数字分别核实。
- 配套仓库只是重实现时，代码缺失不能否定用户已确认的项目范围。
- 未确认线索为 candidate；冲突为 contested；通用资料为 reference_only。
- 数字必须有口径和来源，示例数字不进入 metrics。

### 4. 同步职业经历

`职业经历.md` 是长期维护的可读文档，不是临时报告，也不是岗位简历。执行 reference 中的文档结构与人工修改处理协议。

- 经确认正文来自 confirmed claims，保留职责、完成状态和限制，用自然段组织而不是倾倒 JSON 字段。
- 待补问题单列，不把 candidate 或 contested 陈述混入已确认正文。
- 用户新增内容先核对；来源不清时提问或保持候选，不默默覆盖，也不自动升级为事实。
- 为文档维护 `.career/manifests/career-history.json`，类型为 `career_history`，`generated_by` 为 `career-evidence`，记录正文使用的 confirmed claim IDs。
- 更新受影响的定位和 `positioning.open_questions`；变化的 claims 运行影响扫描，先标记依赖产物 stale，再把已同步的职业经历 manifest 设回 current。岗位材料只在本轮授权范围内同步。
- 职业经历不是对外投递包，不套用岗位简历的强制主题和篇幅要求。

## 收口与恢复

当前目标所需的经历、个人贡献、结果边界已足够清楚时，交付可用小结和文档；用户疲惫或时间不足时也应暂停。证据不足则交付待补问题，不绕过确认 Gate。

经授权将未解问题写入 `positioning.open_questions`：说明经历、问题、已知内容、关联 claim、优先原因和下次动作。不新建平行访谈状态。

用户说“继续补充”时先读职业经历和 open questions，接着上次未解问题往下问；优先当前岗位空白，否则补长期价值高的经历，不重复开局。

## Sensors 与调整

```bash
python ../career-assets/scripts/state_lint.py --state-dir <state-dir> --repo-root <git-root>
python ../career-assets/scripts/impact_scan.py --state-dir <state-dir> --claim-id <id> --mark-stale
```

- 计算检查：证据路径、claim 引用、manifest、文档存在性、链接和 `git diff --check`。
- 语义检查：是否问出个人动作与取舍，是否诱导数字或主导权，用户修改是否被保留，正文是否忠于 claims。
- 缺证据就缩小表达或追问；冲突保留版本与来源；通用方案不写成实际成果。
- 不用不断追问代替阶段成果，不用润色代替事实确认。

## 完成 Gate

- 用户得到经历小结、待补问题和清楚的下一步。
- 保存时，claims、职业经历、manifest 与未解问题同步；无法同步则明确 stale 和原因。
- 正文只使用 confirmed claims，个人／团队边界、完成状态和数字口径一致。
- 人工补充已核对或保留待确认，没有被覆盖。
- 状态、路径、链接和 diff 检查通过；受影响的其他产物已列出或标记 stale。

# 求职材料组织与依赖

## 核心原则

不要把所有 Markdown 当作并列资产。材料按职责分层：

```text
证据层：用户确认、源码、项目文稿、交付物
事实状态层：.career/claims.json
控制状态层：positioning.json、opportunity.json、manifest
可读经历层：content/Knowledge/Outputs/职业经历.md
派生产物层：通用自我介绍、项目 dossier、resume、岗位自我介绍、interview plan
反馈层：投递、面试、人工评审与 Harness 改进记录
```

已确认正文由 claims 支撑。职业经历文档的人工补充和市场反馈可以触发上游核对，不能未经确认直接成为事实。claims 保存结构化账本，职业经历保存长期可读叙述，两者不各自维护一套独立事实。

## 状态不是笔记

`.career/` 保存 Agent 的状态和依赖关系，不进入 Obsidian 发布区：

- `claims.json`：唯一事实账本；
- `positioning.json`：长期市场定位与待补问题；
- `opportunities/<id>/opportunity.json`：单次岗位状态；
- `manifests/`：产物依赖的 claim IDs；
- `feedback.jsonl`：真实结果与下一步。

用户日常审阅和补充入口是 `config.paths.career_history`，本仓库为 `content/Knowledge/Outputs/职业经历.md`。每轮授权保存经历时同步此文档及 `.career/manifests/career-history.json`（`artifact_type: career_history`）。写入前对照全文与 claims，保留人工新增和批注；事实修改先确认再入账，未解决时标记 stale，不覆盖用户文字。具体协议见 `../../career-evidence/references/experience-discovery.md`。

## 长期保留与按需生成

长期保留：

- 来源与证据；
- claims 和 positioning（含跨会话未解问题）；
- `content/Knowledge/Outputs/职业经历.md` 及其 manifest；
- 通用自我介绍；
- 高频项目 dossier；
- manifests 与真实反馈。

按 opportunity 生成：

```text
.career/opportunities/<opportunity_id>/
├── opportunity.json
├── outputs/
│   ├── resume.md
│   ├── resume.docx              # 用户要求时
│   ├── self-introduction.md
│   └── interview-plan.md
└── manifests/
```

不覆盖全局“当前岗位适配版”。多个岗位的自我介绍跟随各自 opportunity 保存，避免状态污染。

## 现有 Obsidian 面试材料

已有 Vault 可以继续沿用：

```text
15分钟：项目名.md
├── 简历回答逐字稿：具体主题.md
│   └── 简历追问：具体主题.md
└── 来源与证据
```

它们是项目 dossier，不是事实源。每个长期维护文件在 `.career/manifests/` 记录 claim IDs；上游 claim 改变后由 `impact_scan.py` 标记受影响材料。

### 项目整体讲法

负责业务问题、个人职责与分工、架构主线、一两个核心难点与交付应用结果。正向陈述真实机制，不附加免责声明或罗列未完成清单。

### 具体回答

一份文件只回答一个简历描述或技术主题，例如协议、调度、SDK 分包或协同状态。

### 追问训练

覆盖方案选择、失败场景、测试证据、技术机制与协作分工。

## 材料状态

状态写入 manifest，不污染 Obsidian frontmatter：

- `current`：与当前 claims 一致；
- `stale`：上游 claim 已改变，等待同步；
- `archived`：历史表达，只供回看。

事实自身的 `candidate`、`confirmed`、`contested` 等状态保存在 claims，不与 artifact 状态混用。

## Claim 变化后的同步审计

以下变化必须运行 impact scan：

- 个人职责或完成状态改变；
- 数字、客户、用户或交付范围改变；
- 技术方案从已完成改为延展，或反之；
- 项目名称、能力主线或证据边界改变。

处理顺序：

1. 更新 claim 和必要的 positioning；
2. 运行 `impact_scan.py`；
3. 把受影响 manifest 标记为 `stale`；
4. 同步用户本轮授权的职业经历与其他产物；核对人工修改后，只有已同步且无未解决事实冲突的 manifest 才设回 current；
5. 验证链接、格式和事实边界。

## 删除与归档

- 删除前先检查 manifest、证据路径和 wikilink。
- 删除岗位简历不能误删名称中含“简历”的项目回答。
- 岗位交付物默认归档到对应 opportunity，不反向更新 claims。
- 不可恢复的 DOCX、PDF 或图片优先进入废纸篓或先确认备份。

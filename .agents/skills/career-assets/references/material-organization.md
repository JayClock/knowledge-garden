# 求职材料组织与依赖

## 核心原则

不要把所有 Markdown 当作并列资产。材料按职责分层：

```text
证据层：用户确认、源码、项目文稿、交付物
事实状态层：.career/claims.json
控制状态层：positioning.json、opportunity.json、manifest
派生产物层：通用自我介绍、项目 dossier、resume、岗位自我介绍、interview plan
反馈层：投递、面试、人工评审与 Harness 改进记录
```

依赖只能向下。反馈可以触发上游复查，但不能直接成为事实。`.career/claims.json` 是唯一职业事实源，不长期维护另一份与它平行的 Markdown 主档。

## 状态不是笔记

`.career/` 保存 Agent 的状态和依赖关系，不进入 Obsidian 发布区：

- `claims.json`：唯一事实账本；
- `positioning.json`：长期市场定位与待补问题；
- `opportunities/<id>/opportunity.json`：单次岗位状态；
- `manifests/`：产物依赖的 claim IDs；
- `feedback.jsonl`：真实结果与下一步。

需要人工审阅事实时，可以按项目、公司或 claim kind 临时渲染报告；报告仍是派生物，不能反向成为事实源。

## 长期保留与按需生成

长期保留：

- 来源与证据；
- claims 和 positioning；
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

负责业务问题、个人职责、架构主线、一两个核心难点、结果和边界。不要塞入所有技术细节。

### 具体回答

一份文件只回答一个简历描述或技术主题，例如协议、调度、SDK 分包或协同状态。

### 追问训练

覆盖方案选择、失败场景、测试证据、缺失数据、个人／团队边界和架构延展。

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
4. 只同步用户本轮授权的产物；
5. 验证链接、格式和事实边界。

## 删除与归档

- 删除前先检查 manifest、证据路径和 wikilink。
- 删除岗位简历不能误删名称中含“简历”的项目回答。
- 岗位交付物默认归档到对应 opportunity，不反向更新 claims。
- 不可恢复的 DOCX、PDF 或图片优先进入废纸篓或先确认备份。

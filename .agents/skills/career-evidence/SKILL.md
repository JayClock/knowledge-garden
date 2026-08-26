---
name: career-evidence
description: 将职业来源材料、源码、旧简历和用户访谈转成 `.career/claims.json` 中可追踪的 claim，核对个人／团队边界、完成状态、数字与冲突。用户说梳理经历、补充事实、素材即事实、核对项目范围、更新职业事实、修正职责或数据时使用；不要用它直接生成岗位简历。
---

# Career Evidence

你负责 Career Harness 的 capture / verify 阶段。目标不是写得好看，而是把最小可复述事实、证据和限制保存进唯一事实源 `.career/claims.json`。

## 开始前

1. 读取 `../career-assets/references/fact-policy.md`。
2. 读取 `../career-assets/references/state-schema.md`。
3. 定位 Git 根、`.career/config.json`、`claims.json`、`positioning.json` 和受影响 manifests。
4. 检查 Git 状态，保留用户已有修改。
5. 没有状态目录时，回到 `career-assets` 初始化；不要在本 Skill 中临时发明另一套状态。

## 内层操控循环

### 前馈

先确定本轮来源范围和用户授权：

- 用户明确确认的事实；
- 实际源码、交付物和测试；
- 能对应本人工作的项目文稿；
- 旧简历和讲稿线索；
- 只用于技术框架的参考资料。

用户说“整个目录／素材即事实”时，把“该材料代表实际项目范围”记录为 user confirmation；仍分别判断个人职责、完成状态、生产事故、客户、规模和数字。原文中的简历示例数字不会自动成为 metric。

### 行动

1. 完整读取目标普通文本；大型源码先读项目结构和与 claim 相关的实现。
2. 把材料拆成最小 claim，不把项目简介、个人动作、团队背景、结果和边界塞进一条。
3. 为每条 claim 填写：`id`、`statement`、`kind`、`ownership`、`completion`、`status`、`evidence`、`metrics`、`constraints`、`tags`。
4. 旧表达只能产生 candidate；用户确认或高等级证据满足后才升级 confirmed。
5. 更新 claims 后同步 `positioning.json` 中受影响的定位和 open questions；不要维护平行的 Markdown 事实主档。
6. claim 变化后运行 impact scan，并把受影响 artifact 标记 stale；只同步用户本轮授权的下游文件。

### Sensors

计算型检查：

```bash
python ../career-assets/scripts/state_lint.py --state-dir <state-dir> --repo-root <git-root>
python ../career-assets/scripts/impact_scan.py --state-dir <state-dir> --claim-id <id>
```

同时检查 Markdown 链接、结构化文件和 `git diff --check`。

推断型检查：

- statement 是否只表达一个事实；
- ownership 是否把团队成果升级成个人成果；
- completion 是否把设计或框架默认能力写成已上线；
- metrics 是否有统计口径；
- 失败是否真实发生在对应项目，而不是示例或重实现；
- constraints 是否足以阻止下游夸大。

### 调整

- 缺证据：保持 candidate，提出最小补充问题。
- 前后冲突：标记 contested，保留两个版本和来源，等待用户判断。
- 只有通用方案：标记 reference_only。
- 用户确认事实边界：更新 claim，但不自动扩大关联 claim。
- 下游暴露新线索：回到本循环确认，不直接改写事实。

## 访谈节奏

材料不足时先建立粗时间线，再围绕背景、目标、动作、结果、指标、个人贡献、失败和反思追问。每约四个关键问题：

1. 给用户一段轻量纪要；
2. 展示新增或变化的事实；
3. 说明仍缺什么；
4. 经授权后写入 claims，并更新受影响的定位或 manifest。

不要无限追问；能够支持当前目标时先交付可用事实集，剩余项留作 candidate。

## 输出约定

对用户只说明：本轮确认了什么、哪些仍待确认、修改了哪些文件、哪些下游已过期。内部 claim ID 只在用户设计或调试 Harness 时展示。

## 完成 Gate

- confirmed claim 均有证据；
- 个人／协作／团队边界和完成状态清楚；
- 未确认数字未进入 metrics；
- claims、positioning 和证据之间没有事实冲突；
- state lint、Schema、链接和 diff 检查通过；
- 受影响 artifact 已列出或标记 stale。

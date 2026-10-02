---
name: resume-package
description: 为一个明确 opportunity 生成岗位简历、岗位自我介绍和可选 DOCX 交付包，并用 manifest 保证两者消费同一组 confirmed claims。用户给出公司／岗位／JD 后要求出简历、改岗位版、自我介绍、Word 或 DOCX 时使用；不负责发现新事实，也不覆盖全局通用自我介绍。
---

# Resume Package

你负责 Career Harness 的 package 阶段。产物属于一次明确岗位机会，不是新的事实源。

## 前置条件

1. 读取 `../career-assets/references/fact-policy.md` 和 `../career-assets/references/state-schema.md`。
2. 读取 `.career/claims.json`、`positioning.json`、`config.json.resume_policy` 和目标 opportunity。
3. opportunity 至少处于 `mapped`，包含公司、岗位、核心要求和 selected claim IDs。
4. 所有 selected claims 必须 confirmed；否则停止并路由 `career-evidence` 或 `career-positioning`。
5. 读取配置中的通用 `自我介绍.md` 只为理解基础定位，不覆盖它。

## 内层操控循环

### 前馈

冻结本次岗位包的：

- 核心 JD 要求；
- selected claim IDs；
- 项目排序；
- 必须保留的 ownership、completion 和 constraints；
- 输出格式和截止时间。

强化建议必须单列，不能混入保真正文。

### 行动

1. 生成书面简历前读取 `references/source-grounded-project-writing.md`，检索项目原始文稿、实战复盘、“中级／高级简历描述”和“项目重难点”；从中提取业务问题、系统边界、架构决策、复杂机制、故障处理和验证线索，再逐条映射到 selected confirmed claims。素材中的简历示例只是信息入口，不作为段落格式。
2. 用同一 claim 集生成书面简历和岗位自我介绍，并无条件包含 `config.resume_policy.required_claim_ids` 与 content markers 校验。不得为压缩篇幅删除基线主题，应先压缩重复或弱相关证据。
3. 项目经历由素材中的强证据自然组织，不强制统一的“技术栈／项目简介／工作内容与成果”结构、分类标签、条目数或先后顺序；技术名词必须进入具体动作、机制或验证语境。
4. 岗位自我介绍保存到：

```text
.career/opportunities/<opportunity_id>/outputs/self-introduction.md
```

5. 默认自我介绍 90～120 秒，读取 `../interview-package/references/interview-oralization.md`；用一条能力主线串起岗位简历中的全部主项目，将存在 confirmed 实际接入点的支撑项目嵌入对应主项目，并在完整口述版本前写入独立的 `提取词`。
6. 简历 Markdown 保存到同一 opportunity 的 `outputs/resume.md`；只有用户明确要求时才生成 DOCX。
7. DOCX 交付读取 `references/resume-docx-delivery.md`，模板原件位于 `assets/templates/钟杰-岗位定制简历模板.docx`。
8. 为每个产物写 manifest，记录 `opportunity_id`、`generated_by: resume-package`、`claim_ids` 和 `status: current`。
9. 更新 opportunity 的 artifacts；全部 Gate 通过后将 stage 设为 `packaged`。

### Sensors

计算型检查：

- state lint；
- 简历和自我介绍 manifest 的 claim ID 集是否一致；
- `resume_policy.required_artifact_types` 的 manifest 是否都包含 required claims，可读文本是否至少命中一个 `content_markers_any`；
- 是否引用 non-confirmed claim；
- 自我介绍非空白字符和预计朗读时长；
- DOCX 占位符、模板基线错误和视觉布局；
- `git diff --check` 与目标文件存在性。

口语时长：

```bash
python ../interview-package/scripts/oral_time.py <self-introduction.md> --section "90～120 秒版本" --min-seconds 90 --max-seconds 120
```

推断型检查：

- 每个主项目的内容顺序是否来自该项目最强素材，而不是被统一小节、标签和条目数强行塑形；
- 项目选择是否回应 JD 的核心工作；
- 简历和自我介绍是否表达同一事实但适配不同媒介；
- 是否扩大个人职责、完成状态、客户、数字或业务结果；
- 自我介绍是否自然可口述，而不是朗读简历。

### 调整

- 事实冲突 → `career-evidence`。
- JD 覆盖不足 → `career-positioning`。
- 书面内容太长 → 压缩次要项目，不删除硬边界。
- 口语超时 → 减少项目和技术细节，不改变事实。
- DOCX 布局失败 → 调整文本密度或 OfficeCLI 操作，不修改模板原件。

## 岗位包规则

- 不再维护无岗位上下文的“当前简历”。
- 不再覆盖全局 `自我介绍.md` 的“当前岗位适配版”。
- 每个岗位自我介绍跟随 opportunity 保存，多个机会互不污染。
- DOCX、PDF 和岗位文案不能反向更新 claims。
- 用户没有要求落盘时，先在对话中展示保真内容和强化建议。

## 完成 Gate

- opportunity 已映射且只使用 confirmed claims；
- 主项目符合 `references/source-grounded-project-writing.md`：模板只提供视觉样式，项目内容由素材和 selected confirmed claims 决定；
- 简历与自我介绍的事实、职责、完成状态和限制一致，并通过全局 `resume_policy` Gate；
- 自我介绍用能力主线串起岗位简历中的全部主项目，包含独立提取词，并通过正文时长和口语化检查；
- DOCX（如有）通过 OfficeCLI 与视觉验证；
- manifests、opportunity artifacts 和 stage 已更新；
- state lint 通过。

---
name: resume-package
description: 面向明确岗位生成求职文案。用户只提供公司／岗位／JD、招聘链接或截图时默认仅生成招呼语；明确要求简历、自我介绍、Word／DOCX 或简历包时才生成对应资料。经授权保存时用 manifest 记录 confirmed claims；不负责发现新事实，也不覆盖全局通用自我介绍。
---

# Resume Package

你负责 Career Harness 的 package 阶段。产物属于一次明确岗位机会，不是新的事实源。

## 先确定输出范围

- **默认招呼语模式**：只收到岗位信息，或泛指“按这个岗位出一版”，仅返回 1 条可直接发送的招呼语。不要附送分析报告、简历、自我介绍、DOCX、面试材料或强化建议。
- **明确资料模式**：要求简历就只生成简历；要求自我介绍就只生成自我介绍；要求 Word／DOCX 才做对应交付。明确要求“简历包”时才同时交付简历与岗位自我介绍，DOCX 仍按明确要求生成。
- 用户明确要求岗位分析或面试时分别交给 `career-positioning`、`interview-package`，不扩展为其它资料。
- 请求生成不等于授权落盘或发送；没有保存要求时只在对话中交付。以下文件、manifest 和阶段更新仅在获得保存授权后执行。

## 共同前置条件

1. 读取 `../career-assets/references/fact-policy.md` 和 `../career-assets/references/state-schema.md`。
2. 读取 `.career/claims.json`、`positioning.json`、`config.json`；有现成目标 opportunity 时读取它，但不覆盖其它机会。
3. 对外表达只使用 confirmed claims，保留相应 ownership、completion 和 constraints；事实缺口交给 `career-evidence`。

## 默认招呼语模式

### 前馈

- 读取 `references/job-greeting.md`。
- 从当前岗位信息提取最相关的要求，内部匹配 1～2 个有 confirmed claims 支撑的优势，不要求先输出完整 JD 分析或生成简历。
- 不要求已存在 `mapped` opportunity，也不以简历定稿为前提；信息不足时只追问会影响措辞的关键问题。状态不存在时不要为一条草稿自动初始化或确认事实，先按 `career-evidence` 核对必要经历。

### 行动

1. 按“核心身份／年限／学历择优＋岗位匹配优势＋简短沟通意向”写 1 条招呼语，通常 50～150 字，前约 17 字优先放最强信息。
2. 直接展示可复制发送的正文，不默认附带模板说明、匹配报告、多版本或其它资料。
3. 仅经授权保存时：新建仅招呼语机会使用 `purpose: outreach`，记录核心要求与实际使用的 confirmed claims；写入 `outputs/greeting.md` 和 `manifests/greeting.json`，`artifact_type: greeting`、`generated_by: resume-package`、`status: current`，claim IDs 为正文实际使用的子集。
4. 新建 outreach 机会保存并通过检查后可设为 `packaged`，下一步交回 `career-assets` 等待用户要求，不自动生成简历或进入面试准备。为已有机会补招呼语时保留其 purpose、阶段、selected claims 和其它产物，不降级或覆盖。
5. 招呼语不要求携带完整 `resume_policy` 基线，不要求 claim 集与简历、自我介绍相同；不把生成或保存招呼语记为已发送或已投递。

### Sensors 与调整

- 核对前约 17 字是否包含最重要的身份或匹配证据，而非空泛寒暄；17 字是写作优先区，不是各平台固定显示规则。
- 检查总字数、岗位关键词是否有实际证据、是否有占位符或空泛自评；英文技术词按自然表达使用，不为凑字数扩写。
- 年限、学历、成果数字、熟练程度、公司业务与到岗时间均须有来源；缺失项可省略，不从 JD、文章模板或相似经验推定。
- 表达正向自然，不用“虽是跨行”“求给机会”等自我削弱开场，不保证高回复率。
- 过长时压缩为最相关的 1～2 项证据；缺口不强行匹配，只有确实阻塞表达时才追问。
- 保存后运行 state lint 与 `git diff --check`，确认只生成已授权的文件；不运行与本次招呼语无关的自我介绍时长或 DOCX 检查。

## 明确资料模式

### 额外前置条件

1. 目标 opportunity 至少处于 `mapped`，包含公司、岗位、核心要求和 selected claim IDs；未建档且未授权保存时，先在对话中完成同等映射，不强制创建状态。
2. 所有 selected claims 必须 confirmed；否则停止并路由 `career-evidence` 或 `career-positioning`。
3. 正式简历机会使用 `purpose: application`；从已保存的 outreach 扩展时复用原机会，补齐 `resume_policy` 基线后再保存变更。
4. 需要生成自我介绍时，读取配置中的通用 `自我介绍.md` 只为理解基础定位，不覆盖它。

### 前馈

冻结本次岗位包的：

- 用户明确要求的产物，不补生成其它资料；
- 核心 JD 要求；
- selected claim IDs；
- 项目排序；
- 必须保留的 ownership、completion 和 constraints；
- 输出格式和截止时间。

用户要求强化建议时单列，不能混入保真正文。

### 行动

1. 生成书面简历前读取 `references/source-grounded-project-writing.md`，检索项目原始文稿、实战复盘、“中级／高级简历描述”和“项目重难点”；从中提取业务问题、系统边界、架构决策、复杂机制、故障处理和验证线索，再逐条映射到 selected confirmed claims。素材中的简历示例只是信息入口，不作为段落格式。
2. 对本次请求的简历／自我介绍，执行 `config.resume_policy.required_claim_ids` 与 content markers 校验。不得为压缩篇幅删除基线主题，应先压缩重复或弱相关证据。同时生成两者时用同一 claim 集；只要求其中之一时不补生成另一份。
3. 项目经历由素材中的强证据自然组织，不强制统一的“技术栈／项目简介／工作内容与成果”结构、分类标签、条目数或先后顺序；技术名词必须进入具体动作、机制或验证语境。
4. 默认自我介绍 90～120 秒，读取 `../interview-package/references/interview-oralization.md`；用一条能力主线串起岗位简历中的全部主项目，将存在 confirmed 实际接入点的支撑项目嵌入对应主项目，并在完整口述版本前写入独立的 `提取词`。仅要求自我介绍且没有岗位简历时，使用同等岗位映射中选定的主项目，不额外生成简历。
5. 经授权保存时，简历 Markdown 写入 `.career/opportunities/<opportunity_id>/outputs/resume.md`，岗位自我介绍写入同目录的 `self-introduction.md`；只写本次要求的产物。
6. 只有用户明确要求时才生成 DOCX；读取 `references/resume-docx-delivery.md`，模板原件位于 `assets/templates/钟杰-岗位定制简历模板.docx`。
7. 为每个已保存产物写 manifest，记录 `opportunity_id`、`generated_by: resume-package`、`claim_ids` 和 `status: current`。
8. 更新 opportunity 的 artifacts；本次请求的产物全部通过 Gate 后可将 stage 设为 `packaged`，但不自动进入面试生成，也不降低已经 submitted／interviewed／closed 的阶段。

### Sensors

仅检查本次实际生成的资料；不因检查缺少未请求的文件而补生成它们。

计算型检查：

- 保存时运行 state lint；
- 同时生成简历和自我介绍时，两者 manifest 的 claim ID 集是否一致；
- 对属于 `resume_policy.required_artifact_types` 的产物，manifest 是否都包含 required claims；受内容检查的可读文本是否至少命中一个 `content_markers_any`；该配置约束已有产物，不要求创建其中列出的所有类型；
- 是否引用 non-confirmed claim；
- 自我介绍非空白字符和预计朗读时长（如有）；
- DOCX 占位符、模板基线错误和视觉布局（如有）；
- `git diff --check` 与目标文件存在性（保存时）。

口语时长（仅生成自我介绍时）：

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
- 书面内容太长 → 压缩次要细节，确保核心产物与职责真实准确。
- 正文严禁输出任何防御性免责声明、反夸大宣称或负向未完成清单。
- 口语超时 → 减少项目和技术细节，不改变事实。
- DOCX 布局失败 → 调整文本密度或 OfficeCLI 操作，不修改模板原件。

## 岗位包规则

- 不再维护无岗位上下文的“当前简历”。
- 不再覆盖全局 `自我介绍.md` 的“当前岗位适配版”。
- 经授权保存的招呼语和岗位自我介绍跟随 opportunity，多个机会互不污染。
- DOCX、PDF、招呼语和岗位文案不能反向更新 claims。
- 用户没有要求落盘时，只在对话中展示所请求的内容；强化建议也仅按需提供。

## 完成 Gate

- 默认入口只交付招呼语；其它资料均有明确请求，未授权不落盘、不发送。
- 所有对外内容只使用 confirmed claims，职责、完成状态和限制一致。
- 招呼语通过 `references/job-greeting.md` 的首句、相关性、长度和事实检查，不套用完整简历基线。
- 简历主项目（如有）符合 `references/source-grounded-project-writing.md`，已请求的简历／自我介绍通过全局 `resume_policy` Gate。
- 自我介绍（如有）用能力主线串起所选全部主项目，包含独立提取词，并通过正文时长和口语化检查。
- DOCX（如有）通过 OfficeCLI 与视觉验证。
- 经授权保存时 manifests、opportunity artifacts 和 stage 已按本次范围更新，state lint 通过；仅招呼语不自动进入面试准备。

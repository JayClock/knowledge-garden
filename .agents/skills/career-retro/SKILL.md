---
name: career-retro
description: 将真实投递、招聘沟通、面试和人工评审反馈分类回流到 Career Harness，判断问题属于事实、证据、定位、项目选择、表达、交付还是 Harness。用户说复盘投递、面试没过、回答卡住、哪版有效、招聘方反馈或下一轮怎么改时使用；反馈不能直接改写职业事实。
---

# Career Retro

你负责 Career Harness 的 retro 阶段。目标不是情绪化评价某次结果，而是把真实观察转成下一轮可执行调整。

## 开始前

1. 读取 `../career-assets/references/fact-policy.md` 和 `../career-assets/references/state-schema.md`。
2. 读取目标 opportunity、其 artifacts / manifests 和 selected claim IDs。
3. 取得真实结果：投递渠道、使用版本、阶段、面试问题、用户主观感受和招聘方原话；缺失时明确标记 unknown。
4. 读取 `.career/feedback.jsonl`；未经授权不写入。
5. 不把一次失败自动解释为事实错误或能力不足。

## 内层操控循环

### 前馈

反馈分类只能使用：

- `fact_gap`
- `evidence_gap`
- `positioning_gap`
- `selection_gap`
- `expression_gap`
- `delivery_error`
- `market_mismatch`
- `harness_gap`

区分观察、解释和行动：招聘方原话是观察；原因判断是解释；下一步才是行动。

### 行动

1. 记录机会、阶段、实际使用 artifact 和反馈原文。
2. 判断反馈影响哪些 claim、requirement 或 artifact；不相关则保持空数组。
3. 选择一个主分类，必要时增加次分类说明。
4. 写入 `feedback.jsonl`，并把 feedback ID 关联到 opportunity。
5. 给出下一步路由：
   - 事实或证据 → `career-evidence`
   - 定位或项目选择 → `career-positioning`
   - 简历／自我介绍 → `resume-package`
   - 项目回答／追问 → `interview-package`
   - 重复性流程缺陷 → 修改相应 Skill 的 Guides、Sensors 或脚本
6. 更新 opportunity stage：面试后为 `interviewed`，流程结束为 `closed`。

### Sensors

计算型检查：

- feedback 每行是有效 JSON；
- opportunity_id 和 artifact manifest 存在；
- affected claim IDs 存在；
- next_skill 与 classification 匹配；
- state lint 通过。

推断型检查：

- 是否把相关性误当因果；
- 是否只因一次拒绝就改长期定位；
- 是否把“讲不清”误判为“没做过”；
- 是否把职位不匹配误判为简历质量；
- 是否有跨多个 opportunity 重复出现的模式。

### 调整

- 信息不足：记录 unknown 和下一次要采集的问题，不强行归因。
- 单次弱信号：优先调整表达或收集更多样本。
- 多次一致信号：升级为定位、选择或 Harness 改进候选。
- 反馈暴露事实冲突：创建 contested candidate，交给 `career-evidence`，不直接修改 confirmed claim。

## Harness 自我改进

只有满足以下条件才建议改 Skill：

- 不同机会重复出现同类失败；
- 失败来自流程缺少 Guide 或 Sensor，而不是某个岗位特例；
- 修改可以用测试 prompt 和断言验证；
- 修改不会放松真实性边界。

记录改进假设、受影响 Skill、预期行为和测试案例，再进入 skill-creator 的评估循环。

## 用户输出

用人话说明：

- 这次发生了什么；
- 哪些只是猜测；
- 最可能的问题层级；
- 下一步只改哪里；
- 哪些事实保持不变。

## 完成 Gate

- 反馈绑定真实 opportunity 和 artifact；
- 观察、解释与行动分开；
- 没有根据市场反馈直接篡改事实；
- next_skill 和下一步明确；
- 重复性 Harness 问题已形成可测试假设；
- state lint 通过。

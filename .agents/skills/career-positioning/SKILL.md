---
name: career-positioning
description: 基于 confirmed career claims 建立长期职业定位，或把具体 JD 拆成要求并映射到证据、项目与 gap。用户询问适合什么岗位、职业主线、岗位匹配、JD 分析、项目选择、简历该突出什么、为什么投递效果不好时使用；它只输出定位和 opportunity brief，不直接写简历或面试稿。
---

# Career Positioning

你负责 Career Harness 的 position 阶段：把事实转成明确的市场定位和岗位选择依据，但不把岗位关键词反向写成职业事实。

## 开始前

1. 读取 `../career-assets/references/state-schema.md` 和 `../career-assets/references/fact-policy.md`。
2. 读取 `.career/claims.json` 和 `positioning.json`；只有账本中的 claims 可以支撑定位判断。
3. 具体岗位必须取得公司、岗位、JD 或明确能力要求；没有这些信息时只讨论长期定位，不制造岗位契合度。
4. 检查 Git 状态，未经授权不创建 opportunity 或修改定位。

## 内层操控循环

### 前馈

固定三条边界：

- 岗位要求是选择条件，不是事实来源。
- 只有 confirmed claim 能作为“已经具备”的证据。
- 没有证据的要求记录为 gap，不用泛化能力或相似术语强行匹配。

### 行动

#### 长期定位

- 从时间线、重复出现的个人动作、可迁移机制和职业偏好中提炼市场名称、能力轴与目标岗位族。
- 市场名称要便于招聘方识别；能力轴可以表达更深层的长期方向。
- 将支持定位的 claim IDs 写入 `positioning.json.base_claim_ids`。
- 用户未确认前保持 `candidate`。

#### 具体机会

1. 建立稳定 `opportunity_id`，目录名使用可识别的公司和岗位，不使用“当前”。
2. 将 JD 收敛为 3～5 个核心要求，区分 `must`、`important`、`optional`。
3. 为每个要求关联 confirmed claim IDs，并记录直接证据、可迁移证据或 gap。
4. 选择能够形成完整证明链的项目，不以技术关键词数量决定优先级。
5. 写入 `opportunity.json`；完成映射后将 stage 从 `intake` 更新为 `mapped`。

### Sensors

计算型检查：

- requirement 和 selected claim ID 是否存在；
- 对外阶段是否只使用 confirmed claim；
- opportunity ID 是否与目录一致；
- 同一机会是否已有状态，避免重复创建。

运行：

```bash
python ../career-assets/scripts/state_lint.py --state-dir <state-dir> --repo-root <git-root>
```

推断型检查：

- claim 是否真正证明要求，而不是只共享名词；
- 项目组合是否覆盖岗位最重要的工作；
- 定位是否与五年经历、职责层级和个人边界一致；
- gap 是否值得补证据、调整表达，还是岗位本身不匹配；
- 选出的项目是否能在面试中继续展开。

### 调整

- 事实缺口 → 路由 `career-evidence`。
- 有事实但项目选择不佳 → 重排 selected claims。
- 关键 must requirement 无证据 → 保留 gap，并向用户说明风险。
- 多次机会反复暴露同一 gap → 提议更新长期定位或制定能力补强计划，不虚构匹配。

## 输出

用户可见输出保持简洁：

- 岗位最重要的 3～5 项要求；
- 已有的强证据；
- 最合适的项目组合；
- 明确 gap；
- 推荐进入 resume-package、interview-package 或暂缓投递。

不要在本阶段写完整简历。

## 完成 Gate

- positioning 有 confirmed claim 支撑，或明确保持 candidate；
- opportunity 的核心要求已映射；
- selected claims 均 confirmed；
- gap 没有被营销措辞掩盖；
- state lint 通过；
- 下一阶段和项目优先级明确。

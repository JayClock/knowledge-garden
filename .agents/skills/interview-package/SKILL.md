---
name: interview-package
description: 从 confirmed claims 和岗位要求生成项目整体讲法、具体回答、追问训练、模拟面试计划与口语化版本。用户说准备面试、15 分钟项目介绍、逐字稿、追问地图、自我介绍口语化、回答不自然或要模拟追问时使用；它只调整选择与表达，不新增事实。
---

# Interview Package

你负责 Career Harness 的 practice 阶段。面试材料必须能够从 claim 追溯到证据，并能在被打断和连续追问时继续回答。

## 前置条件

1. 读取 `../career-assets/references/fact-policy.md` 和 `../career-assets/references/state-schema.md`。
2. 读取 claims；涉及岗位时读取目标 opportunity 的 requirements 与 selected claim IDs。
3. 读取 `references/interview-oralization.md`。
4. 发现新事实线索时停止扩写，交给 `career-evidence` 确认。

## 内层操控循环

### 前馈

固定本轮：

- 面试场景和时长；
- 目标岗位或通用目的；
- 选用项目与 claim IDs；
- 个人／团队边界；
- 已完成、延展和不能声称的内容；
- 面试官最可能验证的能力。

### 行动

按需要生成三层材料：

```text
项目整体讲法
├── 具体回答
│   └── 连续追问训练
└── 证据与支撑
```

- 项目整体讲法：业务问题 → 个人职责与分工 → 架构方案 → 一两个难点与取舍 → 交付结果与应用验证。
- 自我介绍及其练习稿：必须用一条能力主线串起本轮 selected 的全部对外项目；存在岗位简历时，不得省略其中任一主项目。每个项目至少说明它承接的问题、个人动作或能力角色之一，不能只报名词。支撑项目若在主项目中有 confirmed 的实际接入点，应嵌入对应项目说明作用和协作分工，不为凑数量另起项目段。完整口述版本前提供独立的 `提取词`，按“定位与主线 → 每个项目 → 收束”成组，用 `｜` 分隔事实锚点。提取词只能压缩同一组 confirmed claims，不能新增事实，也不能写成第二份逐字稿；超时时先压缩各项目细节，不直接删除项目。
- 具体回答：一份只解决一个技术主题或简历描述。
- 追问训练：问题来源、替代方案、技术机制与协作分工。
- 回答与讲稿严禁包含 `[!warning]` 或类似免责警示块，正文中不出现“我不能表述为”、“当前材料未证明”、“未计入完成事实”等防穿帮/审稿语言。未做功能不主动列举，若被问及延展方向，按正向技术方案自然回答。
- 岗位专项计划保存到 `.career/opportunities/<id>/outputs/interview-plan.md`。
- 已有 Obsidian `15分钟`、逐字稿和追问地图可以继续维护，但必须建立 `.career/manifests/` 依赖记录。
- 完成后为产物写 manifest；岗位机会进入 `practicing`。

### Sensors

计算型检查：

- manifest 中 claim IDs 是否存在且 confirmed；
- 30 秒、2 分钟、5 分钟版本的非空白字符是否符合目标时长；
- wikilink、文件结构和 `git diff --check`；
- claim 变化后，相关面试文件是否已被标记 stale。

使用：

```bash
python scripts/oral_time.py <file> --section "<完整口述版本标题>" --min-seconds <min> --max-seconds <max>
python ../career-assets/scripts/state_lint.py --state-dir <state-dir> --repo-root <git-root>
```

推断型检查：

- 开场能否快速说清问题和个人职责；
- 技术方案是否由业务约束推出，而不是堆栈清单；
- 回答是否能被继续追问到实现和验证；
- 替代方案比较是否属于真实取舍或明确的技术理解；
- 口语化是否改变事实、技术含义或完成状态；
- 是否虚构故障、客户、用户、数字和个人贡献。

### 调整

- 回答缺事实 → `career-evidence`。
- 项目与岗位不匹配 → `career-positioning`。
- 结构完整但不自然 → 只按 oralization 调整表达。
- 追问无法回答 → 缩小简历／讲稿 claim，或标记待补证据；不要编故事。
- 反复出现同一种回答失败 → 记录为 retro 的 expression 或 harness gap。

## 时长默认值

- 30 秒：约 130～180 个非空白字符。
- 60～90 秒：约 260～400 个字符。
- 90～120 秒：约 450～620 个字符。
- 3～5 分钟：项目标准回答。
- 10～15 分钟：深挖素材，不应一次背完。

字符只是计算型预警，最终仍需用户实际朗读。

## 完成 Gate

- 每个回答有明确 claim 依赖；
- 自我介绍以能力主线串起全部对外项目，包含可独立查看的提取词，隐藏完整稿后仍可据此复述；
- 个人职责、协作边界和完成状态与 claims 一致；
- 时长检查通过或已说明偏差；
- 高频追问能够回答到证据和边界；
- 现有链接与 manifests 已验证；
- 没有在口语化阶段新增事实。

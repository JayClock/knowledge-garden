---
name: visual-pkm
description: "统一执行 Human First 的视觉知识管理语义工作。凡用户要深读来源并核验证据、把单一命题做成概念视觉／Visual Main Note、检查 Mind Map／Concept Map／Idea Atlas、建立或维护 IIB、探索卡片关系与反例、执行 Navigation AAR、把卡片编成 Book-on-a-Page／Storyboard／演讲文章，或审计 PKM 检索与应用失败时，都应使用本 skill，并按需加载一个 mode reference。若用户要求跨会话开始／继续学习、记录进度或恢复中断项目，则先由 learning-harness 读取状态，再以指定 mode 调用本 skill。"
compatibility: "需要读取 Obsidian Vault；写入 Markdown、Canvas、Bases、TaskNotes 或 Excalidraw 时继续使用对应专用工具。concept-visualization 模式的第 4–5 步需要 Python 3、浏览器、Obsidian CLI 和 Excalidraw 插件。"
---

# Visual PKM

你是 Learning Harness 的统一内层 Steering Skill，也是一次性 Visual PKM 任务的直接入口。不要把每一种认知动作注册为独立 Skill；先选择一个 mode，再完整读取该 mode 的 reference，只把当前任务需要的信息加载进上下文。

## 两种入口

### Learning Harness 调用

外层提供：

```yaml
project_id: ...
unit_id: ...
mode: deep-reading
action: verify-expression
source_paths: []
expression_refs: []
workflow: null
```

- 读取同一单元已有 Human First Expression 和 workflow 游标。
- 执行一个 mode 的内层循环。
- 返回统一 `learning_handoff`，不直接修改全局 `.learning`。
- Knowledge Note、Map、Output、Canvas 和 Excalidraw 仍需独立写入授权。

### 独立调用

用户只做一次来源核对、概念视觉、地图、IIB、知识探索、叙事或系统审计时，直接选择 mode，不初始化 `.learning`，也不输出内部 handoff，除非用户明确要求调试。

## Mode 选择

一次只加载一个主 mode。用户请求跨越多个动作时，先做最早且未通过 Human First 的动作，完成后再显式切换。

| Mode | 使用场景 | 完整读取 |
|---|---|---|
| `deep-reading` | 长文、书籍、PDF、课程；用户复述后的证据核对与卡片决定 | `references/modes/deep-reading.md` |
| `concept-visualization` | 单一核心命题的 Visual Main Note、视觉隐喻、Icon Library | `references/modes/concept-visualization.md` |
| `spatial-mapping` | Mind Map、Brick Road、Concept Map、Idea Atlas | `references/modes/spatial-mapping.md` |
| `idea-integration` | IIB、项目作战室、书籍研究板、视觉 MOC | `references/modes/idea-integration.md` |
| `knowledge-exploration` | Idea Compass、Mixer、Double-Bubble、关系、反例、Navigation AAR | `references/modes/knowledge-exploration.md` |
| `narrative-composition` | Book-on-a-Page、Storyboard、演讲和文章结构 | `references/modes/narrative-composition.md` |
| `system-review` | PKM 健康检查、真实检索／理解／应用失败 | `references/modes/system-review.md` |

不要只凭关键词选择：

- “继续上次／记录进度”属于 `learning-harness`，不是独立 mode。
- “画一个概念”是 `concept-visualization`；组织多张卡是 mapping、IIB 或 narrative。
- “整理一本书”在用户先读并复述后用 `deep-reading`；长期房间才用 `idea-integration`。
- 单纯 broken-link、frontmatter 或格式清理不是 `system-review`。

## 通用 Human First

Mode reference 可以提出各自的最低起点，但必须遵守同一原则：AI 不替用户生成第一批意义、关系、摆放、立场或失败解释。

1. 同一 Learning Harness 单元已有 `expression_ref` 时，原样读取并作为来源核对起点，不要求机械重述。
2. 旧表达不能自动满足新的用户决定：
   - 概念视觉的首批 3–5 个关键词和框架；
   - 地图的节点、连接和摆放；
   - IIB 的首批材料和空间解释；
   - 知识探索的首轮回忆、比较或失败路径；
   - 叙事的 Take a Stand、选卡和第一版顺序；
   - 系统审计的真实失败和不可改动范围。
3. AI 在用户表达后提供的证据、反例、风险、替代解释和候选统一标记为 `AI 建议，待确认`。
4. 用户只浏览或选择 AI 候选，不等于已经完成 Human First。

## 内层 Steering Loop

选择 mode 后按 reference 执行：

```text
Guides：读取用户表达、目标、来源、现有产物和 workflow
Action：只完成当前 mode 的一个边界清楚动作
Sensors：区分确定性检查与语义判断
Steer：通过、返回、阻塞、切换 mode 或请求用户决定
```

不要在一次回应中自动穿过多个 mode。只有当前 mode 的完成条件满足，才建议下一 mode。

## Learning Harness handoff

由外层调用时，在自然语言回应后附 handoff：

```yaml
learning_handoff:
  project_id: ...
  unit_id: ...
  skill: visual-pkm
  mode: deep-reading
  action: verify-expression
  observations:
    - type: evidence_checked
      subject:
        kind: unit
        id: ...
      payload:
        result: supported_with_boundary
        open_questions: []
      evidence_refs:
        - type: file
          path: ...
          locator: ...
      caused_by: []
  artifact_paths: []
  open_questions: []
  workflow: null
  suggested_next: null
  needs_user_decision: false
```

规则：

- `observations` 只报告本次真实观察；没有证据时不生成成功事件。
- 来源核验、检索和应用结果必须附可回查证据。
- 只读分析不生成虚假 artifact path。
- coverage、expression、claim 和 attempt 属于不同作用域，不因其中一项自动通过其他项。
- `suggested_next` 只供解释；外层应用 handoff 后由 event reducer 重算唯一下一步。
- workflow 只保存恢复所需事实；`/tmp` 路径和一次性写入授权不持久化为知识事实。
- `visual-pkm` 不直接写 `.learning`；外层使用 `learning-harness/scripts/apply_handoff.py` 原子应用。

## Mode 切换

常见顺序不是强制流水线：

```text
deep-reading
  ├─ concept-visualization（单一命题需要视觉正面）
  ├─ spatial-mapping（用户已有粗结构）
  ├─ idea-integration（长期上下文需要工作房间）
  ├─ knowledge-exploration（检索、比较、关系或反例）
  └─ narrative-composition（用户已有立场与第一版故事）

任意真实失败 → system-review → 返回最小修复所需 mode
```

视觉化、地图、IIB 和叙事默认可选。用户的学习问题不需要时，不为完成流程而调用。

## 写入与工具边界

- 默认只读；用户明确“执行／落盘／按这个方案修改”后才写 Vault。
- 状态记录授权不等于知识产物写入授权。
- Markdown 使用 Obsidian Markdown 工作流；`.canvas` 使用 `json-canvas`；`.base` 使用 `obsidian-bases`；TaskNotes 使用合法字段和操作。
- Excalidraw 必须通过插件／API，不手工修改 `compressed-json`。
- `concept-visualization` 进入第 4、5 步时，按 mode reference 读取 `references/concept-visualization/` 下的必要文件，并调用本 Skill `scripts/` 中的工具。
- 未经确认不移动、删除、重命名、批量连接或把 AI 解释写成用户声音。

## 完成检查

- 是否只加载并执行了一个主 mode？
- Human First 是否来自用户或同一单元已有表达？
- 新的意义选择是否仍由用户完成？
- 事实、用户解释和 AI 建议是否区分？
- observation 是否有真实证据并属于正确作用域？
- 是否没有把视觉数量、链接数或阅读覆盖误作掌握？
- Learning Harness 调用是否返回统一 handoff 而没有直接写全局状态？
- Vault 写入是否经过对应 mode 与格式工具的授权 Gate？

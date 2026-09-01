# 第 4 步直接生成完整视觉

## 固定交付

第 4 步根据用户确认的核心信息、视觉框架和文字样式说明，直接生成一个完整、可编辑的 Excalidraw 视觉正面，并通过 Obsidian Excalidraw 插件／API 写入第 1 步确定的 Visual Main Note。

用户负责意义和文字导演，AI 负责构图与绘制：

```text
用户核心命题 + 尽可能具体的文字视觉说明
→ AI 按 Icon First 盘点语义角色并搜索本地组件
→ AI 形成手绘 composition_plan、Icon First representation_plan 与完整构图规格
→ 内部 dry-run
→ 直接写入 Visual Main Note
→ 用户查看成品并用文字反馈
→ AI 在同一卡片中迭代
```

完整视觉直接出现在目标知识卡的 Excalidraw Drawing；临时 JSON 只用于执行和恢复。

## 进入条件

开始生成前需要：

1. 一个由用户提出、确认或已存在于其知识卡中的单一核心命题；
2. 已确定的知识卡目标：现有 `Knowledge/Notes/*.md`，或已确认标题且排除重复的新卡；
3. 用户提供的文字视觉说明；信息可以不完整，但至少不能与核心命题冲突；
4. 用户已经要求“生成视觉知识卡”“按这个描述画并写入”或等价执行动作。

第 4 项本身就是对已回显目标与说明的写入授权。用户只是在讨论方案、要求预览或明确说“先不要修改”时保持只读。

## 用户的文字视觉说明

用户尽可能从下面维度描述，缺项允许 AI 做可撤销的生产判断：

- 主体：画面里有什么角色、物体或抽象对象；
- 动作：谁对谁做什么，发生什么变化；
- 关系：对比、因果、包含、循环、阻隔、流动或层级；
- 构图：左右、上下、中心—外围、路径、前后景或留白偏好；
- 样式：手绘感、线条粗细、几何／有机、简洁／丰富、质感和参考气质；
- 配色：希望保留或避免的颜色、情绪和强调方式；
- 标签：必须出现、可以出现或不要出现的短文字；
- 禁止项：不希望使用的隐喻、对象、风格和构图。

3–5 个关键词可以作为简洁输入。用户没有描述的局部，由 AI 选择一个与已确认命题一致、容易修改的实现，并在报告中称为“AI 视觉实现”，不能写成用户偏好。

## 完整视觉的生成规则

完整读取并执行[Icon First 视觉生成规则](icon-first-generation.md)。

1. **只画一个命题。** 不把定义、所有例子、来源、`up` 和知识连接一起图解。
2. **直接完成主体—动作—关系。** 第一次写入就必须能够作为视觉正面阅读，不得只放零散素材、抽象骨架或待用户拼装的组件。
3. **图形先于文字。** 每个主要主体、动作和状态先搜索本地 Icon Library；按 `library-icon → native-pictogram → shape-relation → text` 决定表达。文字只负责专有名词、技术术语、数字、方向或仍未消除的歧义，不能用一组标签框代替视觉。
4. **手绘而非机械布局。** 使用不对称平衡、尺度差异、弯曲路径、局部重叠和有机留白；不要默认使用等宽矩形、统一卡片、完美网格和机械居中。给流程图增加 roughness 不等于手绘构图。
5. **语义准确优先。** 同名 icon 若引入错误隐喻，应拒绝并自制原生 pictogram 或改用更准确的空间关系；Icon First 不等于追求 icon 数量。
6. **原生可编辑。** 已有 Icon Library 组件通过 image reference 复用；自制主体、动作和关系使用原生 Excalidraw 元素。原生非文字元素的有效 `roughness` 至少为 1；外部 SVG、PNG/JPG 或远程图片不能直接嵌入。
7. **用户文字优先。** 用户指定的对象、方向、配色、标签和禁用项优先于 AI 默认审美。
8. **未指定项可由 AI 决定。** AI 可以选择构图、比例、局部对象、视觉层级和必要短标签，但这些都是可撤销的生产决定，不是新的知识主张。
9. **不画可见外壳。** Visual Main Note 自身不添加满幅背景矩形或外边框；画布背景由 Drawing appState 控制。固定导出边界需要矩形时，其描边与填充保持 `transparent`。
10. **保留现有内容。** 现有卡的正文、frontmatter、wikilinks 和非本轮 Drawing 元素不能丢失。相同 `visual_id` 的后续生成只替换本轮 AI 视觉，不覆盖用户或其他视觉元素。
11. **不伪造用户声音。** AI 新增的标签必须是视觉读法所需的短文本，不能替用户撰写未经确认的知识背面。

## Visual Spec

生成前在 `/tmp/visual-pkm-concept-visualization/<concept-slug>/visual-spec.json` 创建高层规格。它不是知识事实，也不写入知识卡正文。

最小示例：

```json
{
  "version": 1,
  "visual_id": "filtering-is-not-deletion",
  "core_message": "过滤只是暂时降低噪声，而不是不可逆地删除。",
  "framework": "过程式",
  "style_brief": "手绘粗线；从左向右；被过滤内容进入下方可恢复托盘；蓝灰主色，橙色强调回流。",
  "canvas": {
    "width": 1200,
    "height": 800,
    "background": "#F7F5F2"
  },
  "defaults": {
    "strokeColor": "#1F2937",
    "backgroundColor": "transparent",
    "strokeWidth": 2,
    "roughness": 1
  },
  "composition_plan": {
    "style": "hand-drawn",
    "spatial_grammar": "asymmetric organic flow",
    "hand_drawn_cues": ["scale contrast", "curved paths", "uneven spacing"],
    "avoids": ["uniform-grid", "repeated-text-cards"],
    "reason": "用一条不规则回流路径强调被过滤内容仍可恢复。"
  },
  "representation_plan": {
    "priority": [
      "library-icon",
      "native-pictogram",
      "shape-relation",
      "text"
    ],
    "semantic_units": [
      {
        "role": "过滤动作",
        "search_terms": ["筛网", "过滤", "filter"],
        "library_decision": "no-match",
        "choice": "native-pictogram",
        "element_keys": ["filter-body"],
        "reason": "本地没有准确表达暂时拦截的组件。"
      },
      {
        "role": "可恢复回流",
        "search_terms": ["回流", "恢复", "return flow"],
        "library_decision": "not-applicable",
        "choice": "shape-relation",
        "element_keys": ["return-flow"],
        "reason": "方向箭头比独立 icon 更准确地表达返回关系。"
      }
    ],
    "text_justifications": []
  },
  "elements": [
    {
      "key": "filter-body",
      "type": "diamond",
      "x": 470,
      "y": 210,
      "width": 180,
      "height": 220,
      "group": "filter",
      "role": "过滤动作"
    },
    {
      "key": "return-flow",
      "type": "arrow",
      "points": [[620, 560], [760, 560], [760, 410]],
      "group": "return-action",
      "role": "可恢复回流",
      "style": {"strokeColor": "#F59E0B", "endArrowHead": "arrow"}
    }
  ]
}
```

可用元素类型：`rectangle`、`ellipse`、`diamond`、`line`、`arrow`、`text`、`icon`。`icon` 只能引用已存在且通过结构校验的 `Knowledge/Assets/Excalidraw/Icon - *.excalidraw`。`group` 是后续 AI 自动判断可提取 icon 时的语义边界；它不要求用户选择，也不保证一定落库。

`composition_plan` 与 `representation_plan` 共同构成写入 Gate。前者必须声明手绘空间语法、实际手绘线索以及对统一网格和重复文字卡片的规避；后者要求每个主要语义角色记录实际检索词、本地组件决定、表达选择、对应元素和理由，并为每个 `text` 元素单独说明为何仍有必要。缺少任一计划、原生非文字元素有效 `roughness < 1`、所有意义都退回文字、引用 icon 却未登记，或存在未说明的文字元素时，dry-run 必须失败。坐标是否仍形成机械网格需要写入后实际查看；即使结构检查通过，等宽卡片与完美网格也不能通过视觉 Gate。

## 直接写入

完整执行[Visual Main Note 直接写入与 icon 自动提取](visual-main-note-write.md)。默认先运行内部 dry-run 检查 Icon First 表达计划、文字必要性、规格、目标、重复候选和组件路径；在本轮已经具有生成授权时，检查通过后立即 `--apply`，不把 dry-run 变成新的用户 Gate。

```bash
python3 ../.agents/skills/visual-pkm/scripts/write_visual_main_note.py \
  --visual-spec /tmp/visual-pkm-concept-visualization/<slug>/visual-spec.json \
  --existing "Knowledge/Notes/实际笔记.md" \
  --vault-root "$PWD"

python3 ../.agents/skills/visual-pkm/scripts/write_visual_main_note.py \
  --visual-spec /tmp/visual-pkm-concept-visualization/<slug>/visual-spec.json \
  --existing "Knowledge/Notes/实际笔记.md" \
  --vault-root "$PWD" \
  --apply
```

新卡先确认标题、搜索重复，再以 `--new-title`、`--duplicate-check-confirmed` 执行。不得手工编辑 `compressed-json`。

## 视觉完成后的状态

第 4 步结束时：

- Visual Main Note 已存在并能以 Excalidraw 视图打开；
- 完整视觉已经写入并可以直接评审；
- 用户通过文字反馈推进修改；
- 用户下一步只需观察成品，用文字描述希望保留、删除、移动、改色、改标签或改变强调的部分；
- Icon Library 此时还不自动增加新组件。只有成品完成后，才执行反向提取。

## 快速检查

- 是否直接生成并写入了完整视觉？
- 用户是否能只用文字描述和反馈视觉？
- 未指定细节是否被视为 AI 可撤销的生产选择，而不是用户意义？
- 是否只表达一个原子命题？
- 是否为主要主体、动作和状态搜索并打开了本地 icon 候选？
- 是否按 `library-icon → native-pictogram → shape-relation → text` 选择表达？
- 是否使用手绘式不对称、尺度差异和有机路径，而不是统一卡片与完美网格？
- 原生非文字元素的有效 `roughness` 是否至少为 1？
- 隐藏文字后是否仍能读出核心方向、对比或循环？
- 每个文字元素是否都有不可由图形替代的消歧理由？
- 是否通过插件／API 写入，且未修改 `compressed-json`？
- 是否保留了现有正文、frontmatter、链接和非本轮场景元素？
- 是否尚未从未定稿视觉提前提取 icon？

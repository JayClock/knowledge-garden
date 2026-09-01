# Icon First 与手绘构图规则

## 目标

Visual Main Note 的正面应当先让图形、动作和空间关系承担意义，文字只负责消歧；整体应呈现手绘草图的生命感，而不是机械整洁的 dashboard、PPT 流程图或 UI 卡片。Icon First 不是追求图标数量，而是避免把知识卡画成“矩形框里的提纲”。

语义准确始终高于复用率。找不到准确 icon 时，应当自制原生 pictogram 或用几何关系表达；不得为了减少文字而采用会误导读者的现成图标。

## 表达优先级

每个主要主体、动作或状态按以下顺序决定表达方式：

1. **`library-icon`**：搜索并打开 Icon Library 中的真实组件；语义准确时通过 image reference 复用。
2. **`native-pictogram`**：本地没有准确组件时，用原生 Excalidraw 元素画出可辨识的小型语义图形。
3. **`shape-relation`**：当意义主要来自包含、循环、阻隔、对比、流动或层级时，让形状、方向和关系线承担意义。
4. **`text`**：只有专有名词、技术术语、数字、方向或图形仍无法消除的歧义才使用文字。

现有 icon、原生 pictogram 和几何关系可以组合。文字可以作为短 caption 叠加在图形旁，但不能成为主要语义角色的唯一载体，除非 `representation_plan` 说明为什么前三种方式不准确。

## 手绘构图优先

“手绘”不是给规则网格加一点 roughness，而是让空间组织本身保持有机：

- 使用不对称平衡、尺度差异、弯曲路径、局部重叠和有呼吸的留白；
- 主体可以偏离整齐轴线，但动作方向和视觉层级必须清楚；
- icon 和 pictogram 采用可辨识的手绘轮廓，不追求像素级对齐；
- 箭头和路径可以轻微弯曲、错位或绕行，服务于动作而不是表格边界；
- 过程、循环和对比仍可结构化，但不要默认使用等宽矩形、统一卡片、完美网格和机械居中；
- 不用装饰性抖动制造“伪手绘”，也不牺牲语义、对比度和可读性。

Visual Spec 的原生非文字元素应使用至少 `roughness: 1`。Icon Library 组件保留自身已经确认的线条风格，不因当前卡的手绘 Gate 改写其内部元素。

## 两类 icon

### Icon Library 组件

- 路径固定为 `Knowledge/Assets/Excalidraw/Icon - *.excalidraw`；
- 搜索中文、英文、近义词、反义词和关键动作；
- 必须打开实际组件确认，不凭文件名或缩略图猜测；
- 通过 Excalidraw image reference 插入，保留比例和颜色；
- 复用组件不在当前卡定稿后重复提取。

### 当前构图中的原生 pictogram

- 用 `rectangle`、`ellipse`、`diamond`、`line`、`arrow` 等原生元素组成；
- 同一语义单位使用稳定 `group`；
- 脱离当前卡仍完整、可复用且不重复时，等成品确认后再自动提取到 Icon Library；
- 未定稿时不提前创建永久 icon。

## 生成前的语义角色盘点

在画元素前，从核心命题中只提取构成第一眼读法的主要角色：

- 主体：谁或什么承担动作；
- 动作：发生了什么变化；
- 状态：前后差异、成功／失败或显隐；
- 关系：因果、循环、阻隔、包含、流动、层级或对比。

不要把标题、定义、来源和全部例子都列为主要角色。每个主要主体、动作和状态都要先搜索 Icon Library；纯关系可以直接选择 `shape-relation`，但仍要说明为什么空间语法比独立 icon 更准确。

## `composition_plan` 与 `representation_plan`

`visual-spec.json` 必须包含可机检的构图与表达计划。最小结构：

```json
{
  "defaults": {
    "roughness": 1
  },
  "composition_plan": {
    "style": "hand-drawn",
    "spatial_grammar": "asymmetric organic flow",
    "hand_drawn_cues": ["scale contrast", "curved paths", "uneven spacing"],
    "avoids": ["uniform-grid", "repeated-text-cards"],
    "reason": "用一条有机回流路径表现过滤后的可恢复性。"
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
        "element_keys": ["filter-body", "filter-mesh"],
        "reason": "本地组件没有同时表达暂时拦截和可恢复性。"
      },
      {
        "role": "可恢复回流",
        "search_terms": ["回流", "恢复", "return flow"],
        "library_decision": "not-applicable",
        "choice": "shape-relation",
        "element_keys": ["return-arrow"],
        "reason": "方向箭头比独立物体更准确地表达返回关系。"
      }
    ],
    "text_justifications": [
      {
        "key": "filter-label",
        "reason": "保留技术术语‘过滤’用于消歧；图形承担主要意义。"
      }
    ]
  }
}
```

字段规则：

- `composition_plan.style` 固定为 `hand-drawn`；
- `spatial_grammar` 说明当前有机空间语法，而不是写“整齐排列”；
- `hand_drawn_cues` 记录实际使用的手绘线索；
- `avoids` 至少包含 `uniform-grid` 与 `repeated-text-cards`；
- 原生非文字元素的有效 `roughness` 至少为 1；
- `priority` 必须保持固定顺序；
- `semantic_units` 至少包含一个主要语义角色；
- `search_terms` 保存本轮实际使用的检索词；
- `library_decision` 只能是：
  - `reuse`：找到并复用本地组件；
  - `no-match`：没有语义准确的本地组件；
  - `rejected`：找到候选但因语义、构图或用户禁用项拒绝；
  - `not-applicable`：该角色本质是空间关系，不适合独立 icon；
- `choice` 必须是固定优先级中的一种；
- `element_keys` 必须指向 Visual Spec 中真实元素；
- `reason` 解释为什么该表达比下一层或上一层更准确；
- 每个 `text` 元素都必须出现在 `text_justifications` 中；没有文字时使用空数组。

`representation_plan` 只用于生产和检查，不写入知识卡正文。

## 文字使用规则

允许文字承担：

- 专有名词和无法可靠图示的技术术语；
- 数字、单位、时间或版本；
- 方向、极性或读图顺序的消歧；
- 用户明确要求保留的短标签。

不允许文字承担：

- 用一组标题框代替主体和动作；
- 重复图形已经清楚表达的内容；
- 把正文句子搬到画布；
- 仅因为制作 icon 更费工就退回文字；
- 用标签掩盖缺少关系、层级或动作的问题。

标签应尽量短。删除标签后若主要关系完全消失，优先补强 icon、pictogram 或空间语法，而不是增加解释段落。

## 生成与验证顺序

1. 提取主要语义角色；
2. 对主体、动作和状态搜索 Icon Library 并打开候选；
3. 按固定优先级选择表达方式；
4. 生成 `composition_plan` 和 `representation_plan`；
5. 再生成具有不对称、尺度差异和有机路径的 `elements`；
6. 运行 `write_visual_main_note.py` dry-run；
7. dry-run 通过后才允许 `--apply`；
8. 写入后执行第一眼测试、去文字测试和语义准确性检查。

## 完成 Gate

- **第一眼测试**：首先看到的是对象、动作和关系，而不是标题列表；
- **去文字测试**：隐藏所有文字后，仍能读出核心方向、对比或循环；
- **语义准确测试**：复用 icon 不会因为同名而引入错误隐喻；
- **必要文字测试**：每个文字元素都有独立的消歧理由；
- **原生性测试**：本地 icon 已验证，新增 pictogram 可编辑；
- **手绘构图测试**：画面不是等宽卡片、完美网格和机械居中；结构清楚但保留不对称、尺度差异与有机路径；
- **视觉密度测试**：没有用重复 icon 装饰画面，也没有为追求“无文字”堆砌难以识别的符号。

Icon First 通过的是语义承载方式，不是 icon 数量。零个 Library icon 仍可能合格，但“多个文字框加箭头”不能仅因结构完整就视为合格视觉正面；给机械布局统一加 roughness 也不算手绘构图。

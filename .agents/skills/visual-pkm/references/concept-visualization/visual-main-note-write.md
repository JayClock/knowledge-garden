# Visual Main Note 直接写入与 icon 自动提取

## 职责

本规则处理两种顺序固定但权限相同的机械动作：

1. 第 4 步把 AI 生成的完整视觉直接写入 Visual Main Note；
2. 用户通过文字反馈确认成品后，AI 自动判断并把其中可复用的原生组件提取到 Icon Library。

用户发出“生成视觉知识卡”“按这个描述画并写入”或等价执行请求后，该授权覆盖：创建／初始化已确认目标、写入完整视觉、根据其文字反馈更新同一视觉，以及成品完成后的自动 icon 提取。授权不覆盖新的核心命题、知识背面、`up` 或语义连接。

## 目标知识卡

### 现有卡

第 1 步记录：

```text
target_note_mode: existing
target_note_path: Knowledge/Notes/实际笔记.md
```

生成前完整读取并保护正文、frontmatter、wikilinks 和现有 Drawing。相同 `visual_id` 的后续版本只替换本轮 AI 生成元素；其他场景元素保持不动。

### 新卡

用户未指定现有卡时，在第 4 步写入前完成：

1. 请用户确认名词、名词短语或动名词标题；
2. 搜索标题、aliases、近义词和关键动作并阅读候选；
3. 没有重复后确定 `Knowledge/Notes/<标题>.md`；
4. 使用 `Templates/知识卡.md` 创建只含标题、H1、用户确认 abstract、空 `up` 和 `sources` 的最小卡；
5. 立即初始化 Drawing 并写入完整视觉。

不创建独立 Concept Visual 文件。`date`、`updated` 和工作流标签不由 Agent 添加。

## 直接写入流程

从 Vault 根目录运行：

```bash
SCRIPT="../.agents/skills/visual-pkm/scripts/write_visual_main_note.py"
SPEC="/tmp/visual-pkm-concept-visualization/<slug>/visual-spec.json"

python3 "$SCRIPT" \
  --visual-spec "$SPEC" \
  --existing "Knowledge/Notes/实际笔记.md" \
  --vault-root "$PWD"
```

内部 dry-run 必须检查：

- 核心信息、框架和用户文字 style brief 存在；
- `composition_plan` 明确采用手绘空间语法、实际手绘线索，并规避 `uniform-grid` 与 `repeated-text-cards`；
- 原生非文字元素的有效 `roughness` 至少为 1；
- `representation_plan` 按 `library-icon → native-pictogram → shape-relation → text` 覆盖主要语义角色；
- 每个主要主体、动作和状态都记录了实际 icon 检索词与复用／拒绝决定；
- 每个 `text` 元素都有必要性说明，且主要语义没有全部退回文字；
- Visual Spec 只包含受支持的原生元素或已验证 Icon Library 引用；
- 坐标、颜色、组和元素 key 有效；
- 目标路径与第 1 步一致；
- 新卡不存在重复候选；
- `visual_id` 可用于安全替换本轮视觉。

用户已经要求生成并写入时，dry-run 通过后立即使用同一参数加 `--apply`，不追加组件选择或二次授权：

```bash
python3 "$SCRIPT" \
  --visual-spec "$SPEC" \
  --existing "Knowledge/Notes/实际笔记.md" \
  --vault-root "$PWD" \
  --apply
```

新卡改用：

```bash
python3 "$SCRIPT" \
  --visual-spec "$SPEC" \
  --new-title "用户确认的名词短语" \
  --duplicate-check-confirmed \
  --vault-root "$PWD" \
  --apply
```

脚本通过 `write_visual_main_note_apply.js` 在运行中的 Obsidian 内调用 Excalidraw Automate API：

- 创建或转换目标知识卡；
- 先复用语义准确的已有 `.excalidraw` icon，再用手绘原生 pictogram、不对称构图和有机路径完成其余主体、动作与关系；
- 复用 icon 时使用 image reference，文字仅作为经过 `representation_plan` 说明的短消歧标签；
- 用 `visual_id` 和语义 group 标记本轮 AI 元素；
- 后续迭代只替换相同 `visual_id`；
- 保存后验证元素数量、正文、frontmatter、Drawing 和视图；
- 不手工读写 `compressed-json`。

## 用户文字反馈与迭代

写入后打开目标卡，让用户直接看成品。用户只需用文字说明，例如：

- “左侧太重，主体往中心收”；
- “保留回流，但删掉时钟”；
- “线条更松、更像铅笔”；
- “不要人物，改成门与流体”；
- “标签只留两个词”；
- “整体方向对了，可以定稿”。

AI 把反馈转换为同一个 `visual_id` 的新 Visual Spec，再执行 dry-run 与 `--apply`。用户没有要求提供多个方案时，不强制 A／B／C，也不要求用户进入画布修改。AI 可以解释改动的可观察后果，但不能把自己的构图选择描述成用户已经表达的偏好。

## 成品后的自动 icon 判断

只有用户确认成品或明确表示视觉完成后才判断。AI 自动检查每个本轮语义 group；不要求用户选择或确认提取清单。

### 应提取

一个 group 同时满足以下条件时自动列入：

- 脱离本卡仍能识别和复用；
- 是一个完整语义单位，而不是单条装饰线或布局碎片；
- 只含原生 Excalidraw 元素；
- 不依赖本卡专属标题、坐标、背景或其他对象才能成立；
- 不是已有 Icon Library 组件的重复版本；
- 形状、动作和必要内部细节足以保持识别性。

### 不提取

- 整张构图、可见外壳、画布背景或导出边界；
- 只连接本卡对象的箭头、路径和关系线；
- 本卡专属标签、标题、解释性段落；
- 单独拿出就失去意义的局部形状；
- 已经作为 image reference 复用的现有 icon；
- 与 Icon Library 中已有组件语义和外观等价的重复项。

“自动判断”允许结果为空。不要为了扩充词库而拆出低价值或重复 icon。

## 自动落库

AI 先在 Icon Library 按同义关键词搜索并打开近似组件。排除语义重复后，在临时目录生成：

```json
{
  "version": 1,
  "visual_id": "filtering-is-not-deletion",
  "icons": [
    {
      "group": "filter",
      "keywords": ["筛网", "过滤", "降噪"],
      "source": "Own",
      "reason": "脱离本卡仍可表示过滤动作。"
    }
  ]
}
```

然后运行：

```bash
python3 ../.agents/skills/visual-pkm/scripts/extract_visual_icons.py \
  --note "Knowledge/Notes/实际笔记.md" \
  --extraction-spec /tmp/visual-pkm-concept-visualization/<slug>/icon-extraction.json \
  --duplicate-check-confirmed \
  --vault-root "$PWD"

python3 ../.agents/skills/visual-pkm/scripts/extract_visual_icons.py \
  --note "Knowledge/Notes/实际笔记.md" \
  --extraction-spec /tmp/visual-pkm-concept-visualization/<slug>/icon-extraction.json \
  --duplicate-check-confirmed \
  --vault-root "$PWD" \
  --apply
```

`extract_visual_icons_apply.js` 从插件保存后的 Drawing 读取对应 group，复制其原生元素、移除本卡位置与绑定、归一化坐标，并保存为：

```text
Knowledge/Assets/Excalidraw/Icon - 关键词1, 关键词2 - Own.excalidraw
```

规则：

- 每个文件只有一个覆盖全部元素的公共 group；
- 不含 image、frame 或 embeddable；
- 保留成品颜色，不执行项目色板 Gate；
- 不覆盖同名文件；
- 不改变来源 Visual Main Note；
- 文件名是唯一索引，不建立 Markdown 清单、JSON 注册表或逐项元数据。

完成后运行：

```bash
python3 ../.agents/skills/visual-pkm/scripts/validate_icon_library.py \
  --vault-root "$PWD" --check
```

## 验证

### Visual Main Note

- 目标路径正确且可以切换到 `viewType: excalidraw`；
- 完整视觉已出现并可以直接评审；
- 本轮主体、动作和关系均可见，第一眼不是标题框列表、dashboard 或机械流程图；
- 构图具有不对称、尺度差异和有机路径，但动作方向仍然清楚；
- 隐藏文字后仍能读出核心方向、对比或循环；
- 每个保留的短标签都有独立消歧理由；
- 原有正文、frontmatter、链接和非本轮场景元素保留；
- 新卡没有模板占位内容和工作流标签；
- 没有手工修改 `compressed-json`。

### Icon Library

- 自动提取发生在成品确认后；
- 可提取判断由 AI 自动完成；
- 未把完整构图、关系线、背景或专属文字落库；
- 没有重复创建已有 icon；
- 每个新组件是纯原生、单公共 group 的 `.excalidraw`；
- 规定文件名可被 Icon Library 自动发现；
- 原知识卡视觉没有因提取而变化。

## 完成报告

只报告：

- Visual Main Note 路径与 `visual_id`；
- AI 实际生成／替换的元素数量；
- 手绘构图摘要：空间语法与实际手绘线索；
- Icon First 表达摘要：复用 icon／原生 pictogram／几何关系／必要文字；
- 是否保留正文、frontmatter、链接和其他 Drawing 元素；
- 自动判断后新建、复用或跳过的 icon 路径；
- `validate_icon_library.py --check` 结果；
- 仍需用户用文字反馈的视觉问题。

# 第 5 步知识卡与 Excalidraw 初始化

## 固定使用时机

用户完成第 4 步 HTML 预览并贴回入选编号后，第 5 步初始化承载本轮视觉正面的知识卡，把入选 icon 确保落地为 Vault 内 `.excalidraw` 组件并嵌入初始视图，再由用户亲自绘制第一张草图。默认流程不再创建独立 Concept Visual 文件，也不提供纸笔或 Vault 外绘制分支。

初始化与素材准备不解释概念，也不生成完整构图。它只建立知识卡与 Drawing、处理用户实际入选的 icon，并把这些组件彼此独立地松散摆成素材托盘；不得顺便添加未入选图形、标题以外的文本元素、箭头、关系、AI 选择的新隐喻、HTML 记录或过程日志。

## 第 1 步记录目标状态

第 1 步确认核心信息时，同时记录以下两种状态之一：

```text
target_note_mode: existing
target_note_path: Knowledge/Notes/实际笔记.md
```

或：

```text
target_note_mode: new
target_note_path: pending
```

- 用户在第 1 步直接指定现有知识卡时，完整读取该卡并保存其实际路径；第 5 步不得再次询问承载方式或改换目标文件。
- 用户没有指定知识卡时，只记录 `new`，不要在第 1–4 步提前创建文件；第 5 步再确认名词短语标题和 `Knowledge/Notes/` 目标路径。
- 读取或选择现有知识卡、贴回入选编号都不等于授权修改。除非用户已经明确要求“初始化并嵌入”或等价执行动作，否则第 5 步转换、组件落地与嵌入前仍需取得写入授权。

## 第 5 步初始化 Gate

### A．现有知识卡

第 4 步参考确认后回显：

```text
第 5 步目标：Knowledge/Notes/实际笔记.md
即将执行：保留原有正文、frontmatter 与链接，初始化 Excalidraw Drawing；把你入选的 icon 确保落地为 Vault 内 `.excalidraw` 组件，并作为独立 image reference 松散嵌入初始视图。
不会添加：未入选图形、文字元素、连接、完整构图或 AI 新视觉方案。
请回复“初始化并嵌入”后执行。
```

用户在本轮此前已经明确授权该目标执行初始化、组件落地与嵌入时，不重复索取授权；只回显即将执行的机械操作。若此前只授权空白初始化，不把授权自动扩展到 icon 落地与嵌入。

### B．新知识卡

1. 根据已确认的核心信息，请用户确认一个名词、名词短语或动名词标题；AI 可以提供不超过 3 个标题候选，但不能替用户定名。
2. 搜索标题、aliases、近义词和关键动作，阅读候选，避免创建同义卡。
3. 没有重复时回显拟创建路径 `Knowledge/Notes/<标题>.md`、确认后的核心信息，以及初始化 Drawing、落地入选 icon、嵌入初始素材托盘的动作。
4. 用户明确授权后，使用 `Templates/知识卡.md` 创建卡片，只保留标题、H1、用户已确认的 abstract，以及空的 `up`、`sources`；删除模板注释、空的知识连接节和占位内容。
5. 不手工添加 `date`、`updated`、工作流标签或未经用户确认的来源、上位关系和正文解释。
6. 创建后立即通过 Excalidraw 插件初始化 Drawing，可以把新画布背景设为项目 `--concept-color-canvas`，再按本轮入选编号落地并嵌入 icon；组件通过结构校验即可，不以颜色是否属于项目色板作为写入条件。知识卡自身不绘制可见的满幅背景矩形或外边框；若为了固定导出范围保留边界矩形，其描边与填充都设为 `transparent`，由父级地图／大卡决定可见外壳。

## 执行前

1. 从 Vault 根目录运行 `git status --short`，识别已有修改。
2. 完整读取目标 Markdown，并确认它位于 `Knowledge/Notes/`，不是 Canvas、Base、PDF 或其他格式。
3. 记录转换前内容；可以复制到 `/tmp` 供转换后核对，但不得把临时备份写入知识库。
4. 确认 Obsidian 已打开、Excalidraw 插件已启用，并显式使用 `vault="content"`。
5. 若目标已经包含 `excalidraw-plugin: parsed` 和有效 Drawing 数据，不重复转换；只打开 Excalidraw 视图。

## 默认脚本执行

使用 `scripts/prepare_visual_main_note.py` 作为第 5 步的默认执行入口。脚本先做 dry-run，只输出确定性计划；只有用户已经授权“初始化并嵌入”后才传 `--apply`。Python 负责解析入选编号、验证目标和原生组件；配套 `prepare_visual_main_note_apply.js` 在正在运行的 Obsidian 中调用 Excalidraw 插件完成转换、image reference、保存与验证。不要直接运行内部 JS。

现有知识卡先 dry-run：

```bash
SCRIPT="../.agents/skills/visual-pkm-concept-visualization/scripts/prepare_visual_main_note.py"
PREVIEW="/tmp/visual-pkm-concept-visualization/<slug>/step-4-preview.json"
NOTE_PATH="Knowledge/Notes/实际笔记.md"

python3 "$SCRIPT" \
  --preview-json "$PREVIEW" \
  --selected A02,A05 \
  --existing "$NOTE_PATH" \
  --vault-root "$PWD"
```

确认计划没有 `pending_temp_icons`，并且目标、编号和组件路径与用户确认一致后执行：

```bash
python3 "$SCRIPT" \
  --preview-json "$PREVIEW" \
  --selected A02,A05 \
  --existing "$NOTE_PATH" \
  --vault-root "$PWD" \
  --apply
```

新知识卡在用户确认标题、核心信息并完成人工语义重复检查后执行：

```bash
python3 "$SCRIPT" \
  --preview-json "$PREVIEW" \
  --selected A02,A05 \
  --new-title "用户确认的名词短语" \
  --core-message "用户确认的核心信息" \
  --duplicate-check-confirmed \
  --vault-root "$PWD" \
  --apply
```

若入选项含 `/tmp/` SVG、PNG/JPG 或其他本地图像参考，dry-run 会返回 `status: needs_materialization` 并拒绝 `--apply`。先按本节后文规则把每项忠实描摹为 Vault 内原生 `.excalidraw` 组件，再显式提供映射：

```bash
--icon-map "/tmp/.../selected.svg=Knowledge/Assets/Excalidraw/Icon - Stable name.excalidraw"
```

脚本提供以下保护：

- `--apply` 前验证所有组件都是单一公共 group、没有嵌套 image／frame 的原生 `.excalidraw`；
- 现有卡写入前在 `/tmp/visual-pkm-concept-visualization/backups/` 建立副本，并用文件大小与修改时间防止 dry-run 后并发覆盖；
- 已有 Drawing 不重复转换，已有同一路径 image reference 不重复嵌入；
- 新卡读取 `Templates/知识卡.md` 的固定接口，只创建最小 frontmatter、H1 和用户确认的 abstract；
- 对永久 icon 组件执行原生结构校验并保留现有颜色；新建或首次初始化的 Drawing 可以使用 `--concept-color-canvas` 作为默认背景，已有 Drawing 保留当前背景；
- 通过 `obsidian-excalidraw-plugin:convert-to-excalidraw` 和 Excalidraw Automate API 操作，不拼接或手工改写 `compressed-json`；
- 素材托盘放在原场景右侧边界外，只新增独立 image reference，并验证原正文、frontmatter、wikilink 文本和原场景元素没有丢失；
- 输出 JSON 报告，包括新增／复用组件、目标路径、视图类型、画布背景、组件颜色保留策略和备份路径。

脚本失败时不要绕过保护直接修改压缩数据；读取错误，修复前置条件后重新 dry-run。

## 可选的逐卡配色管理

配色审计不再是知识卡初始化或最终完成的 Gate。用户可以保留本地组件、临时重绘组件和 `source-palette` 素材中已经确认的颜色；非项目色板颜色本身不构成错误。已描摹 icon 的内部颜色始终排除在项目色板审计与迁移之外，即使目标知识卡选择加入受管集合。

只有用户明确要求把当前卡统一到项目语义色板或登记为受管文件时，才读取 `references/palettes.md`，由用户确认各元素的语义颜色，再通过 Excalidraw 插件／API 修改。随后可按需运行：

```bash
PALETTE_SCRIPT="../.agents/skills/visual-pkm-concept-visualization/scripts/sync_excalidraw_palette.sh"
NOTE="Knowledge/Notes/实际笔记.md"

bash "$PALETTE_SCRIPT" --check --path="$NOTE"
bash "$PALETTE_SCRIPT" --apply --path="$NOTE" --register
bash "$PALETTE_SCRIPT" --check --path="$NOTE"
```

登记知识卡只是用户选择的色板维护，不等于把卡中组件自动登记到 Icon 索引。没有选择项目色板管理时，不运行这些命令，也不因未登记而阻止报告完成。

## 入选 icon 落地与嵌入

知识卡 Drawing 可打开后，读取第 4 步 `step-4-preview.json`，按用户贴回的候选编号展开其中 `icons`，去重后只处理实际入选项：

1. **统一原生格式**：所有进入知识卡或 Icon 索引的 icon 都必须是只含原生元素的纯 JSON `.excalidraw` 组件；SVG、PNG/JPG、WebP 等图像只能作为临时描摹参考，不得直接成为永久 icon。
2. **复用本地组件**：`src` 已指向 `Knowledge/Assets/Excalidraw/Icon - *.excalidraw` 时，验证场景可解析、内部没有 image 嵌套、存在单一公共 group，并按现有颜色直接复用；它被视为已经完成描摹。不要复制出第二份，也不要因配色不属于项目色板而拒绝。
3. **描摹临时参考**：`src` 指向本轮 `/tmp/` SVG、PNG/JPG 或其他图像参考时，不把源图复制到 Vault，也不把它作为 image 封装。以用户已经确认的预览外观（包括颜色）为唯一机械目标，通过 Excalidraw 插件／API 用原生元素描摹为一个结构完整、可识别、单一公共 group 的纯 JSON `.excalidraw` 文件，保存为 `Knowledge/Assets/Excalidraw/Icon - <稳定名称>.excalidraw`。创建前搜索同名与近似组件，能够忠实复用时不重复创建。
4. **不自动登记词库**：落地组件不自动修改 `Icon 索引.md` 或 `icon-index-registry.json`；只有用户另行明确要求扩充视觉词库时才登记。
5. **嵌入知识卡**：通过 Excalidraw 插件／API 把每个入选 `.excalidraw` 文件作为 image reference 加入目标 Drawing。每个 icon 保持独立可移动与原始纵横比，只按编号做无语义的松散横排或素材托盘并留出间距；不添加标签、容器、箭头或关系，不组合成最终画面。
6. **设置视口**：让初始视图能同时看到全部入选组件。若目标已有 Drawing，不移动、缩放、删除或覆盖用户原有元素；把素材托盘放到现有内容边界之外的空白区域。

不得手工改写目标知识卡的 `compressed-json`。组件创建、image reference、Embedded Files 与场景保存都通过 Excalidraw 插件／API 完成。

## 打开绘图视图

先检查当前视图：

```bash
obsidian vault="content" eval \
  code="app.workspace.activeLeaf?.view?.getViewType?.()"
```

只有返回 `markdown` 时才执行切换，避免把已经打开的绘图切回 Markdown：

```bash
obsidian vault="content" command \
  id="obsidian-excalidraw-plugin:toggle-excalidraw-view"
```

## 验证

初始化完成后至少检查：

1. 目标位于 `Knowledge/Notes/`，并与第 1 步记录或第 5 步确认的路径一致；
2. 原有 H1、核心观点、正文、`sources`、`up` 和 wikilinks 没有丢失或改写；
3. 新卡的文件名、frontmatter `title`（如存在）和 H1 核心名称一致，且没有模板占位内容；
4. frontmatter 包含 `excalidraw-plugin: parsed`；
5. 文件包含由插件生成且闭合的 `## Drawing` 与 `compressed-json` 数据；
6. 初始化没有新增 `## Text Elements`、箭头、连接、标签或完整构图；场景新增项只包含用户实际入选的 icon image references；
7. 每个入选 icon 都解析到真实 Vault `.excalidraw` 文件；所有 SVG、PNG/JPG 或其他图像参考都已描摹为原生元素，没有被复制、封装或直接嵌入，未入选项没有落地；
8. 每个新落地组件是单一公共 group 的原生元素，不含嵌套 image；目标 Drawing 的 Embedded Files 指向这些 `.excalidraw` 文件且重新打开后可见，且组件颜色没有被初始化流程自动替换；
9. 当前目标能够切换到 `viewType: excalidraw`，视口能看到入选素材托盘；
10. 没有仅为流程新增 `视觉思考`、`概念视觉` 或 `excalidraw` 标签；
11. `obsidian vault="content" links path="$NOTE_PATH"` 仍能解析原有内部链接。

可以运行 `obsidian vault="content" dev:errors` 检查插件行为，但要区分本次转换错误与此前已经存在的无关插件错误。

## 进入第 5 步绘制

验证初始素材托盘后再提示用户：

```text
知识卡与初始视图已准备：Knowledge/Notes/……md
第 4 步参考 HTML：/tmp/visual-pkm-concept-visualization/……/step-4-preview.html
你选择的参考：A……
已落地／复用组件：Knowledge/Assets/Excalidraw/Icon - ….excalidraw

入选 icon 已作为彼此独立的素材放在初始视图中。现在请用约五分钟移动、缩放、组合并按需补画，亲自完成第一张草图。请由你决定主体、动作、关系，以及保留哪些具体实例、状态和必要短标签；AI 只说明它们可能承担的功能或读法，不替你衡量、删减或分配正反面。
```

AI 可以机械落地并嵌入用户实际入选的 icon，但不替用户完成首张草图；松散素材托盘不算 Express。

## 失败处理

- 用户没有授权时停在初始化 Gate，不创建、转换、落地或嵌入文件。
- 命令没有执行时，先确认目标文件处于活动 Markdown 视图，再重试一次。
- 文件已经是 Excalidraw 时停止转换，不覆盖已有 Drawing；只在边界外新增入选素材托盘。
- 临时图像参考无法忠实描摹为原生 Excalidraw 时停止该项并说明，不用 SVG／位图 image、截图或几何占位符冒充。
- 若正文、frontmatter 或原有场景元素出现意外变化，停止后续操作，对照脚本报告中的 `/tmp/` 转换前副本做小范围检查；不要自动覆盖用户可能同时产生的新修改。
- 脚本不会在失败时自动删除或回滚已创建／已转换的知识卡，避免覆盖执行期间的用户编辑；根据错误中返回的目标或备份路径检查后，再决定最小修复。
- 若 Drawing 无法由插件重新打开，不手工修复压缩数据，应回到插件命令或 API 重新保存。

## 完成报告

只需说明：

- 创建或转换的目标路径；
- 使用了 Excalidraw 插件／API；
- 实际复用或新落地的 `.excalidraw` 组件路径，以及其颜色是否按用户确认外观保留；
- 入选 icon 是否已作为 image reference 嵌入且重新打开可见；
- 原有文字背面、链接和场景元素是否保留；
- 是否已验证 `viewType: excalidraw`；
- 当前只有无语义素材托盘，下一步由用户亲自组合并绘制。

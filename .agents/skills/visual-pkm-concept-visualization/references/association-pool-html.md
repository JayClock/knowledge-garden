# 第 4 步固定视觉参考 HTML

## 固定交付

用户在第 3 步确认视觉框架后，第 4 步必须生成一个可在浏览器打开的实际图像预览 HTML。它把所需主体、动作、关系和辅助组件并排展示，供用户观察、选择和重组；第 5 步经授权把入选 icon 确保落地为 Vault 内 `.excalidraw` 组件并嵌入知识卡初始视图，再由用户亲自移动、组合和补画第一张草图。

生成前必须已经具备：

- 用户确认的单一核心信息；
- 用户先列出的 3–5 个关键词及 AI 扩展联想；
- 用户在第 3 步选定的视觉框架。

HTML 是临时视觉参考，不是知识卡正面、最终构图或 AI Express。第 4 步展示结构完整、可识别、可分层重组的视觉零件和简单组合可能，不替用户完成第 5 步草图。组件可以相对完整；快速、粗糙、不润色描述的是第 5 步首次 Express 的整体构图，而不是第 4 步 icon 的质量。

## 固定内容

每个预览候选都必须包含实际可见图像，而不只是文字占位：

- 先使用已有本地图标和用户已有草图；优先通过分层、叠加、小幅调整和选择性复用形成可重组组件；
- 本地视觉词库没有合适组件时，才到 [Flaticon](https://www.flaticon.com/) 检索主体、动作或关系，把候选当作观察轮廓与结构的视觉字典；
- 不下载、转换、截图、描摹路径或嵌入 Flaticon 的 PNG／SVG；观察后在系统临时目录重新绘制 SVG 视觉组件；
- 临时重绘组件必须保留可识别轮廓、关键动作、部件关系和必要细节，并适合分层、替换和重组。可以用基础形状和自制路径完成，但不能只是几个几何形状组成的低完成度占位符，也不能成为精炼的最终构图；其颜色可以取自项目语义色板，也可以采用与本轮视觉意图一致的其他配色，第 5 步应保留用户在预览中确认的颜色；
- 不保留 Flaticon 的详情页、作者、素材 ID、权利说明或其他逐项来源记录；本轮第 4 步不得把这些字段新增到 JSON、HTML 或 Vault，永久组件只在规定文件名末尾保留来源名称；
- 每项使用 1–3 个本地已有 Excalidraw icon 组件或本轮临时重绘的 SVG／其他本地图像参考，并只说明名称、类型、怎样画、分层方式和突出什么，不附加素材追溯、误读或风险；所有非 `.excalidraw` 项都只是预览参考，入选后必须先描摹为原生 Excalidraw 组件；
- 预览只帮助人类模仿和重组视觉零件，不能做成可直接充当最终视觉的精炼构图。

候选数量按实际需要决定。使用 `scripts/render_association_pool.py` 生成可筛选、可选择的独立 HTML；用户从中选择或重组 1–3 个参考方向，使用页面按钮复制入选编号并贴回对话。

## 临时位置与生成

固定输出写入系统临时目录，避免未经单独授权改动 Vault：

```text
/tmp/visual-pkm-concept-visualization/<concept-slug>/
├── step-4-preview.json
└── step-4-preview.html
```

从 Vault 根目录运行：

```bash
PREVIEW_DIR="/tmp/visual-pkm-concept-visualization/<concept-slug>"
mkdir -p "$PREVIEW_DIR"

python3 ../.agents/skills/visual-pkm-concept-visualization/scripts/render_association_pool.py \
  "$PREVIEW_DIR/step-4-preview.json" \
  "$PREVIEW_DIR/step-4-preview.html" \
  --asset-root "$PWD" \
  --open
```

若浏览器无法自动打开，返回完整 HTML 路径供用户手动打开。第 4 步期间 JSON、HTML 和临时图像参考都不发布、不写进知识卡正文，也不写入 Icon Library。第 5 步只有用户实际入选且授权落地的参考才按预览外观描摹为 Vault 内原生 `.excalidraw` 文件；不复制或封装 SVG、PNG/JPG 等源图，未入选项继续留在 `/tmp/`。

## 最小候选内容

```json
{
  "id": "A01",
  "type": "视觉组件",
  "label": "筛网",
  "visualization": "模仿绘制一个筛网，让对象流从中穿过。",
  "emphasis": "过滤动作",
  "icons": [
    {
      "src": "Knowledge/Assets/Excalidraw/Icon - 漏斗, 过滤器, 筛选, 提纯, 选择, 降噪, 已应用, filter - ACNH.excalidraw",
      "alt": "筛网",
      "role": "过滤组件"
    }
  ]
}
```

编号只用于方便选择，不承担知识关系。每项至少有一个真实图像，最多三个，便于人类在第 5 步选择素材而不被精炼成品限制。`src` 优先指向本地已有的 `.excalidraw` icon 组件，也可以指向本轮 `/tmp/` 中重绘的可识别 SVG 或其他本地图像参考；不能使用远程 URL。渲染脚本会在内存中把纯 JSON `.excalidraw` 组件转换为 HTML 可显示的 SVG data URI，不在 Vault 生成 SVG。第 5 步以这些 `src` 为确定性清单：本地 `.excalidraw` 组件通过结构校验后按现有颜色直接复用；其他入选图像参考按用户确认的外观（包括颜色）描摹为原生 `.excalidraw`，随后才作为 image reference 嵌入目标知识卡。任何源图都不得直接成为知识卡 icon；联想候选不包含来源追溯或逐项风险字段。

## 快速检查

- 用户是否已经确认核心信息、首批关键词和第 3 步视觉框架？
- 第 4 步是否实际生成并打开了 HTML，而不是只给文字候选或文件路径？
- 是否先检索本地实际 Excalidraw icon 组件，只有本地不足时才检索 Flaticon？
- 是否只观察 Flaticon 后临时重绘 SVG 组件，没有下载、转换、截图、描摹路径或嵌入原素材？
- JSON、HTML 和其他记录中是否没有 Flaticon 详情页、作者、素材 ID 或权利说明？
- 每个临时重绘组件是否结构完整、可识别、可分层重组，而不是低完成度几何占位符；第 5 步是否保留了用户确认的颜色？
- 每个候选是否包含本地 Excalidraw icon 或临时图像参考、怎样画、分层方式和突出什么，同时不附加素材追溯或逐项风险？
- HTML 是否只提供可模仿的完整组件和简单组合可能，而没有替用户完成最终构图？
- 是否把快速、不润色的粗草图留到第 5 步首次 Express？
- 用户是否先预览、选择或重组参考，再进入第 5 步授权初始化、落地和嵌入，并由自己在知识卡中完成组合？
- 第 4 步是否把 JSON、HTML 和临时图像参考保存在系统临时目录；第 5 步是否把所有非 `.excalidraw` 入选项先描摹为原生 `.excalidraw`，不复制、封装或直接嵌入源图，并采用规定文件名进入 Icon Library？

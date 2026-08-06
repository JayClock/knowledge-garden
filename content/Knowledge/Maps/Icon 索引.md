---
excalidraw-plugin: parsed
title: Icon 索引
aliases:
  - Icon Library
  - 图标库
tags:
  - icon
  - 视觉思考
  - assets
type: 资源索引
icon-count: 31
preferred-format: svg
visual-style: handdrawn-master-variable
master-suffix: -handdrawn
master-roughness: 2
master-stroke-width: 1.8
master-linecap: round
master-linejoin: round
master-vector-effect: non-scaling-stroke
master-optical-stroke-policy: scale-invariant
color-variable: --icon-color
color-fallback: "#000000"
palette-variable-prefix: --concept-color-
palette-css: Knowledge/Assets/Styles/concept-visualization-palette.css
active-palette: Teal–Paper Semantic 8
palette-reference: https://coolors.co/001219-005f73-009999-99dede-f3e9e0-ee9b00-ca6702-bb3e03-fff6f0
palette-inspiration: https://www.visual-thinking-workshop.com/
palette-trends-source: https://coolors.co/palettes/trending
palette-variables:
  ink: --concept-color-ink
  deep-structure: --concept-color-deep-structure
  positive-flow: --concept-color-positive-flow
  cool-fill: --concept-color-cool-fill
  warm-fill: --concept-color-warm-fill
  attention: --concept-color-attention
  friction: --concept-color-friction
  conflict: --concept-color-conflict
  canvas: --concept-color-canvas
allowed-external-sources:
  - Flaticon
  - Noun Project
  - Google Images
  - Google Material Symbols
  - Tabler Icons
date: 2026-08-02
updated: 2026-08-06 15:31:35
---
# Icon 索引

> [!info] 视觉词汇表
> 所有概念视觉使用的 SVG 统一存放于 `Knowledge/Assets/Icons/`。带 `-handdrawn.svg` 后缀的文件是知识卡直接引用的规范手绘母版；无该后缀的同名文件保留原始来源几何与许可信息。外部视觉元素可以从 [Flaticon](https://www.flaticon.com/)、[Noun Project](https://thenounproject.com/)、[Google Images](https://images.google.com/)、[Google Material Symbols](https://fonts.google.com/icons) 和 [Tabler Icons](https://tabler.io/icons) 寻找；来源、作者、许可和使用位置统一记录在这里。Google Images 只作为发现入口，实际采用素材时应记录原始页面，而不是搜索结果或缩略图链接。

> [!tip] 可变配色 SVG
> 全局语义颜色集中定义在 `Knowledge/Assets/Styles/concept-visualization-palette.css`，变量前缀为 `--concept-color-`；替换色板时只修改该文件的九个基础变量。规范手绘母版与原始 SVG 都保留许可元数据，单色入口统一使用 `--icon-color` 并默认回退为 `#000000`；CSS 中的 `--icon-color` 已指向 `--concept-color-icon-default`。知识卡通过 Excalidraw color map 引用同一手绘母版：修改母版会同步所有引用位置，卡片语义色不会写回母版。
> 规范手绘母版的语义路径统一使用 `1.8` 线宽、圆角端点与圆角连接，并通过 `vector-effect="non-scaling-stroke"` 保持缩放前后的光学线宽；透明边界路径不计入线条规范。统一的是线条渲染规则，原始 SVG 的来源几何、构图与许可信息保持不变。
> 单体 icon 默认只使用一种语义色；多色 icon 拆为可独立着色的组件，默认限制为主色加一个强调色，品牌色作为登记例外。Excalidraw 保存解析后的 HEX；修改 CSS 后在仓库根目录先运行 `npm run palette:check`，确认后运行 `npm run palette:sync`，通过插件同步全部登记画布。
> 可视化博客以暖纸色 `--concept-color-warm-fill` 作为页面底板、`--concept-color-canvas` 作为知识卡画布；链接和可读按钮使用深结构色，品牌青绿主要用于图形、粗线与大号标记。

> [!example] Teal–Paper Semantic 8 配色实例
> - [[Knowledge/Notes/现代架构下的全栈边界|现代架构下的全栈边界]]：八个技术示例 SVG 统一收敛为深冷结构／正向流动色，三个交付孤岛使用冷色边界；人物保持主墨色，思考气泡、三把局部梯子、右侧拼接长梯与 AI 助推使用暖色族，问号使用冲突色。
> - [[全栈程序员的生效前提|全栈程序员的生效前提]]：分仓交接路径／门禁使用暖色族，唯一共享房屋／电梯使用冷色族；两个主墨色工程符号放在手绘开发者伸出的双手之间，人物不再使用 UI 式徽标框。
> - [[Knowledge/Notes/微服务的独立交付边界|微服务的独立交付边界]]：页面绑定路径以暖色和低透明度退居背景，业务能力边界使用深冷轮廓与冷色排线，API／有效连接使用正向流动色，独立发布和断开的 App 线缆分别使用注意色与冲突色。
> - 知识卡统一引用 `-handdrawn.svg` 规范母版并通过 Excalidraw color map 配色；原始 SVG 与手绘母版都保留 `--icon-color`，未固化卡片色值。
> - [[Knowledge/Notes/地图与 IIB 的职责边界|地图与 IIB 的职责边界]]：关系树与过滤器表示地图对关系的提纯；书桌、打开的书、便签、书签与相机共同保留 IIB 中材料的位置、未定问题和恢复点。

> [!important] 标签是检索把手，不是意义定义
> `关键词` 用于找到素材，不规定图标只能表达什么。使用图标时，应先明确核心信息、发散联想并选择视觉框架，再回到本索引寻找可重组的零件；不要从抽象词直接跳到第一个同名图标。

## 字段说明

- **文件**：知识卡直接引用的 `-handdrawn.svg` 规范母版；修改后同步所有引用位置。
- **原始文件**：保留外部来源几何、作者与许可的无后缀 SVG，不直接作为知识卡实例。
- **素材／对象**：来源名称及常用对象名称，便于按“它通常叫什么”检索。
- **去标签观察**：暂时不使用对象名称，只记录可见的形状、方向、距离与结构。
- **动作／关系**：图形能够支持的动作、变化或空间关系。
- **可能读法**：可被激活的解释，不是图标的固定含义。
- **关键词**：兼容全文搜索的检索词汇总，不等同于概念定义。
- **联想／语境**：本项目中已经采用的具体解释；相同图标可以在其他语境中产生新含义。
- **同步引用**：直接链接规范手绘母版的知识卡；这些位置会随母版更新。

<!-- icon-index:start -->

<!-- icon-entry:building-blocks-handdrawn.svg:start -->
## building Blocks

![[building-blocks-handdrawn.svg|180]]

- **文件**：`Knowledge/Assets/Icons/building-blocks-handdrawn.svg`
- **原始文件**：`Knowledge/Assets/Icons/building-blocks.svg`
- **素材／对象**：`积木`, `手`, `building blocks`, `LEGO bricks`
- **去标签观察**：左上方的弧线轮廓把一个带凸点的长方块移向下方两块
- **动作／关系**：`放置`, `堆叠`, `对齐接口`, `拆分`, `重新组合`
- **可能读法**：`模块化`, `有目的的约束`, `逐步构建`, `重混`
- **关键词**：`积木`, `手`, `乐高`, `模块化`, `约束`, `组合`, `重混`, `building blocks`, `LEGO`, `modularity`
- **联想／语境**：[[Knowledge/Notes/乐高式思考|乐高式思考]] · 有目的的约束让想法自由组合
- **来源**：[building Blocks](https://thenounproject.com/icon/building-blocks-7669575/)
- **作者**：ProSymbols · Noun Project
- **许可**：[CC BY 3.0](https://creativecommons.org/licenses/by/3.0/)
- **使用**：[[Knowledge/Notes/乐高式思考|乐高式思考]]
- **同步引用**：[[Knowledge/Notes/乐高式思考|乐高式思考]]；[[Knowledge/Notes/软件交付中的知识流|软件交付中的知识流]]
<!-- icon-entry:building-blocks-handdrawn.svg:end -->

<!-- icon-entry:curtain-handdrawn.svg:start -->
## Curtain

![[curtain-handdrawn.svg|180]]

- **文件**：`Knowledge/Assets/Icons/curtain-handdrawn.svg`
- **原始文件**：`Knowledge/Assets/Icons/curtain.svg`
- **素材／对象**：`窗帘`, `帘布`, `curtain`, `drapery`
- **去标签观察**：左右成对的垂落曲线在中间形成开口，下端分别向两侧收束
- **动作／关系**：`遮挡`, `拉开`, `露出`, `分隔内外`, `框定未知区域`
- **可能读法**：`隐藏`, `未知`, `边界`, `揭示`, `舞台`
- **关键词**：`窗帘`, `帘布`, `遮挡`, `隐藏`, `未知`, `边界`, `揭示`, `curtain`, `drapery`, `window`, `concealment`, `unknown`
- **联想／语境**：[[Knowledge/Notes/归纳推理|归纳推理]] · `A05` · 帘后的重复花纹
- **来源**：[Curtain](https://thenounproject.com/icon/curtain-8430562/)
- **作者**：naomi argi · Noun Project
- **许可**：[CC BY 3.0](https://creativecommons.org/licenses/by/3.0/)
- **处理**：保留原始图形路径；移除下载文件底部署名文字，署名保留于本索引与使用笔记
- **使用**：[[Knowledge/Notes/归纳推理|归纳推理]]（方案 B「预测下一格」）
- **同步引用**：[[Knowledge/Notes/归纳推理|归纳推理]]
<!-- icon-entry:curtain-handdrawn.svg:end -->

<!-- icon-entry:wallpaper-pattern-handdrawn.svg:start -->
## wallpaper pattern

![[wallpaper-pattern-handdrawn.svg|180]]

- **文件**：`Knowledge/Assets/Icons/wallpaper-pattern-handdrawn.svg`
- **原始文件**：`Knowledge/Assets/Icons/wallpaper-pattern.svg`
- **素材／对象**：`墙纸`, `花纹`, `wallpaper pattern`, `seamless pattern`
- **去标签观察**：同一组圆弧单元按行列连续铺开，边缘仍像可以向外延伸
- **动作／关系**：`重复`, `平铺`, `连续`, `裁切`, `延伸下一格`
- **可能读法**：`规律`, `模式`, `证据`, `外推`, `可预测性`
- **关键词**：`墙纸`, `花纹`, `重复`, `规律`, `模式`, `连续`, `外推`, `wallpaper pattern`, `seamless pattern`, `repeat`, `pattern`
- **联想／语境**：[[Knowledge/Notes/归纳推理|归纳推理]] · `A05` · 帘后的重复花纹
- **来源**：[wallpaper pattern](https://thenounproject.com/icon/wallpaper-pattern-2516034/)
- **作者**：Kristina Margaryan · Noun Project
- **许可**：[CC BY 3.0](https://creativecommons.org/licenses/by/3.0/)
- **处理**：保留原始图形路径；移除下载文件底部署名文字，署名保留于本索引与使用笔记
- **使用**：[[Knowledge/Notes/归纳推理|归纳推理]]（方案 B「预测下一格」）
- **同步引用**：[[Knowledge/Notes/归纳推理|归纳推理]]
<!-- icon-entry:wallpaper-pattern-handdrawn.svg:end -->

<!-- icon-entry:role-business-material-symbol-handdrawn.svg:start -->
## Business role · Material Symbol

![[role-business-material-symbol-handdrawn.svg|180]]

- **文件**：`Knowledge/Assets/Icons/role-business-material-symbol-handdrawn.svg`
- **原始文件**：`Knowledge/Assets/Icons/role-business-material-symbol.svg`
- **素材／对象**：`公文包`, `business_center`, `briefcase`
- **去标签观察**：上方短弧连接一个封闭矩形，内部由横线分隔，中央有小方块
- **动作／关系**：`携带`, `容纳`, `承担`, `标记参与身份`
- **可能读法**：`工作`, `业务`, `商业`, `职责`, `参与方`
- **关键词**：`业务`, `商业`, `公文包`, `角色`, `参与方`, `business`, `briefcase`, `role`, `stakeholder`
- **联想／语境**：[[Knowledge/Notes/统一语言|统一语言]] · `A21` · 业务参与方的工具徽标
- **来源**：[business_center · Google Material Symbols](https://github.com/google/material-design-icons/blob/master/symbols/web/business_center/materialsymbolsoutlined/business_center_24px.svg)
- **作者**：Google · Material Symbols
- **许可**：[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0)
- **处理**：保留原始 SVG 路径与视觉风格；在 Excalidraw 中等比缩放为 `28×28`
- **使用**：[[Knowledge/Notes/统一语言|统一语言]]（概念视觉「参与方逐次套准」）
- **同步引用**：[[Knowledge/Notes/全栈能力的知识边界|全栈能力的知识边界]]；[[Knowledge/Notes/现代架构下的全栈边界|现代架构下的全栈边界]]；[[Knowledge/Notes/统一语言|统一语言]]；[[Knowledge/Notes/软件交付中的知识流|软件交付中的知识流]]
<!-- icon-entry:role-business-material-symbol-handdrawn.svg:end -->

<!-- icon-entry:role-product-material-symbol-handdrawn.svg:start -->
## Product role · Material Symbol

![[role-product-material-symbol-handdrawn.svg|180]]

- **文件**：`Knowledge/Assets/Icons/role-product-material-symbol-handdrawn.svg`
- **原始文件**：`Knowledge/Assets/Icons/role-product-material-symbol.svg`
- **素材／对象**：`尺子与笔`, `design_services`, `crossed tools`
- **去标签观察**：两根端头不同的细长形以 X 形交叉，在中心形成连接点
- **动作／关系**：`测量`, `绘制`, `交叉`, `协调工具`
- **可能读法**：`设计`, `产品`, `制作`, `工具`, `参与方`
- **关键词**：`产品`, `设计`, `工具`, `尺子`, `笔`, `角色`, `参与方`, `product`, `design services`, `role`, `stakeholder`
- **联想／语境**：[[Knowledge/Notes/统一语言|统一语言]] · `A21` · 产品参与方的工具徽标
- **来源**：[design_services · Google Material Symbols](https://github.com/google/material-design-icons/blob/master/symbols/web/design_services/materialsymbolsoutlined/design_services_24px.svg)
- **作者**：Google · Material Symbols
- **许可**：[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0)
- **处理**：保留原始 SVG 路径与视觉风格；在 Excalidraw 中等比缩放为 `28×28`
- **使用**：[[Knowledge/Notes/统一语言|统一语言]]（概念视觉「参与方逐次套准」）
- **同步引用**：[[Knowledge/Notes/现代架构下的全栈边界|现代架构下的全栈边界]]；[[Knowledge/Notes/统一语言|统一语言]]
<!-- icon-entry:role-product-material-symbol-handdrawn.svg:end -->

<!-- icon-entry:role-engineering-material-symbol-handdrawn.svg:start -->
## Engineering role · Material Symbol

![[role-engineering-material-symbol-handdrawn.svg|180]]

- **文件**：`Knowledge/Assets/Icons/role-engineering-material-symbol-handdrawn.svg`
- **原始文件**：`Knowledge/Assets/Icons/role-engineering-material-symbol.svg`
- **素材／对象**：`尖括号`, `code symbol`, `angle brackets`
- **去标签观察**：一对尖角从左右朝向中间，中央保留一段空白
- **动作／关系**：`成对`, `包围`, `指向内部`, `标记代码`
- **可能读法**：`工程`, `开发`, `实现`, `代码`, `参与方`
- **关键词**：`工程`, `开发`, `代码`, `尖括号`, `角色`, `参与方`, `engineering`, `development`, `code`, `role`, `stakeholder`
- **联想／语境**：[[Knowledge/Notes/统一语言|统一语言]] · `A21` · 工程参与方的工具徽标；[[全栈程序员的生效前提|全栈程序员的协同前提]] · `A22` · 两名都能修改三层的开发者徽标
- **来源**：[code · Google Material Symbols](https://github.com/google/material-design-icons/blob/master/symbols/web/code/materialsymbolsoutlined/code_24px.svg)
- **作者**：Google · Material Symbols
- **许可**：[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0)
- **处理**：保留原始 SVG 路径与视觉风格；按角色徽标需要在 Excalidraw 中等比缩放为 `24×24` 或 `28×28`
- **使用**：[[Knowledge/Notes/统一语言|统一语言]]（概念视觉「参与方逐次套准」）；[[全栈程序员的生效前提|全栈程序员的协同前提]]（概念视觉「Monorepo 共同所有」）
- **同步引用**：[[Knowledge/Notes/全栈程序员的生效前提|全栈程序员的生效前提]]；[[Knowledge/Notes/现代架构下的全栈边界|现代架构下的全栈边界]]；[[Knowledge/Notes/统一语言|统一语言]]；[[Knowledge/Notes/软件交付中的知识流|软件交付中的知识流]]
<!-- icon-entry:role-engineering-material-symbol-handdrawn.svg:end -->

<!-- icon-entry:role-ai-material-symbol-handdrawn.svg:start -->
## AI role · Material Symbol

![[role-ai-material-symbol-handdrawn.svg|180]]

- **文件**：`Knowledge/Assets/Icons/role-ai-material-symbol-handdrawn.svg`
- **原始文件**：`Knowledge/Assets/Icons/role-ai-material-symbol.svg`
- **素材／对象**：`机器人脸`, `smart_toy`, `robot face`
- **去标签观察**：圆角方形中央排列两点和一横，顶部有短线，左右各有圆形突出
- **动作／关系**：`面对`, `回应`, `作为非人参与者进入场景`
- **可能读法**：`AI`, `机器人`, `智能体`, `自动化`, `参与方`
- **关键词**：`AI`, `人工智能`, `机器人`, `智能体`, `自动化`, `角色`, `参与方`, `smart toy`, `agent`, `role`, `stakeholder`
- **联想／语境**：[[Knowledge/Notes/统一语言|统一语言]] · `A21` · AI 参与方的工具徽标；[[Knowledge/Notes/微服务的独立交付边界|微服务的独立交付边界]] · `A19` · Agent 消费入口
- **来源**：[smart_toy · Google Material Symbols](https://github.com/google/material-design-icons/blob/master/symbols/web/smart_toy/materialsymbolsoutlined/smart_toy_24px.svg)
- **作者**：Google · Material Symbols
- **许可**：[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0)
- **处理**：保留原始 SVG 路径与视觉风格；在 Excalidraw 中等比缩放为 `28×28`
- **使用**：[[Knowledge/Notes/统一语言|统一语言]]（概念视觉「参与方逐次套准」）；[[Knowledge/Notes/微服务的独立交付边界|微服务的独立交付边界]]（最终概念视觉「按页面切的端到端 vs 微服务能力边界」）
- **同步引用**：[[Knowledge/Notes/微服务的独立交付边界|微服务的独立交付边界]]；[[Knowledge/Notes/现代架构下的全栈边界|现代架构下的全栈边界]]；[[Knowledge/Notes/统一语言|统一语言]]；[[Knowledge/Notes/软件交付中的知识流|软件交付中的知识流]]
<!-- icon-entry:role-ai-material-symbol-handdrawn.svg:end -->

<!-- icon-entry:layer-ui-web-material-symbol-handdrawn.svg:start -->
## UI layer · Material Symbol

![[layer-ui-web-material-symbol-handdrawn.svg|180]]

- **文件**：`Knowledge/Assets/Icons/layer-ui-web-material-symbol-handdrawn.svg`
- **原始文件**：`Knowledge/Assets/Icons/layer-ui-web-material-symbol.svg`
- **素材／对象**：`网页框架`, `web`, `browser layout`
- **去标签观察**：横向矩形被一条横线和一条短竖线分成大小不同的区域
- **动作／关系**：`分区`, `展示`, `面向外部`, `作为一层排列`
- **可能读法**：`界面`, `网页`, `前端`, `技术层`, `模块`
- **关键词**：`界面`, `前端`, `网页`, `技术层`, `模块`, `UI`, `frontend`, `web`, `layer`, `module`
- **联想／语境**：[[全栈程序员的生效前提|全栈程序员的协同前提]] · `A02` · 多层建筑中的 UI 层；[[Knowledge/Notes/微服务的独立交付边界|微服务的独立交付边界]] · `A17` · 页面端到端切片中的 UI 层；`A19` · Web 消费入口
- **来源**：[web · Google Material Symbols](https://github.com/google/material-design-icons/blob/master/symbols/web/web/materialsymbolsoutlined/web_24px.svg)
- **作者**：Google · Material Symbols
- **许可**：[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0)
- **处理**：保留原始 SVG 路径与视觉风格；在 Excalidraw 中等比缩放为 `24×24` 或 `28×28`
- **使用**：[[全栈程序员的生效前提|全栈程序员的协同前提]]（概念视觉「Monorepo 共同所有」）；[[Knowledge/Notes/微服务的独立交付边界|微服务的独立交付边界]]（最终概念视觉「按页面切的端到端 vs 微服务能力边界」）
- **同步引用**：[[Knowledge/Notes/LCP 的衡量与优化|LCP 的衡量与优化]]；[[Knowledge/Notes/全栈程序员的生效前提|全栈程序员的生效前提]]；[[Knowledge/Notes/全栈能力的知识边界|全栈能力的知识边界]]；[[Knowledge/Notes/微服务的独立交付边界|微服务的独立交付边界]]；[[Knowledge/Notes/现代架构下的全栈边界|现代架构下的全栈边界]]
<!-- icon-entry:layer-ui-web-material-symbol-handdrawn.svg:end -->

<!-- icon-entry:layer-api-material-symbol-handdrawn.svg:start -->
## API layer · Material Symbol

![[layer-api-material-symbol-handdrawn.svg|180]]

- **文件**：`Knowledge/Assets/Icons/layer-api-material-symbol-handdrawn.svg`
- **原始文件**：`Knowledge/Assets/Icons/layer-api-material-symbol.svg`
- **素材／对象**：`接口符号`, `api`, `four-way interface`
- **去标签观察**：四组折角围绕中心排列，相邻形状彼此咬合并朝向不同方向
- **动作／关系**：`连接`, `交换`, `路由`, `居中协调`, `作为一层排列`
- **可能读法**：`接口`, `API`, `服务`, `后端`, `技术层`, `模块`
- **关键词**：`接口`, `连接`, `交换`, `后端`, `服务`, `技术层`, `模块`, `API`, `backend`, `service`, `layer`, `module`
- **联想／语境**：[[全栈程序员的生效前提|全栈程序员的协同前提]] · `A02` · 多层建筑中的 API 层；[[Knowledge/Notes/微服务的独立交付边界|微服务的独立交付边界]] · `A17` · 页面端到端切片中的 API 层；`A08` · 微服务边界标识
- **来源**：[api · Google Material Symbols](https://github.com/google/material-design-icons/blob/master/symbols/web/api/materialsymbolsoutlined/api_24px.svg)
- **作者**：Google · Material Symbols
- **许可**：[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0)
- **处理**：保留原始 SVG 路径与视觉风格；在 Excalidraw 中等比缩放为 `24×24` 或 `28×28`
- **使用**：[[全栈程序员的生效前提|全栈程序员的协同前提]]（概念视觉「Monorepo 共同所有」）；[[Knowledge/Notes/微服务的独立交付边界|微服务的独立交付边界]]（最终概念视觉「按页面切的端到端 vs 微服务能力边界」）
- **同步引用**：[[Knowledge/Notes/全栈程序员的生效前提|全栈程序员的生效前提]]；[[Knowledge/Notes/全栈能力的知识边界|全栈能力的知识边界]]；[[Knowledge/Notes/微服务的独立交付边界|微服务的独立交付边界]]；[[Knowledge/Notes/现代架构下的全栈边界|现代架构下的全栈边界]]
<!-- icon-entry:layer-api-material-symbol-handdrawn.svg:end -->

<!-- icon-entry:layer-database-material-symbol-handdrawn.svg:start -->
## Database layer · Material Symbol

![[layer-database-material-symbol-handdrawn.svg|180]]

- **文件**：`Knowledge/Assets/Icons/layer-database-material-symbol-handdrawn.svg`
- **原始文件**：`Knowledge/Assets/Icons/layer-database-material-symbol.svg`
- **素材／对象**：`圆柱堆叠`, `database`, `storage cylinder`
- **去标签观察**：三个扁椭圆轮廓上下堆叠，外侧竖线把各层连接成整体
- **动作／关系**：`堆叠`, `容纳`, `存取`, `作为底层承托`
- **可能读法**：`数据库`, `数据`, `存储`, `技术层`, `模块`
- **关键词**：`数据库`, `数据`, `存储`, `堆叠`, `技术层`, `模块`, `database`, `data`, `storage`, `layer`, `module`
- **联想／语境**：[[全栈程序员的生效前提|全栈程序员的协同前提]] · `A02` · 多层建筑中的数据层；[[Knowledge/Notes/微服务的独立交付边界|微服务的独立交付边界]] · `A17` · 页面端到端切片中的数据层
- **来源**：[database · Google Material Symbols](https://github.com/google/material-design-icons/blob/master/symbols/web/database/materialsymbolsoutlined/database_24px.svg)
- **作者**：Google · Material Symbols
- **许可**：[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0)
- **处理**：保留原始 SVG 路径与视觉风格；在 Excalidraw 中等比缩放为 `24×24` 或 `28×28`
- **使用**：[[全栈程序员的生效前提|全栈程序员的协同前提]]（概念视觉「Monorepo 共同所有」）；[[Knowledge/Notes/微服务的独立交付边界|微服务的独立交付边界]]（最终概念视觉「按页面切的端到端 vs 微服务能力边界」）
- **同步引用**：[[Knowledge/Notes/全栈程序员的生效前提|全栈程序员的生效前提]]；[[Knowledge/Notes/全栈能力的知识边界|全栈能力的知识边界]]；[[Knowledge/Notes/微服务的独立交付边界|微服务的独立交付边界]]；[[Knowledge/Notes/现代架构下的全栈边界|现代架构下的全栈边界]]
<!-- icon-entry:layer-database-material-symbol-handdrawn.svg:end -->

<!-- icon-entry:access-lock-material-symbol-handdrawn.svg:start -->
## Access lock · Material Symbol

![[access-lock-material-symbol-handdrawn.svg|180]]

- **文件**：`Knowledge/Assets/Icons/access-lock-material-symbol-handdrawn.svg`
- **原始文件**：`Knowledge/Assets/Icons/access-lock-material-symbol.svg`
- **素材／对象**：`锁`, `门禁`, `lock`, `access control`
- **去标签观察**：上方拱形连接下方封闭方块，方块中央有一个圆点
- **动作／关系**：`关闭`, `打开`, `阻挡`, `放行`, `划分边界`
- **可能读法**：`访问控制`, `等待`, `阻塞`, `交接`, `权限`
- **关键词**：`门禁`, `锁`, `访问控制`, `等待`, `阻塞`, `交接`, `边界`, `access`, `lock`, `waiting`, `blockage`, `handoff`
- **联想／语境**：[[全栈程序员的生效前提|全栈程序员的协同前提]] · `A04` · 跨角色交接处的门禁
- **来源**：[lock · Google Material Symbols](https://github.com/google/material-design-icons/blob/master/symbols/web/lock/materialsymbolsoutlined/lock_24px.svg)
- **作者**：Google · Material Symbols
- **许可**：[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0)
- **处理**：保留原始 SVG 路径与视觉风格；在 Excalidraw 中等比缩放为 `26×26`
- **使用**：[[全栈程序员的生效前提|全栈程序员的协同前提]]（概念视觉「Monorepo 共同所有」）
- **同步引用**：[[Knowledge/Notes/全栈程序员的生效前提|全栈程序员的生效前提]]
<!-- icon-entry:access-lock-material-symbol-handdrawn.svg:end -->

<!-- icon-entry:monorepo-folder-code-material-symbol-handdrawn.svg:start -->
## Monorepo folder · Material Symbol

![[monorepo-folder-code-material-symbol-handdrawn.svg|180]]

- **文件**：`Knowledge/Assets/Icons/monorepo-folder-code-material-symbol-handdrawn.svg`
- **原始文件**：`Knowledge/Assets/Icons/monorepo-folder-code-material-symbol.svg`
- **素材／对象**：`代码文件夹`, `folder_code`, `repository folder`
- **去标签观察**：带折角的开放容器轮廓旁放置一对相向的尖括形
- **动作／关系**：`收纳`, `汇集`, `共享`, `把多层放入同一边界`
- **可能读法**：`代码仓库`, `单体仓库`, `共同所有`, `共享代码`, `跨层`
- **关键词**：`单体仓库`, `代码仓库`, `文件夹`, `共同所有`, `共享代码`, `跨层`, `monorepo`, `repository`, `folder code`, `collective ownership`, `shared code`
- **联想／语境**：[[全栈程序员的生效前提|全栈程序员的协同前提]] · `A21` · 单仓共享代码面
- **来源**：[folder_code · Google Material Symbols](https://github.com/google/material-design-icons/blob/master/symbols/web/folder_code/materialsymbolsoutlined/folder_code_24px.svg)
- **作者**：Google · Material Symbols
- **许可**：[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0)
- **处理**：保留原始 SVG 路径与视觉风格；在 Excalidraw 中等比缩放为 `38×38`
- **使用**：[[全栈程序员的生效前提|全栈程序员的协同前提]]（概念视觉「Monorepo 共同所有」）
- **同步引用**：[[Knowledge/Notes/全栈程序员的生效前提|全栈程序员的生效前提]]
<!-- icon-entry:monorepo-folder-code-material-symbol-handdrawn.svg:end -->

<!-- icon-entry:elevator-material-symbol-handdrawn.svg:start -->
## Elevator · Material Symbol

![[elevator-material-symbol-handdrawn.svg|180]]

- **文件**：`Knowledge/Assets/Icons/elevator-material-symbol-handdrawn.svg`
- **原始文件**：`Knowledge/Assets/Icons/elevator-material-symbol.svg`
- **素材／对象**：`电梯`, `升降厢`, `elevator`, `lift`
- **去标签观察**：竖向圆角矩形内左侧站立一个人形，右侧上下排列两个三角形
- **动作／关系**：`上移`, `下移`, `穿过楼层`, `运送`, `贯通上下`
- **可能读法**：`跨层`, `端到端`, `垂直通道`, `层间协作`
- **关键词**：`电梯`, `升降`, `贯通`, `跨层`, `端到端`, `上下移动`, `elevator`, `cross-layer`, `end-to-end`, `vertical movement`
- **联想／语境**：[[全栈程序员的生效前提|全栈程序员的协同前提]] · `A03` · 贯通电梯
- **来源**：[elevator · Google Material Symbols](https://github.com/google/material-design-icons/blob/master/symbols/web/elevator/materialsymbolsoutlined/elevator_24px.svg)
- **作者**：Google · Material Symbols
- **许可**：[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0)
- **处理**：保留原始 SVG 路径与视觉风格；在 Excalidraw 中等比缩放为 `58×58`
- **使用**：[[全栈程序员的生效前提|全栈程序员的协同前提]]（概念视觉「Monorepo 共同所有」）
- **同步引用**：[[Knowledge/Notes/全栈程序员的生效前提|全栈程序员的生效前提]]；[[Knowledge/Notes/全栈能力的知识边界|全栈能力的知识边界]]
<!-- icon-entry:elevator-material-symbol-handdrawn.svg:end -->

<!-- icon-entry:lcp-finish-flag-material-symbol-handdrawn.svg:start -->
## Finish flag · Material Symbol

![[lcp-finish-flag-material-symbol-handdrawn.svg|180]]

- **文件**：`Knowledge/Assets/Icons/lcp-finish-flag-material-symbol-handdrawn.svg`
- **原始文件**：`Knowledge/Assets/Icons/lcp-finish-flag-material-symbol.svg`
- **素材／对象**：`方格旗`, `终点旗`, `sports_score`, `finish flag`
- **去标签观察**：一根竖杆旁连接多行交错方块，方块沿横向展开并形成清楚的停止标记
- **动作／关系**：`标记时刻`, `穿过界线`, `抵达节点`, `设定测量点`
- **可能读法**：`终点`, `里程碑`, `计时点`, `性能指标时刻`
- **关键词**：`终点`, `旗帜`, `方格旗`, `计时`, `测量点`, `LCP`, `finish`, `flag`, `sports score`, `milestone`
- **联想／语境**：[[Knowledge/Notes/LCP 的衡量与优化|LCP 的衡量与优化]] · `A01` · 最大可见内容抵达 LCP 测量点
- **来源**：[sports_score · Google Material Symbols](https://github.com/google/material-design-icons/blob/master/symbols/web/sports_score/materialsymbolsoutlined/sports_score_24px.svg)
- **作者**：Google · Material Symbols
- **许可**：[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0)
- **处理**：保留原始 SVG 路径与视觉风格；补充来源元数据；在 Excalidraw 中等比缩放为 `29×29`
- **使用**：[[Knowledge/Notes/LCP 的衡量与优化|LCP 的衡量与优化]]（最终概念视觉「视口内最大内容呈现」）
- **同步引用**：[[Knowledge/Notes/LCP 的衡量与优化|LCP 的衡量与优化]]
<!-- icon-entry:lcp-finish-flag-material-symbol-handdrawn.svg:end -->

<!-- icon-entry:lcp-image-material-symbol-handdrawn.svg:start -->
## Image candidate · Material Symbol

![[lcp-image-material-symbol-handdrawn.svg|180]]

- **文件**：`Knowledge/Assets/Icons/lcp-image-material-symbol-handdrawn.svg`
- **原始文件**：`Knowledge/Assets/Icons/lcp-image-material-symbol.svg`
- **素材／对象**：`图片框`, `山景占位符`, `image`, `image placeholder`
- **去标签观察**：封闭矩形内有两段高低不同的折线，折线共同指向矩形底边
- **动作／关系**：`框定画面`, `占据区域`, `标记图像内容`, `作为候选进入视口`
- **可能读法**：`图片`, `视觉内容`, `媒体块`, `可见内容候选`
- **关键词**：`图片`, `图像`, `媒体`, `候选内容`, `视口`, `LCP`, `image`, `picture`, `media`, `candidate`
- **联想／语境**：[[Knowledge/Notes/LCP 的衡量与优化|LCP 的衡量与优化]] · `A10` · 图像可以成为最大可见内容，也可以只是后续出现的小内容块
- **来源**：[image · Google Material Symbols](https://github.com/google/material-design-icons/blob/master/symbols/web/image/materialsymbolsoutlined/image_24px.svg)
- **作者**：Google · Material Symbols
- **许可**：[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0)
- **处理**：保留原始 SVG 路径与视觉风格；补充来源元数据；在 Excalidraw 中等比缩放为 `25×25` 或 `18×18`
- **使用**：[[Knowledge/Notes/LCP 的衡量与优化|LCP 的衡量与优化]]（最终概念视觉「视口内最大内容呈现」）
- **同步引用**：[[Knowledge/Notes/LCP 的衡量与优化|LCP 的衡量与优化]]
<!-- icon-entry:lcp-image-material-symbol-handdrawn.svg:end -->

<!-- icon-entry:lcp-text-material-symbol-handdrawn.svg:start -->
## Text candidate · Material Symbol

![[lcp-text-material-symbol-handdrawn.svg|180]]

- **文件**：`Knowledge/Assets/Icons/lcp-text-material-symbol-handdrawn.svg`
- **原始文件**：`Knowledge/Assets/Icons/lcp-text-material-symbol.svg`
- **素材／对象**：`大小写字形`, `文本字段`, `text_fields`, `text symbol`
- **去标签观察**：一大一小两组横竖笔画并排，每组都由横线支撑中央竖线
- **动作／关系**：`标记文字`, `占据区域`, `形成文本块`, `作为候选进入视口`
- **可能读法**：`文本`, `标题`, `文字内容`, `可见内容候选`
- **关键词**：`文本`, `文字`, `标题`, `文本块`, `候选内容`, `视口`, `LCP`, `text`, `text fields`, `typography`, `candidate`
- **联想／语境**：[[Knowledge/Notes/LCP 的衡量与优化|LCP 的衡量与优化]] · `A10` · 文本同样可以成为最大可见内容
- **来源**：[text_fields · Google Material Symbols](https://github.com/google/material-design-icons/blob/master/symbols/web/text_fields/materialsymbolsoutlined/text_fields_24px.svg)
- **作者**：Google · Material Symbols
- **许可**：[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0)
- **处理**：保留原始 SVG 路径与视觉风格；补充来源元数据；在 Excalidraw 中等比缩放为 `25×25`
- **使用**：[[Knowledge/Notes/LCP 的衡量与优化|LCP 的衡量与优化]]（最终概念视觉「视口内最大内容呈现」）
- **同步引用**：[[Knowledge/Notes/LCP 的衡量与优化|LCP 的衡量与优化]]
<!-- icon-entry:lcp-text-material-symbol-handdrawn.svg:end -->


<!-- icon-entry:electrical-services-material-symbol-handdrawn.svg:start -->
## Electrical services · Material Symbol

![[electrical-services-material-symbol-handdrawn.svg|180]]

- **文件**：`Knowledge/Assets/Icons/electrical-services-material-symbol-handdrawn.svg`
- **原始文件**：`Knowledge/Assets/Icons/electrical-services-material-symbol.svg`
- **素材／对象**：`电源插头`, `electrical_services`, `plug and cable`
- **去标签观察**：一条弯曲线从左侧延伸到右侧方块，方块一端伸出两根平行短条
- **动作／关系**：`连接`, `插入`, `拔出`, `接通`, `通过标准接点交换`
- **可能读法**：`插头`, `接口`, `稳定接点`, `可替换连接`, `API`
- **关键词**：`插头`, `电源线`, `连接`, `接口`, `接点`, `API`, `plug`, `electrical services`, `connection`, `interface`
- **联想／语境**：[[Knowledge/Notes/微服务的独立交付边界|微服务的独立交付边界]] · `A01` · 微服务 API 的稳定接点；`A20` · 拔掉一个消费入口后，能力边界仍保持连接与发布
- **来源**：[electrical_services · Google Material Symbols](https://github.com/google/material-design-icons/blob/master/symbols/web/electrical_services/materialsymbolsoutlined/electrical_services_24px.svg)
- **作者**：Google · Material Symbols
- **许可**：[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0)
- **处理**：保留原始 SVG 路径与视觉风格；在 Excalidraw 中等比缩放为 `38×38` 或 `42×42`
- **使用**：[[Knowledge/Notes/微服务的独立交付边界|微服务的独立交付边界]]（最终概念视觉「按页面切的端到端 vs 微服务能力边界」）
- **同步引用**：[[Knowledge/Notes/微服务的独立交付边界|微服务的独立交付边界]]；[[Knowledge/Notes/现代架构下的全栈边界|现代架构下的全栈边界]]
<!-- icon-entry:electrical-services-material-symbol-handdrawn.svg:end -->

<!-- icon-entry:product-inventory-material-symbol-handdrawn.svg:start -->
## Product inventory · Material Symbol

![[product-inventory-material-symbol-handdrawn.svg|180]]

- **文件**：`Knowledge/Assets/Icons/product-inventory-material-symbol-handdrawn.svg`
- **原始文件**：`Knowledge/Assets/Icons/product-inventory-material-symbol.svg`
- **素材／对象**：`商品箱`, `库存箱`, `inventory_2`, `inventory container`
- **去标签观察**：一个竖向封闭矩形被顶部横条分区，中间另有一条短横线
- **动作／关系**：`容纳`, `封装`, `归档`, `标记商品单元`, `作为能力块排列`
- **可能读法**：`商品`, `库存`, `封装单元`, `业务能力`, `服务模块`
- **关键词**：`商品`, `库存`, `货品`, `封装`, `业务能力`, `微服务`, `product`, `inventory`, `container`, `capability`
- **联想／语境**：[[Knowledge/Notes/微服务的独立交付边界|微服务的独立交付边界]] · `A16` · 商品业务能力单元
- **来源**：[inventory_2 · Google Material Symbols](https://github.com/google/material-design-icons/blob/master/symbols/web/inventory_2/materialsymbolsoutlined/inventory_2_24px.svg)
- **作者**：Google · Material Symbols
- **许可**：[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0)
- **处理**：保留原始 SVG 路径与视觉风格；在 Excalidraw 中等比缩放为 `25×25`
- **使用**：[[Knowledge/Notes/微服务的独立交付边界|微服务的独立交付边界]]（最终概念视觉「按页面切的端到端 vs 微服务能力边界」）
- **同步引用**：[[Knowledge/Notes/全栈能力的知识边界|全栈能力的知识边界]]；[[Knowledge/Notes/微服务的独立交付边界|微服务的独立交付边界]]
<!-- icon-entry:product-inventory-material-symbol-handdrawn.svg:end -->

<!-- icon-entry:price-sell-material-symbol-handdrawn.svg:start -->
## Price tag · Material Symbol

![[price-sell-material-symbol-handdrawn.svg|180]]

- **文件**：`Knowledge/Assets/Icons/price-sell-material-symbol-handdrawn.svg`
- **原始文件**：`Knowledge/Assets/Icons/price-sell-material-symbol.svg`
- **素材／对象**：`价格标签`, `sell`, `price tag`
- **去标签观察**：一个斜放的五边形轮廓在尖端附近留有圆孔，整体朝右下方延伸
- **动作／关系**：`附着`, `标价`, `关联数值`, `跟随对象移动`
- **可能读法**：`价格`, `售价`, `标签`, `商业属性`, `业务能力`
- **关键词**：`价格`, `售价`, `标签`, `标价`, `业务能力`, `price`, `sell`, `tag`, `pricing`, `capability`
- **联想／语境**：[[Knowledge/Notes/微服务的独立交付边界|微服务的独立交付边界]] · `A16` · 价格业务能力单元
- **来源**：[sell · Google Material Symbols](https://github.com/google/material-design-icons/blob/master/symbols/web/sell/materialsymbolsoutlined/sell_24px.svg)
- **作者**：Google · Material Symbols
- **许可**：[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0)
- **处理**：保留原始 SVG 路径与视觉风格；在 Excalidraw 中等比缩放为 `25×25`
- **使用**：[[Knowledge/Notes/微服务的独立交付边界|微服务的独立交付边界]]（最终概念视觉「按页面切的端到端 vs 微服务能力边界」）
- **同步引用**：[[Knowledge/Notes/全栈能力的知识边界|全栈能力的知识边界]]；[[Knowledge/Notes/微服务的独立交付边界|微服务的独立交付边界]]
<!-- icon-entry:price-sell-material-symbol-handdrawn.svg:end -->

<!-- icon-entry:availability-fact-check-material-symbol-handdrawn.svg:start -->
## Availability check · Material Symbol

![[availability-fact-check-material-symbol-handdrawn.svg|180]]

- **文件**：`Knowledge/Assets/Icons/availability-fact-check-material-symbol-handdrawn.svg`
- **原始文件**：`Knowledge/Assets/Icons/availability-fact-check-material-symbol.svg`
- **素材／对象**：`核对清单`, `fact_check`, `checklist with check mark`
- **去标签观察**：封闭矩形左侧排列三条短横线，右侧由两段折线组成一个勾形
- **动作／关系**：`核对`, `确认`, `列举条件`, `标记通过状态`
- **可能读法**：`可售`, `校验`, `事实核查`, `状态确认`, `业务规则`
- **关键词**：`可售`, `库存状态`, `校验`, `确认`, `清单`, `业务规则`, `availability`, `fact check`, `checklist`, `validation`
- **联想／语境**：[[Knowledge/Notes/微服务的独立交付边界|微服务的独立交付边界]] · `A16` · 可售状态业务能力单元
- **来源**：[fact_check · Google Material Symbols](https://github.com/google/material-design-icons/blob/master/symbols/web/fact_check/materialsymbolsoutlined/fact_check_24px.svg)
- **作者**：Google · Material Symbols
- **许可**：[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0)
- **处理**：保留原始 SVG 路径与视觉风格；在 Excalidraw 中等比缩放为 `25×25`
- **使用**：[[Knowledge/Notes/微服务的独立交付边界|微服务的独立交付边界]]（最终概念视觉「按页面切的端到端 vs 微服务能力边界」）
- **同步引用**：[[Knowledge/Notes/全栈能力的知识边界|全栈能力的知识边界]]；[[Knowledge/Notes/微服务的独立交付边界|微服务的独立交付边界]]；[[Knowledge/Notes/软件交付中的知识流|软件交付中的知识流]]
<!-- icon-entry:availability-fact-check-material-symbol-handdrawn.svg:end -->

<!-- icon-entry:smartphone-material-symbol-handdrawn.svg:start -->
## Smartphone · Material Symbol

![[smartphone-material-symbol-handdrawn.svg|180]]

- **文件**：`Knowledge/Assets/Icons/smartphone-material-symbol-handdrawn.svg`
- **原始文件**：`Knowledge/Assets/Icons/smartphone-material-symbol.svg`
- **素材／对象**：`智能手机`, `smartphone`, `mobile device`
- **去标签观察**：一个高而窄的圆角矩形由顶部、中央和底部三个横向区域组成
- **动作／关系**：`承载界面`, `作为入口`, `移动使用`, `连接服务`
- **可能读法**：`App`, `移动端`, `渠道`, `消费者`, `用户入口`
- **关键词**：`手机`, `移动端`, `App`, `应用`, `渠道`, `消费者`, `smartphone`, `mobile`, `application`, `consumer`
- **联想／语境**：[[Knowledge/Notes/微服务的独立交付边界|微服务的独立交付边界]] · `A19` · 可替换的 App 消费入口；`A20` · 被主动拔开、用来测试能力独立性的前台
- **来源**：[smartphone · Google Material Symbols](https://github.com/google/material-design-icons/blob/master/symbols/web/smartphone/materialsymbolsoutlined/smartphone_24px.svg)
- **作者**：Google · Material Symbols
- **许可**：[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0)
- **处理**：保留原始 SVG 路径与视觉风格；在 Excalidraw 中等比缩放为 `20×20`
- **使用**：[[Knowledge/Notes/微服务的独立交付边界|微服务的独立交付边界]]（最终概念视觉「按页面切的端到端 vs 微服务能力边界」）
- **同步引用**：[[Knowledge/Notes/微服务的独立交付边界|微服务的独立交付边界]]
<!-- icon-entry:smartphone-material-symbol-handdrawn.svg:end -->

<!-- icon-entry:confused-programmer-shrug-nounproject-handdrawn.svg:start -->
## Shrug person

![[confused-programmer-shrug-nounproject-handdrawn.svg|180]]

- **文件**：`Knowledge/Assets/Icons/confused-programmer-shrug-nounproject-handdrawn.svg`
- **原始文件**：`Knowledge/Assets/Icons/confused-programmer-shrug-nounproject.svg`
- **素材／对象**：`摊手人物`, `摊手的人`, `shrug`, `shrugging person`
- **去标签观察**：空白圆形头部连接开放的躯干线条，两侧手臂弯曲并向外抬起，手掌朝上，头部与手腕附近保留短虚线细节
- **动作／关系**：`摊手`, `左右权衡`, `面对多个选择`, `停在决定之前`
- **可能读法**：`不知道`, `无可奈何`, `不确定`, `左右为难`, `开放问题`
- **关键词**：`摊手`, `人物`, `双手`, `无奈`, `不知道`, `选择`, `权衡`, `shrug`, `person`, `uncertain`, `choice`
- **联想／语境**：[[Knowledge/Notes/现代架构下的全栈边界|现代架构下的全栈边界]] · `A22` · 摊手动作承载“范围没有自然落点”；`DEV` 徽标与困惑表情均在知识卡画布中作为独立元素组合
- **来源**：[Shrug #1763239](https://thenounproject.com/icon/shrug-1763239/) · Noun Project
- **作者**：Sarah Rudkin
- **许可**：[CC BY 3.0](https://creativecommons.org/licenses/by/3.0/)
- **处理**：原始文件由来源页官方 `512 px` PNG 预览使用 VTracer 0.6.15 描摹为 SVG，并裁切到可见边界；规范手绘母版再从该轮廓自动提取中心线，经 Excalidraw `roughness: 2` 转为统一单线手绘笔触，保留原图姿势与比例，同时避免把原来的粗线描成双重边界。颜色由 `--icon-color` 控制，不在母版中拼入其他图标
- **使用**：[[Knowledge/Notes/现代架构下的全栈边界|现代架构下的全栈边界]]（作为摊手人物，与困惑表情在画布内组合）
- **同步引用**：[[Knowledge/Notes/现代架构下的全栈边界|现代架构下的全栈边界]]
<!-- icon-entry:confused-programmer-shrug-nounproject-handdrawn.svg:end -->

<!-- icon-entry:confused-face-mood-puzzled-tabler-handdrawn.svg:start -->
## Mood Puzzled

![[confused-face-mood-puzzled-tabler-handdrawn.svg|180]]

- **文件**：`Knowledge/Assets/Icons/confused-face-mood-puzzled-tabler-handdrawn.svg`
- **原始文件**：`Knowledge/Assets/Icons/confused-face-mood-puzzled-tabler.svg`
- **素材／对象**：`困惑表情`, `疑惑头像`, `puzzled face`, `confused expression`
- **去标签观察**：近乎闭合的圆形头像在右上留出缺口，两只点状眼睛高低不一，嘴线向一侧倾斜，缺口外接一个问号形短线
- **动作／关系**：`提出疑问`, `犹豫`, `无法判断`, `停在答案之前`
- **可能读法**：`困惑`, `想不通`, `不确定`, `对边界产生疑问`
- **关键词**：`头像`, `表情`, `困惑`, `疑惑`, `问号`, `斜嘴`, `不确定`, `face`, `expression`, `puzzled`, `confused`, `question`, `uncertain`, `mood`
- **联想／语境**：[[Knowledge/Notes/现代架构下的全栈边界|现代架构下的全栈边界]] · `A24` · 在知识卡画布中与摊手人物叠加，激活对“全栈”边界的疑问
- **来源**：[Mood Puzzled · Tabler Icons](https://tabler.io/icons?icon=mood-puzzled) · [官方 SVG](https://github.com/tabler/tabler-icons/blob/main/icons/outline/mood-puzzled.svg)
- **作者**：Paweł Kuna／Tabler Icons
- **许可**：[MIT License](https://github.com/tabler/tabler-icons/blob/main/LICENSE)
- **处理**：保留 Tabler 官方 SVG 的原始中心线路径，规范母版使用单层普通线条，不叠加、偏移或组合第二笔触；在词库 `140` 单元预览下，以 `2.3` 非缩放线宽对齐 22 号图标的实际视觉粗细，并保留圆角端点与圆角连接。素材文件保留完整 MIT 许可与来源元数据，线条颜色由 `--icon-color` 控制；与其他图标的组合只发生在使用它的知识卡画布中
- **使用**：[[Knowledge/Notes/现代架构下的全栈边界|现代架构下的全栈边界]]（与摊手人物在画布内组合成困惑角色）
- **同步引用**：[[Knowledge/Notes/现代架构下的全栈边界|现代架构下的全栈边界]]
<!-- icon-entry:confused-face-mood-puzzled-tabler-handdrawn.svg:end -->

<!-- icon-entry:account-tree-material-symbol-handdrawn.svg:start -->
## Relationship tree · Material Symbol

![[account-tree-material-symbol-handdrawn.svg|180]]

- **文件**：`Knowledge/Assets/Icons/account-tree-material-symbol-handdrawn.svg`
- **原始文件**：`Knowledge/Assets/Icons/account-tree-material-symbol.svg`
- **素材／对象**：`关系树`, `层级图`, `account_tree`, `hierarchy diagram`
- **去标签观察**：三个空心方块由水平与垂直折线连接，中央主干向上下两个端点分叉
- **动作／关系**：`连接`, `分叉`, `建立层级`, `显示路径`, `压缩为少量节点`
- **可能读法**：`关系地图`, `目录`, `层级`, `拓扑`, `稳定结构`
- **关键词**：`关系树`, `层级图`, `目录`, `节点`, `分支`, `知识地图`, `account tree`, `hierarchy`, `relationship map`, `structure`
- **联想／语境**：[[Knowledge/Notes/地图与 IIB 的职责边界|地图与 IIB 的职责边界]] · `A04` · 提纯后的关系目录
- **来源**：[account_tree · Google Material Symbols](https://github.com/google/material-design-icons/blob/master/symbols/web/account_tree/materialsymbolsoutlined/account_tree_24px.svg)
- **作者**：Google · Material Symbols
- **许可**：[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0)
- **处理**：保留官方 SVG 路径与视觉风格；颜色由 `--icon-color` 控制；在 Excalidraw 中等比缩放为 `88×88`
- **使用**：[[Knowledge/Notes/地图与 IIB 的职责边界|地图与 IIB 的职责边界]]（最终概念视觉「一桌，两种保存」）
- **同步引用**：[[Knowledge/Notes/地图与 IIB 的职责边界|地图与 IIB 的职责边界]]
<!-- icon-entry:account-tree-material-symbol-handdrawn.svg:end -->

<!-- icon-entry:filter-alt-material-symbol-handdrawn.svg:start -->
## Filter · Material Symbol

![[filter-alt-material-symbol-handdrawn.svg|180]]

- **文件**：`Knowledge/Assets/Icons/filter-alt-material-symbol-handdrawn.svg`
- **原始文件**：`Knowledge/Assets/Icons/filter-alt-material-symbol.svg`
- **素材／对象**：`漏斗`, `过滤器`, `filter_alt`, `filter funnel`
- **去标签观察**：宽阔的上边缘向中央逐步收窄，底部延伸出一段短而窄的出口
- **动作／关系**：`筛选`, `收窄`, `去除噪声`, `让少量内容通过`, `从多到少`
- **可能读法**：`过滤`, `提纯`, `选择`, `降噪`, `形成稳定结构`
- **关键词**：`漏斗`, `过滤器`, `筛选`, `提纯`, `选择`, `降噪`, `filter`, `funnel`, `distill`, `selection`, `noise reduction`
- **联想／语境**：[[Knowledge/Notes/地图与 IIB 的职责边界|地图与 IIB 的职责边界]] · `A15` · 从散落材料中筛出少量稳定关系
- **来源**：[filter_alt · Google Material Symbols](https://github.com/google/material-design-icons/blob/master/symbols/web/filter_alt/materialsymbolsoutlined/filter_alt_24px.svg)
- **作者**：Google · Material Symbols
- **许可**：[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0)
- **处理**：保留官方 SVG 路径与视觉风格；颜色由 `--icon-color` 控制；在 Excalidraw 中等比缩放为 `60×60`
- **使用**：[[Knowledge/Notes/地图与 IIB 的职责边界|地图与 IIB 的职责边界]]（最终概念视觉「一桌，两种保存」）
- **同步引用**：[[Knowledge/Notes/地图与 IIB 的职责边界|地图与 IIB 的职责边界]]
<!-- icon-entry:filter-alt-material-symbol-handdrawn.svg:end -->

<!-- icon-entry:desk-material-symbol-handdrawn.svg:start -->
## Desk · Material Symbol

![[desk-material-symbol-handdrawn.svg|180]]

- **文件**：`Knowledge/Assets/Icons/desk-material-symbol-handdrawn.svg`
- **原始文件**：`Knowledge/Assets/Icons/desk-material-symbol.svg`
- **素材／对象**：`书桌`, `工作台`, `desk`, `work table`
- **去标签观察**：宽矩形台面由两侧竖线支撑，右侧被两条横线切分为上下收纳区
- **动作／关系**：`承托`, `摊开材料`, `保留位置`, `形成工作表面`, `容纳进行中的组合`
- **可能读法**：`研究现场`, `工作台`, `当前任务`, `尚未收拾的上下文`
- **关键词**：`书桌`, `工作台`, `研究桌`, `工作现场`, `材料位置`, `上下文`, `desk`, `work table`, `workspace`, `research desk`
- **联想／语境**：[[Knowledge/Notes/地图与 IIB 的职责边界|地图与 IIB 的职责边界]] · `A04` · 尚未收桌的研究现场
- **来源**：[desk · Google Material Symbols](https://github.com/google/material-design-icons/blob/master/symbols/web/desk/materialsymbolsoutlined/desk_24px.svg)
- **作者**：Google · Material Symbols
- **许可**：[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0)
- **处理**：保留官方 SVG 路径与视觉风格；颜色由 `--icon-color` 控制；在 Excalidraw 中等比缩放为 `42×42` 或 `70×70`
- **使用**：[[Knowledge/Notes/地图与 IIB 的职责边界|地图与 IIB 的职责边界]]（最终概念视觉「一桌，两种保存」）
- **同步引用**：[[Knowledge/Notes/地图与 IIB 的职责边界|地图与 IIB 的职责边界]]
<!-- icon-entry:desk-material-symbol-handdrawn.svg:end -->

<!-- icon-entry:menu-book-material-symbol-handdrawn.svg:start -->
## Open book · Material Symbol

![[menu-book-material-symbol-handdrawn.svg|180]]

- **文件**：`Knowledge/Assets/Icons/menu-book-material-symbol-handdrawn.svg`
- **原始文件**：`Knowledge/Assets/Icons/menu-book-material-symbol.svg`
- **素材／对象**：`打开的书`, `阅读材料`, `menu_book`, `open book`
- **去标签观察**：左右两组弧形页面围绕中央书脊展开，页面内排列多条短横线
- **动作／关系**：`打开`, `阅读`, `并置来源`, `停留在当前页`, `继续查阅`
- **可能读法**：`来源`, `正在阅读`, `工作材料`, `未完成的研究上下文`
- **关键词**：`打开的书`, `阅读`, `来源`, `当前页`, `研究材料`, `书本`, `menu book`, `open book`, `source`, `reading context`
- **联想／语境**：[[Knowledge/Notes/地图与 IIB 的职责边界|地图与 IIB 的职责边界]] · `A04` · 研究桌上仍打开的来源
- **来源**：[menu_book · Google Material Symbols](https://github.com/google/material-design-icons/blob/master/symbols/web/menu_book/materialsymbolsoutlined/menu_book_24px.svg)
- **作者**：Google · Material Symbols
- **许可**：[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0)
- **处理**：保留官方 SVG 路径与视觉风格；颜色由 `--icon-color` 控制；在 Excalidraw 中等比缩放为 `88×88`
- **使用**：[[Knowledge/Notes/地图与 IIB 的职责边界|地图与 IIB 的职责边界]]（最终概念视觉「一桌，两种保存」）
- **同步引用**：[[Knowledge/Notes/地图与 IIB 的职责边界|地图与 IIB 的职责边界]]
<!-- icon-entry:menu-book-material-symbol-handdrawn.svg:end -->

<!-- icon-entry:sticky-note-material-symbol-handdrawn.svg:start -->
## Sticky note · Material Symbol

![[sticky-note-material-symbol-handdrawn.svg|180]]

- **文件**：`Knowledge/Assets/Icons/sticky-note-material-symbol-handdrawn.svg`
- **原始文件**：`Knowledge/Assets/Icons/sticky-note-material-symbol.svg`
- **素材／对象**：`便签`, `折角纸片`, `sticky_note_2`, `sticky note`
- **去标签观察**：一个方形轮廓在右下角向内折起，内部保留两条长短不同的横线
- **动作／关系**：`记录`, `移动`, `重新摆放`, `贴近其他材料`, `保留临时状态`
- **可能读法**：`问题`, `假设`, `线索`, `下一步`, `尚未稳定的想法`
- **关键词**：`便签`, `折角纸`, `问题`, `假设`, `线索`, `下一步`, `临时材料`, `sticky note`, `note`, `question`, `hypothesis`, `clue`
- **联想／语境**：[[Knowledge/Notes/地图与 IIB 的职责边界|地图与 IIB 的职责边界]] · `A04` · 散落在研究桌上的临时材料
- **来源**：[sticky_note_2 · Google Material Symbols](https://github.com/google/material-design-icons/blob/master/symbols/web/sticky_note_2/materialsymbolsoutlined/sticky_note_2_24px.svg)
- **作者**：Google · Material Symbols
- **许可**：[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0)
- **处理**：保留官方 SVG 路径与视觉风格；颜色由 `--icon-color` 控制；在 Excalidraw 中等比缩放为 `52×52` 至 `60×60`，以轻微角度差保留散落感
- **使用**：[[Knowledge/Notes/地图与 IIB 的职责边界|地图与 IIB 的职责边界]]（最终概念视觉「一桌，两种保存」）
- **同步引用**：[[Knowledge/Notes/地图与 IIB 的职责边界|地图与 IIB 的职责边界]]；[[Knowledge/Notes/软件交付中的知识流|软件交付中的知识流]]
<!-- icon-entry:sticky-note-material-symbol-handdrawn.svg:end -->

<!-- icon-entry:bookmark-material-symbol-handdrawn.svg:start -->
## Bookmark · Material Symbol

![[bookmark-material-symbol-handdrawn.svg|180]]

- **文件**：`Knowledge/Assets/Icons/bookmark-material-symbol-handdrawn.svg`
- **原始文件**：`Knowledge/Assets/Icons/bookmark-material-symbol.svg`
- **素材／对象**：`书签`, `页签`, `bookmark`, `page marker`
- **去标签观察**：竖向长方形向下延伸，底边由两条斜线向中央汇成内凹尖口
- **动作／关系**：`标记位置`, `暂停`, `返回`, `从原处继续`, `保存断点`
- **可能读法**：`保存点`, `恢复点`, `当前页`, `中断位置`, `继续思考`
- **关键词**：`书签`, `页签`, `保存点`, `恢复点`, `断点`, `继续`, `bookmark`, `page marker`, `save point`, `resume`, `checkpoint`
- **联想／语境**：[[Knowledge/Notes/地图与 IIB 的职责边界|地图与 IIB 的职责边界]] · `A18` · 从中断位置重新进入思考
- **来源**：[bookmark · Google Material Symbols](https://github.com/google/material-design-icons/blob/master/symbols/web/bookmark/materialsymbolsoutlined/bookmark_24px.svg)
- **作者**：Google · Material Symbols
- **许可**：[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0)
- **处理**：保留官方 SVG 路径与视觉风格；颜色由 `--icon-color` 控制；在 Excalidraw 中等比缩放为 `36×36`
- **使用**：[[Knowledge/Notes/地图与 IIB 的职责边界|地图与 IIB 的职责边界]]（最终概念视觉「一桌，两种保存」）
- **同步引用**：[[Knowledge/Notes/地图与 IIB 的职责边界|地图与 IIB 的职责边界]]
<!-- icon-entry:bookmark-material-symbol-handdrawn.svg:end -->

<!-- icon-entry:photo-camera-material-symbol-handdrawn.svg:start -->
## Camera · Material Symbol

![[photo-camera-material-symbol-handdrawn.svg|180]]

- **文件**：`Knowledge/Assets/Icons/photo-camera-material-symbol-handdrawn.svg`
- **原始文件**：`Knowledge/Assets/Icons/photo-camera-material-symbol.svg`
- **素材／对象**：`相机`, `镜头`, `photo_camera`, `camera`
- **去标签观察**：横向机身中央嵌入同心圆，顶部凸起的小矩形与机身相连
- **动作／关系**：`拍摄`, `冻结瞬间`, `记录布局`, `保存状态`, `生成快照`
- **可能读法**：`现场快照`, `状态保存`, `连续记录`, `可恢复的工作语境`
- **关键词**：`相机`, `快照`, `拍摄`, `状态保存`, `布局`, `现场`, `photo camera`, `snapshot`, `capture`, `state`, `context preservation`
- **联想／语境**：[[Knowledge/Notes/地图与 IIB 的职责边界|地图与 IIB 的职责边界]] · `A15` · 连续快照保留变化中的思考现场
- **来源**：[photo_camera · Google Material Symbols](https://github.com/google/material-design-icons/blob/master/symbols/web/photo_camera/materialsymbolsoutlined/photo_camera_24px.svg)
- **作者**：Google · Material Symbols
- **许可**：[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0)
- **处理**：保留官方 SVG 路径与视觉风格；颜色由 `--icon-color` 控制；在 Excalidraw 中等比缩放为 `32×32`
- **使用**：[[Knowledge/Notes/地图与 IIB 的职责边界|地图与 IIB 的职责边界]]（最终概念视觉「一桌，两种保存」）
- **同步引用**：[[Knowledge/Notes/地图与 IIB 的职责边界|地图与 IIB 的职责边界]]；[[Knowledge/Notes/软件交付中的知识流|软件交付中的知识流]]
<!-- icon-entry:photo-camera-material-symbol-handdrawn.svg:end -->

<!-- icon-entry:ladder-tabler-handdrawn.svg:start -->
## Ladder

![[ladder-tabler-handdrawn.svg|180]]

- **文件**：`Knowledge/Assets/Icons/ladder-tabler-handdrawn.svg`
- **原始文件**：`Knowledge/Assets/Icons/ladder-tabler.svg`
- **素材／对象**：`梯子`, `竖梯`, `ladder`, `climbing equipment`
- **去标签观察**：两条平行竖线由四条等距横档连接，顶部与底部均保持开放
- **动作／关系**：`攀爬`, `逐级上移`, `跨越高度`, `分段重复`, `上下拼接`
- **可能读法**：`技术栈`, `能力层级`, `可达范围`, `局部全栈`, `贯穿范围`
- **关键词**：`梯子`, `竖梯`, `横档`, `攀登`, `层级`, `技术栈`, `局部范围`, `拼接`, `可达范围`, `ladder`, `climb`, `stack`, `tier`, `range`
- **联想／语境**：[[Knowledge/Notes/现代架构下的全栈边界|现代架构下的全栈边界]] · `A25` · 三把独立短梯表示各交付边界内的局部“全栈”，右侧由相同小梯上下拼接出的长梯表示贯穿整条系统链路的另一种尺度
- **来源**：[Ladder · Tabler Icons](https://tabler.io/icons?icon=ladder) · [官方 SVG](https://github.com/tabler/tabler-icons/blob/main/icons/outline/ladder.svg)
- **作者**：Paweł Kuna／Tabler Icons
- **许可**：[MIT License](https://github.com/tabler/tabler-icons/blob/main/LICENSE)
- **处理**：保留 Tabler 官方 SVG 的两条竖轨与四条横档及其相对间距，每条来源中心线各转换为一个 Excalidraw `roughness: 2` 线元素；导出的路径保留自然双笔触抖动，不增加新的语义零件。可见路径统一使用词库标准 `1.8` 非缩放线宽、圆角端点与圆角连接，颜色由 `--icon-color` 控制；卡片中的长梯只由多个相同母版实例上下拼接，不改写母版几何
- **使用**：[[Knowledge/Notes/现代架构下的全栈边界|现代架构下的全栈边界]]（三把局部短梯与一把模块化长梯）
- **同步引用**：[[Knowledge/Notes/现代架构下的全栈边界|现代架构下的全栈边界]]
<!-- icon-entry:ladder-tabler-handdrawn.svg:end -->

<!-- icon-index:end -->

# Excalidraw Data

## Text Elements
Icon Library ^I075YkSy

01 ^S4e68YFy

building Blocks ^o3WkwQ8o

模块化 · 约束 · 重混 ^rq7bLKDl

Noun Project · #7669575 ^AaTrUT8s

02 ^ykwI3Poy

Curtain ^ail4Z1w2

遮挡 · 未知 · 揭示 ^vR4PL4f2

Noun Project · #8430562 ^meCD5tKo

03 ^B1WUyKKb

wallpaper pattern ^dqXstFxV

重复 · 规律 · 外推 ^t3AKxc1H

Noun Project · #2516034 ^tMSKSTkJ

04 ^xTX7GQOK

Business role ^JGEJsB4Q

业务 · 决策 · 参与方 ^B9CBflXs

Google · Material Symbols ^0Fc2qiVT

05 ^EQgdrOKZ

Product role ^gjc852cC

产品 · 设计 · 参与方 ^FYgQrEAS

Google · Material Symbols ^j2NSSQhz

06 ^wcCA8a1s

Engineering role ^HoeEHMff

工程 · 代码 · 参与方 ^CeLOX01k

Google · Material Symbols ^EqxuLq8F

07 ^cEMBq7Q0

AI role ^koA9e3pc

AI · 智能体 · 参与方 ^wAvpxAm4

Google · Material Symbols ^bynIhjUa

08 ^zzEFrEwk

UI layer ^cMcNBWb4

界面 · 前端 · 技术层 ^X81wOoso

Google · Material Symbols ^rbIGfIsN

09 ^f3MAMSEs

API layer ^Op0Q9TOR

接口 · 后端 · 技术层 ^sX9vgRIP

Google · Material Symbols ^sBUDDxaU

10 ^4uvU4r9v

Database layer ^CgZ1LDne

数据库 · 数据 · 技术层 ^mtVsceT5

Google · Material Symbols ^vNMHE30b

11 ^24uYUnkw

Access lock ^GxuPyuJn

门禁 · 等待 · 阻塞 ^1PFm6XY2

Google · Material Symbols ^HWx941KL

12 ^z6S3ad6J

Monorepo ^tpUkUpyb

单仓 · 共享 · 跨层 ^34pQ8VCZ

Google · Material Symbols ^bkoKQhAH

13 ^Iqq680gt

Elevator ^ai4B0JoJ

贯通 · 跨层 · 端到端 ^gmbTdfi8

Google · Material Symbols ^PqiVRjd1

14 ^h3SkKptJ

Finish flag ^dwOAa4IE

终点 · 计时 · 测量点 ^pmhDfDsX

Google · Material Symbols ^frmySfPI

15 ^82Ti0pr6

Image candidate ^HFYNFBsH

图片 · 视口 · 候选内容 ^yYK7oozF

Google · Material Symbols ^QD1CpZFI

16 ^mVTkzpNd

Text candidate ^e4RMKSjR

文本 · 视口 · 候选内容 ^MgBn2gov

Google · Material Symbols ^rNVE4apN

17 ^ZV3QeqD8

Electrical services ^ivHvvyae

连接 · 插接 · 稳定接口 ^P2juxbYd

Google · Material Symbols ^XsPb7Lb4

18 ^4sUcLIGO

Product inventory ^xafD5aEl

商品 · 库存 · 业务能力 ^JkSINqGu

Google · Material Symbols ^2rzy0RR8

19 ^hN93XilP

Price tag ^sblj2NCZ

价格 · 标签 · 业务能力 ^iUAe7H1e

Google · Material Symbols ^0o8UrhMY

20 ^PA2o72xT

Availability check ^AB4bJnpv

可售 · 校验 · 状态确认 ^74Ulff0a

Google · Material Symbols ^4nTUzlfk

21 ^Wem5MlZM

Smartphone ^nNnYafPD

移动端 · App · 消费入口 ^oRtRxKgv

Google · Material Symbols ^fe4JxsID

22 ^qI3QZfAB

Shrug person ^QKllD18v

摊手 · 人物 · 权衡 ^XjcazQw5

Sarah Rudkin · Noun Project ^keNHooaC

23 ^Utzq08P2

Mood Puzzled ^lQ19bQbV

困惑 · 斜嘴 · 问号 ^9aaIws8a

Paweł Kuna · Tabler Icons ^SZeiF8KR

24 ^nlGrNmsN

Relationship tree ^Zgxy9B41

关系 · 层级 · 稳定结构 ^haBMQbsH

Google · Material Symbols ^bFVMN1Yq

25 ^j47UzUfe

Filter ^RwN9mnjF

筛选 · 提纯 · 降噪 ^56ghqcS3

Google · Material Symbols ^hc0LsRgG

26 ^116qwuWC

Desk ^8gU3398V

书桌 · 工作台 · 现场 ^pDI62gaT

Google · Material Symbols ^hJU6po7w

27 ^jMsKhEEw

Open book ^72ti8nTx

书本 · 来源 · 当前页 ^atp6wNbE

Google · Material Symbols ^kBvmrzKd

28 ^AaMXpJDO

Sticky note ^k1Pm9Mkt

便签 · 问题 · 临时材料 ^pHcrhLqq

Google · Material Symbols ^s683Z3iw

29 ^aAGnvC7g

Bookmark ^3oiCTeY0

书签 · 保存点 · 继续 ^TdlQbDdz

Google · Material Symbols ^kEVFFaf6

30 ^s9i1nxVT

Camera ^4OFcIYIQ

相机 · 快照 · 状态保存 ^fcAOxOiz

Google · Material Symbols ^kpYArBjE

31 ^Ld31NumA

Ladder ^Ld31Name

梯子 · 技术栈 · 可达范围 ^Ld31Keys

Paweł Kuna · Tabler Icons ^Ld31SrcA

31 个可复用 SVG · 来源与许可见文本索引 ^LibCnt31

## Embedded Files
649b4209e11d06793c7282c0ddd0238e23cd1712: [[confused-face-mood-puzzled-tabler-handdrawn.svg]] {"currentcolor":"#001219"}

35d16bbcb3c535e0b4836feda06e9931445595d6: [[building-blocks-handdrawn.svg]] {"currentcolor":"#001219"}

36abc29441e56c46412c28e20dbdb4e80feafc83: [[curtain-handdrawn.svg]] {"currentcolor":"#001219"}

56a81038093a8e8882ea537f00c5bde06558033c: [[wallpaper-pattern-handdrawn.svg]] {"currentcolor":"#001219"}

4b1c53a456ffbc72ae3d28a7fe935e0cebd376e1: [[role-business-material-symbol-handdrawn.svg]] {"currentcolor":"#001219"}

f62b42cdb4448b9f084f93339dda77b53a87c2e5: [[role-product-material-symbol-handdrawn.svg]] {"currentcolor":"#001219"}

4821b26942349f283cd3ac863b1532d9ed7c31f5: [[role-engineering-material-symbol-handdrawn.svg]] {"currentcolor":"#001219"}

a16a067e17e70dcc7db1ce19d187e046dec4af4c: [[role-ai-material-symbol-handdrawn.svg]] {"currentcolor":"#001219"}

4d09c8c537a9b0086bfcd3ff3c5ebfedf0df4844: [[layer-ui-web-material-symbol-handdrawn.svg]] {"currentcolor":"#001219"}

f31166db8b3f6f84d67d8cf8a3c93f7f12b59b69: [[layer-api-material-symbol-handdrawn.svg]] {"currentcolor":"#001219"}

ac516d00057eaf3bd5a6d7a3d3e807ebad3cb2e4: [[layer-database-material-symbol-handdrawn.svg]] {"currentcolor":"#001219"}

4af24f845baf0a3c3d3b1390d6d3fbdfad086d37: [[access-lock-material-symbol-handdrawn.svg]] {"currentcolor":"#001219"}

3a227290881802f678f16ef014fd622197f94d60: [[monorepo-folder-code-material-symbol-handdrawn.svg]] {"currentcolor":"#001219"}

4a362e9eb6315d3953ffc10b991bb1da624784c9: [[elevator-material-symbol-handdrawn.svg]] {"currentcolor":"#001219"}

f61a82358ddfdda8aa64c5bcd4af08f093335e75: [[lcp-finish-flag-material-symbol-handdrawn.svg]] {"currentcolor":"#001219"}

6fb4f0b61985d062d1fc3c5326a1545c8837e8cf: [[lcp-image-material-symbol-handdrawn.svg]] {"currentcolor":"#001219"}

fa29c270dc5d399037daff9c10c3d7767e391ab0: [[lcp-text-material-symbol-handdrawn.svg]] {"currentcolor":"#001219"}

06cb8e5e91f1aae20fb7360355a7466338606139: [[electrical-services-material-symbol-handdrawn.svg]] {"currentcolor":"#001219"}

ac8772443891444d2bcb5c0881997357d8d31fc5: [[product-inventory-material-symbol-handdrawn.svg]] {"currentcolor":"#001219"}

cac2b13777934be7a58249f31a627914acf606f1: [[price-sell-material-symbol-handdrawn.svg]] {"currentcolor":"#001219"}

12e11d83991fbd3356b3a718f3672782e783397c: [[availability-fact-check-material-symbol-handdrawn.svg]] {"currentcolor":"#001219"}

ebf3abe52a703bd8fb3f134dcd35e121de97d808: [[smartphone-material-symbol-handdrawn.svg]] {"currentcolor":"#001219"}

d72c0c0b07ab8d39f0e031285258933a9286188c: [[account-tree-material-symbol-handdrawn.svg]] {"currentcolor":"#001219"}

75b5c7cf22e542a9442fb50215a923cbcc69de0f: [[filter-alt-material-symbol-handdrawn.svg]] {"currentcolor":"#001219"}

36026e017cbc8faca9f9259d07893c2489325aff: [[desk-material-symbol-handdrawn.svg]] {"currentcolor":"#001219"}

9cee780237c80a9efc5a40b8517893fab075132c: [[menu-book-material-symbol-handdrawn.svg]] {"currentcolor":"#001219"}

4c8040de3c103453b9692bc526bc8b4f8ce94102: [[sticky-note-material-symbol-handdrawn.svg]] {"currentcolor":"#001219"}

d9b65dcfd0890e8c35b454271380280eff660b0c: [[bookmark-material-symbol-handdrawn.svg]] {"currentcolor":"#001219"}

318f94923bfe1c57a3d66bf236f20b204f08d5fd: [[photo-camera-material-symbol-handdrawn.svg]] {"currentcolor":"#001219"}

caa6db59b750ab746bc9a79ddc576d0b917607b1: [[confused-programmer-shrug-nounproject-handdrawn.svg]] {"currentcolor":"#001219"}

7062e048ebc4be6dcfbe724d1d25e7400c136ad4: [[ladder-tabler-handdrawn.svg]] {"currentcolor":"#001219"}

%%
## Drawing
```compressed-json
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

KbZVQAfoTMANgHRnf2k3BSZHkCAAA===
```
%%
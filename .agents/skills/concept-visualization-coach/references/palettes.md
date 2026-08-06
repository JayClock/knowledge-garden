# LEGO 卡配色参考

快照来源：[Coolors · Trending Color Palettes](https://coolors.co/palettes/trending)，查看日期：2026-08-06。

Coolors 的趋势列表会变化。趋势色板是候选颜色集合，不应再机械压缩成“轮廓／强调／辅助／背景”四个色值。项目默认保留 5–8 个源色，并按概念关系分配语义；单张卡只启用有意义的颜色，避免为了“丰富”而平均撒色。

## 项目默认：Teal–Paper Semantic 8

来源：[自定义 Coolors 色板](https://coolors.co/001219-005f73-009999-99dede-f3e9e0-ee9b00-ca6702-bb3e03-fff6f0)，以 Trending 中的 [Ocean Sunset](https://coolors.co/001219-005f73-0a9396-94d2bd-e9d8a6-ee9b00-ca6702-bb3e03-ae2012-9b2226) 为语义骨架，并参考 [Visual Thinking Workshop](https://www.visual-thinking-workshop.com/) 的青绿品牌色与暖纸表面。

“Teal–Paper Semantic 8”保留冷色结构／流动与暖色注意／动作／冲突的语义分工，同时把页面与卡片重构为适合可视化博客的暖纸层级。变量名称保持稳定，旧卡按相同语义重新映射，而不是重新解释颜色。

| 语义角色 | 色值 | 用途 |
|---|---|---|
| 主墨色 | `#001219` | 主标题、正文、人物、默认图标和外框 |
| 深冷结构 | `#005F73` | 共享边界、稳定结构、链接与可读按钮 |
| 品牌／正向流动 | `#009999` | 协同、贯通、成功路径、品牌装饰；不用于小号正文 |
| 冷色填充 | `#99DEDE` | 共享区域、客户端、次级正向状态底色 |
| 暖纸页面 | `#F3E9E0` | 博客页面、地图底板、上下文区域 |
| 注意／未知 | `#EE9B00` | 问号、选择、人物焦点、关键标记 |
| 摩擦／动作 | `#CA6702` | 交接、攀爬、过渡、动作关系 |
| 冲突／边界 | `#BB3E03` | 阻塞、过度责任、危险边界、反例 |
| 卡片／画布 | `#FFF6F0` | 知识卡、插图画布、按钮文字和浅色表面 |

### 对比度要点

| 颜色 | 对卡片 `#FFF6F0` | 对主墨色 `#001219` |
|---|---:|---:|
| `#001219` | `17.89:1` | — |
| `#005F73` | `6.83:1` | `2.62:1` |
| `#009999` | `3.27:1` | `5.47:1` |
| `#99DEDE` | `1.42:1` | `12.59:1` |
| `#F3E9E0` | `1.12:1` | `15.94:1` |
| `#EE9B00` | `2.11:1` | `8.47:1` |
| `#CA6702` | `3.61:1` | `4.95:1` |
| `#BB3E03` | `5.18:1` | `3.46:1` |

小号文字在卡片背景上优先使用 `#001219`、`#005F73` 或 `#BB3E03`。`#009999` 用作品牌图形、粗线和大号标记；主按钮使用 `#005F73` 配 `#FFF6F0`，避免青绿色背景上的浅色小字。其余浅色主要用于面积或以 `#001219` 为前景的填充区域。

## CSS 变量与替换

唯一变量来源：`Knowledge/Assets/Styles/concept-visualization-palette.css`

基础变量保持稳定命名：

```css
--concept-color-ink
--concept-color-deep-structure
--concept-color-positive-flow
--concept-color-cool-fill
--concept-color-warm-fill
--concept-color-attention
--concept-color-friction
--concept-color-conflict
--concept-color-canvas
```

另有 `--concept-color-text-primary`、`--concept-color-icon-default`、`--concept-color-brand-primary`、`--concept-color-link`、`--concept-color-surface-page`、`--concept-color-surface-card` 和 `--concept-color-state-positive` 等用途别名，以及与现有 SVG 约定衔接的 `--icon-color`。替换整套色板时只修改九个基础变量的值，不改变量名或消费方。

CSS 使用示例：

```css
.concept-card {
  color: var(--concept-color-text-primary);
  background: var(--concept-color-canvas);
  border-color: var(--concept-color-border-default);
}
```

SVG 配色脚本可以直接解析变量及其 `var(...)` 别名：

```bash
python scripts/svg_palette.py variant \
  source.svg /tmp/positive.svg \
  --color-var=--concept-color-state-positive
```

Excalidraw 场景最终仍保存解析后的 HEX，不会实时读取外部 CSS；更换基础变量后，应按同一语义映射重新执行场景配色。不要在笔记、脚本或新 SVG 中再建立第二份权威颜色常量表。

### Excalidraw 场景一键同步

同步工具读取 CSS 当前值，并以 `references/palette-sync-state.json` 中的上次落盘快照完成旧值到新值的语义迁移。状态文件只是迁移游标，CSS 仍是唯一权威来源。

```bash
# 从仓库根目录运行；默认只检查，不写文件
npm run palette:check

# 确认后通过 Obsidian Excalidraw 插件同步
npm run palette:sync

# 也可以从 skill 目录直接调用
scripts/sync_excalidraw_palette.sh --check
scripts/sync_excalidraw_palette.sh --apply
```

`--check` 在存在待同步内容时退出码为 `2`。`--apply` 只保存确有变化的画布，全部成功后才更新状态；中途失败可直接重跑。脚本同时检查未登记颜色、知识正文、元素数量和 ID。新增采用本色板的画布时，把路径及其 `backgroundRole` 登记到 `references/palette-sync-state.json`，不要靠扫描全库误改无关绘图。

## 紧凑备选：Black & Gold Elegance

来源：[Coolors palette](https://coolors.co/000000-14213d-fca311-e5e5e5-ffffff)

| 角色 | 色值 | 用途 |
|---|---|---|
| 轮廓／正文 | `#14213D` | 主图标、关系线、正文 |
| 强调 | `#FCA311` | 焦点、选中状态、关键局部 |
| 辅助 | `#E5E5E5` | 次级区域、容器底色 |
| 背景 | `#FFFFFF` | 卡片背景 |

轮廓与背景对比度约 `15.97:1`。强调色与背景只有约 `2.02:1`，因此强调色用于面积、标记或粗线，不用于小号正文。该方案适合需要极简、正式或单焦点表达的卡片，不再作为项目默认。

## 备选：Summer Ocean Breeze

来源：[Coolors palette](https://coolors.co/e63946-f1faee-a8dadc-457b9d-1d3557)

| 角色 | 色值 | 用途 |
|---|---|---|
| 主墨色 | `#1D3557` | 主图标、正文 |
| 次级结构 | `#457B9D` | 边界、连接、次级层级 |
| 冷色填充 | `#A8DADC` | 次级图形、关系区域 |
| 冲突强调 | `#E63946` | 冲突、转折、关键焦点 |
| 背景 | `#F1FAEE` | 卡片背景 |

主墨色与背景对比度约 `11.56:1`。适合对比、注意力和变化主题；红色强调不用于小号正文。

## 备选：Neutral Harmony Bliss

来源：[Coolors palette](https://coolors.co/f4f1de-e07a5f-3d405b-81b29a-f2cc8f)

| 角色 | 色值 | 用途 |
|---|---|---|
| 主墨色 | `#3D405B` | 主图标、正文 |
| 人物／动作 | `#E07A5F` | 人物、动作、关键节点 |
| 关系／生长 | `#81B29A` | 次级结构、连接区域 |
| 注意填充 | `#F2CC8F` | 提示、选择、浅色焦点 |
| 背景 | `#F4F1DE` | 卡片背景 |

主墨色与背景对比度约 `8.87:1`。适合温和、反思、学习及人与系统主题。

## 备选：Olive Garden Feast

来源：[Coolors palette](https://coolors.co/606c38-283618-fefae0-dda15e-bc6c25)

| 角色 | 色值 | 用途 |
|---|---|---|
| 主墨色 | `#283618` | 主图标、正文 |
| 次级结构 | `#606C38` | 次级图标、关系线 |
| 浅色背景 | `#FEFAE0` | 卡片与安静区域 |
| 轻动作 | `#DDA15E` | 过渡、提示、暖色填充 |
| 强动作 | `#BC6C25` | 关键对象、变化点 |

主墨色与背景对比度约 `12.24:1`。适合生长、积累、生态和长期演化主题。

## 使用规则

1. 一套源色板保留 5–8 个颜色；三个原型共享同一源色板，但可以只启用其中有语义的 5–7 色，不必强制把每个颜色都放进画面。
2. 先建立颜色语义，再上色：例如冷色族表示结构／共享／正向流动，暖色族表示注意／动作／冲突。相同含义跨卡保持同色。
3. 主墨色承担阅读；正文与背景至少达到 `4.5:1`。不达标的颜色只用于非文字元素，或作为能与主墨色达到 `4.5:1` 的填充。
4. 颜色数量增加后仍要保持注意力层级：一个主焦点、一个次焦点，其余颜色服务于分类和关系，不把每个对象都涂成不同颜色。
5. 同一卡中复用同一对象时保持颜色稳定；只有语义发生变化时才换色。装饰性变化不能成为新增颜色的理由。
6. 先在粗糙原型中执行去文字测试、灰度测试和对比度检查，再沉淀为常用色板。

## SVG 配色变量

所有索引 SVG 使用单色入口：

```css
--icon-color
```

源文件默认回退到黑色。为卡片生成配色副本时优先解析语义变量：

```bash
python scripts/svg_palette.py variant \
  Knowledge/Assets/Icons/building-blocks.svg \
  /tmp/building-blocks-accent.svg \
  --color-var=--concept-color-positive-flow
```

脚本仍接受 `--color '#RRGGBB'` 作为临时兼容入口，但项目内固定工作流不要复制 HEX。

同一个 SVG 可以生成主墨色、结构色、正向色、动作色或冲突色实例。不要为了多色效果随意拆改图标内部路径；优先通过多个可复用图标实例、Excalidraw color map、容器填充和关系线形成层级。

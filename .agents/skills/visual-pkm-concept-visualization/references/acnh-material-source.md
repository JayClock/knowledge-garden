# ACNH Pocket Guide 素材来源与使用规则

本文件规定用户明确选择《集合啦！动物森友会》视觉语言后，如何从 ACNH Pocket Guide 选择、下载、追溯和使用素材。ACNH 不是默认素材层，也不在快速联想阶段检索；只有最终方向确实需要这类人物、物体或场景时才完整读取本文件。

一般外部素材边界以[入选素材的生产检查](material-source-order.md)为准。

## 1. ACNH 固定来源

- 仓库：<https://github.com/jameskokoska/ACNH-Pocket-Guide>
- 默认分支：`main`
- Raw 基址：`https://raw.githubusercontent.com/jameskokoska/ACNH-Pocket-Guide/{ref}/`
- 应用素材根目录：`animal_crossing_app/assets/`

`main` 会变化。每次实际采用素材时，先用 `git ls-remote https://github.com/jameskokoska/ACNH-Pocket-Guide.git refs/heads/main` 或 GitHub API 解析并记录当时的 commit SHA；最终追溯优先使用带 SHA 的 GitHub 或 Raw URL，而不是只记录 `main`。

如果用户提供了本地 clone 或素材目录，优先使用该位置，但仍记录其 remote 与 commit。不要假设本机存在固定 clone 路径，也不要把 Obsidian vault 中的临时目录当成素材事实来源。

## 2. 可用素材层

### 2.1 结构化游戏数据

主入口：

`animal_crossing_app/assets/data/DataCreated/`

按语义分组：

- 家具与空间：`Housewares.json`、`Miscellaneous.json`、`Wall-mounted.json`、`Ceiling Decor.json`、`Interior Structures.json`、`Floors.json`、`Wallpaper.json`、`Rugs.json`、`Fencing.json`、`Gyroids.json`、`Construction.json`
- 服饰与随身物：`Tops.json`、`Bottoms.json`、`Dress-Up.json`、`Headwear.json`、`Accessories.json`、`Shoes.json`、`Socks.json`、`Bags.json`、`Umbrellas.json`、`Clothing Other.json`
- 生物与博物馆：`Fish.json`、`Insects.json`、`Sea Creatures.json`、`Fossils.json`、`Artwork.json`
- 角色与社交：`Villagers.json`、`Special NPCs.json`、`Photos.json`、`Posters.json`、`Reactions.json`、`Message Cards.json`、`Paradise Planning.json`
- 制作、收集与时间：`Recipes.json`、`Music.json`、`Achievements.json`、`Seasons and Events.json`、`ToolsGoods.json`、`Other.json`

`animal_crossing_app/assets/data/data.json` 是体积较大的聚合原始数据库。概念视觉检索默认先用已拆分的 `DataCreated/*.json`，只有拆分数据缺字段时才读取它。

专项数据：

- `artIdentification.json`：艺术品真假辨识
- `flowers.json`：花卉杂交关系与概率
- `events.json`：活动资料
- `ordinances.json`：岛屿条例
- `extraSongs.json`：补充歌曲资料
- `categoryConstants.json`：类别与显示字段定义
- `tvTimes.py`：电视节目时间数据脚本；它不是 JSON

### 2.2 翻译数据

- `animal_crossing_app/assets/data/Generated/translatedItems.json`
- `animal_crossing_app/assets/data/Generated/translatedVillagers.json`
- `animal_crossing_app/assets/data/Generated/translatedSpecialNPCs.json`
- `animal_crossing_app/assets/data/Generated/translatedVariants.json`
- `animal_crossing_app/assets/data/Generated/translatedCatchphrases.json`
- `animal_crossing_app/assets/data/Generated/translatedVillagerCatchPhrases.json`
- `animal_crossing_app/assets/data/Generated/translatedMuseumDescriptions.json`
- `animal_crossing_app/assets/data/Generated/translationsAppGenerated.json`
- `animal_crossing_app/assets/data/TranslationsStrings/`

基础记录通常以英文名为键。为中文卡片选择素材时，用生成的翻译表辅助检索与显示，但追溯表同时保留英文 `Name`、`Internal ID` 或其他稳定标识，不能只记录中文译名。

### 2.3 Amiibo 数据

`animal_crossing_app/assets/data/Amiibo Data/` 包含 Series 1–5、Welcome amiibo、Sanrio 和 Promos。记录可能引用 `dodo.ac` 等站点的图片。使用时同时记录 JSON 文件、卡号、角色名、图片字段和最终 URL。

### 2.4 仓库内视觉文件

`animal_crossing_app/assets/icons/` 包含 UI 图标、NPC／节日／季节图标、鱼影、尺寸示意、神秘岛缩略图、少量 Amiibo 卡图与设置示例。它们主要是 PNG/JPG，不是可任意换色的项目 SVG。

可以把这些素材作为人物、物体、季节、时间、地点、边界、工具或状态组件的描摹参考；不要因为画面可爱就把它当作无语义装饰，也不要仅凭文件名采用，必须查看实际图像。入选后仍需描摹为原生 Excalidraw 组件。

### 2.5 记录中的远程图片

大量物品、生物、居民和艺术品图片并未存入 Git 仓库，而是由 JSON 字段引用远程资源，常见来源包括 `acnhcdn.com`；Amiibo 记录还可能引用 `dodo.ac`。

常见图片字段包括：

- `Image`
- `Icon Image`
- `Critterpedia Image`
- `Furniture Image`
- `Photo Image`
- `House Image`
- `Closet Image`
- `Storage Image`
- `Inventory Image`
- `High-Res Texture`
- Amiibo 的 `image`

不同数据集的 schema 不一致。数字经常保存为字符串，缺失值可能是 `"NA"`、空字符串或 `null`。读取前检查实际字段，不要假设所有类别共用一个 schema。

### 2.6 音频

`animal_crossing_app/assets/data/Media/` 包含小时 BGM 与 K.K. 的唱片、现场和八音盒版本。它不是视觉知识卡的默认素材层；除非用户明确要求声音卡或音视频输出，否则不要下载、嵌入或把音频误当作视觉组件。

## 3. 从概念到素材的检索顺序

1. 从用户选定的核心信息、隐喻和草图提取英文与中文检索词，并补充动作、关系、物体类别和相反状态。
2. 先搜索 `DataCreated/*.json` 的 `Name`、`Source`、`Season/Event`、`Where/How`、`Description`、`Catch phrase` 等实际存在的字段。
3. 用 `Generated/translated*.json` 扩展中文检索；不要只匹配译名。
4. 再搜索 `assets/icons/` 的文件名与目录，但采用前必须打开图像核对。
5. 比较记录中的多个图片字段，选择最符合当前语义与构图层级的版本。例如小型符号优先清晰图标，角色关系可考虑照片或全身图，艺术品细节可考虑高分辨率纹理。
6. 实际访问 URL 或读取本地文件，确认资源存在、格式可用且不是占位图。
7. 如果多个候选只是外观接近而语义不同，回到概念关系判断，不按“最可爱”或“最精致”自动选择。

## 4. 获取方式

### 4.1 单文件按需下载

优先只下载当前需要的 JSON 或图片。例如：

```bash
curl -L \
  "https://raw.githubusercontent.com/jameskokoska/ACNH-Pocket-Guide/{ref}/animal_crossing_app/assets/data/DataCreated/Fish.json" \
  -o "$TMPDIR/Fish.json"
```

把 `{ref}` 替换为已记录的 commit SHA。远程图片从记录的实际图片字段下载到临时目录，只作为描摹参考；入选后通过 Obsidian／Excalidraw 插件用原生元素描摹，不直接导入或嵌入源图。

### 4.2 多次检索时使用 sparse checkout

仓库包含大量音频，历史与完整工作树体积较大。只有需要反复检索时，才在用户同意的位置做稀疏检出：

```bash
git clone --depth 1 --filter=blob:none --sparse \
  https://github.com/jameskokoska/ACNH-Pocket-Guide.git \
  ACNH-Pocket-Guide

cd ACNH-Pocket-Guide
git sparse-checkout set \
  "animal_crossing_app/assets/data/DataCreated" \
  "animal_crossing_app/assets/data/Amiibo Data" \
  "animal_crossing_app/assets/data/Generated" \
  "animal_crossing_app/assets/data/TranslationsStrings" \
  "animal_crossing_app/assets/icons"
```

不要默认检出 `assets/data/Media/`，也不要为了一个图标静默克隆整个仓库。不要把临时 clone 或批量下载内容提交进知识库。

## 5. 组合与配色

- ACNH 的 PNG/JPG 保留原始宽高比与原色，只作为临时描摹参考；不要把它们当作 `--icon-color` 单色 SVG，也不要直接复制、封装或嵌入知识卡与 Icon 索引。
- 用户明确要求把候选重绘为扁平 SVG 时，可以保留来源色彩关系并标记 `data-color-mode="source-palette"`；该 SVG 仍只是临时参考。入选后必须通过 Excalidraw 插件描摹为只含原生元素的纯 JSON `.excalidraw` 组件，并保留用户确认的颜色，除非用户另行要求创建项目语义色板变体。
- `concept-visualization-palette.css` 是可选的统一视觉语言，不控制所有最终卡片、自制组件或永久 icon。已描摹 icon 的内部颜色不进入项目色板 Gate；游戏原色在权利允许且用户确认时可以保留在原生组件中。
- 统一画面时优先用裁切、留白、尺度、扁平轮廓、背景和关系线建立层级；不得不可逆地改写原始素材，需要不同配色时创建单独的原生 Excalidraw 变体。
- `scripts/svg_palette.py` 的 `prepare`／`variant` 只用于可变单色项目 SVG，不用于 PNG/JPG，也不用于把 `source-palette` SVG 冒充整体可换色图标。
- 一个游戏对象只有在其动作、功能、处境或文化联想能推进核心信息时才进入画面。例如桥可以承担“过渡”，网可以承担“捕获／筛选”，化石可以承担“由残片重建”；仅仅同名不构成语义匹配。
- 不默认使用游戏 Logo、品牌字样或角色肖像替代概念论证。

## 6. 追溯格式

每个承担概念含义的 ACNH 素材至少记录：

| 字段 | 要求 |
|---|---|
| 草图／组件 | 说明它位于哪个最终视觉或承担什么组件；只有确实使用候选编号时才记录编号 |
| 数据集／目录 | 例如 `DataCreated/Fish.json` 或 `assets/icons/shadowsAligned/` |
| 记录标识 | 英文 `Name`，并尽量补充 `Internal ID`、Amiibo 卡号或文件名 |
| 中文显示名 | 来自已核对的翻译表；没有可靠翻译时留空 |
| 图片字段 | 例如 `Icon Image`、`Image` 或本地文件路径 |
| 固定版本 | commit SHA 与访问日期 |
| 原始 URL | 带 SHA 的仓库 URL，以及记录实际引用的图片 URL |
| 概念作用 | 它表达哪个动作、关系或对比 |
| 使用位置 | 目标卡片／画布与方案编号 |
| 权利状态 | 已确认、待确认，或仅作构图灵感 |

这张表是最终采用素材的生产审计，不是 Icon 索引 schema。只有用户明确要求把已确认组件提升为长期复用图标时，才把必要信息写入 `references/icon-index-registry.json`：标题、完整 SVG 路径、最多 8 个关键词、固定版本的来源链接、来源方及必要的改编／核对状态。随后使用 `scripts/sync_icon_index.py` 同步索引；不要把概念作用、使用位置或处理日志重新塞回索引。

来源追溯默认留在答复或用户指定记录文件，不自动写进知识卡正文。

## 7. 来源与权利边界

- 编写本规则时，ACNH Pocket Guide 仓库未提供明确的顶层 `LICENSE`；每次公开使用前重新检查，公开可访问不等于可任意再授权。
- `DataCreated/Read Me.json` 指向 ACNH Item Spreadsheet，并要求使用其数据的应用或网站回链该表格、联系维护者登记合作项目。
- 游戏图片、角色、音乐、商标和其他内容还可能受任天堂及各素材提供方的权利约束；仓库代码、社区数据与游戏素材不是同一个许可层。
- 对私人研究或本地草图，仍然保留完整追溯。目标位于发布目录、演示文稿、公开网站或商业交付时，在嵌入素材前单独确认权利；无法确认时，只把候选作为构图灵感，改用用户拥有权利的自制表达，并把状态写为“待确认”。
- 不声称素材是自制、CC、公共领域或“官方可自由使用”，除非有对应证据。

## 8. 未命中

如果 ACNH 来源没有可靠候选：

1. 明确说明当前缺少的最小视觉组件与已检索的数据集／关键词。
2. 优先回到基础形状、关系线、用户草图或自制表达。
3. 若用户仍希望采用外部成品素材，再按[入选素材的生产检查](material-source-order.md)选择合适来源；不自动跳转到固定下一层。

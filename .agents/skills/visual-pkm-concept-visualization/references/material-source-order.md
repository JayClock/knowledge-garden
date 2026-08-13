# 入选素材的生产检查

## 使用时机

本规则不属于快速联想、框架尝试或五分钟草图。只有用户已经通过 ETC 选定方向，并且最终数字化方案实际采用外部素材、准备公开发布或需要长期复用时才执行。

不要为未入选联想搜索成品图、下载文件或建立追溯表。素材检查应当保护最终交付，而不是阻断视觉思考。

## 选择顺序

外部来源采用明确边界：一般性的“寻找外部素材”只授权继续寻找，不授权打开新的来源站点。按以下原则选择：

1. **自己的视觉词库优先。** 先查看旧草图、`Knowledge/Maps/Icon 索引.md` 和 `Knowledge/Assets/Excalidraw/Icon - *.excalidraw` 组件，优先重组熟悉元素。
2. **基础形状与自制表达优先于弱匹配。** 圆、线、箭头、边界、尺度和用户草图往往比关键词相同但关系错误的成品 icon 更准确。
3. **只使用已有注册来源。** 外部检索前读取 `references/icon-index-registry.json`；默认只能使用本任务开始前已存在于 `source_groups` 的来源，并继续遵守各来源自己的附加 Gate。
4. **用户可以明确指定新范围。** 用户明确给出网站、素材集合、本地目录或许可范围后，才可在该范围内搜索。笼统的“找外部素材”“换一个外部 icon”不构成新增来源授权；向注册表增加新 `source_group` 前再次确认该具体来源。
5. **灵感与采用分开。** 即使来源在允许范围内，权利不清的图片也只能帮助理解构图，不能因此直接嵌入公开成品。
6. **语义准确优先于画风。** 素材必须说明它表达哪个动作、关系或对比；更可爱、更精致或同名不构成采用理由。

用户明确要求《集合啦！动物森友会》素材时，完整读取并执行 [ACNH 素材规则](acnh-material-source.md)。ACNH 虽可登记在注册表中，仍是需要用户明确选择的特定视觉语言，不是默认素材层。

## 最终采用前的最低检查

只对最终实际使用的外部组件完成：

1. 确认来源属于本任务开始前已有的 `source_groups`，或落在用户明确指定的范围内；不满足时停止搜索、下载和采用。
2. 打开真实图像和原始详情页，不只看文件名、搜索缩略图或 CDN 地址。
3. 记录足以再次找到它的信息：标题／作者、素材 ID 或稳定记录、原始页面、访问日期。
4. 核对许可、署名、账户／订阅限制和目标用途；不同素材不能沿用站点级假设。
5. 无法确认公开或商业使用权时，只保留构图启发，改用用户拥有权利的草图、基础形状或自制表达。
6. 原始素材副本保持宽高比和原色；未经许可不改写颜色、删除署名或声称素材为自制。若许可允许最终使用，用户可以选择保留原色，也可以另行授权创建配色变体。
7. 外部 SVG、PNG/JPG、WebP 或其他图像只能作为描摹参考；进入知识卡或 Icon 索引前，必须按用户确认的外观与许可要求，通过 Obsidian／Excalidraw 插件描摹为只含原生元素的纯 JSON `.excalidraw` 组件。不得复制、封装或直接嵌入源图。项目语义色板不是永久 icon 的颜色白名单，描摹组件保留用户确认且许可允许的颜色；不得手工编造 Embedded Files 或改写 `compressed-json`。

## 最小追溯记录

| 组件 | 来源／作者 | 素材 ID 或文件 | 原始页面 | 概念作用 | 权利与署名 | 使用位置 |
|---|---|---|---|---|---|---|

只记录最终采用项。来源追溯留在答复或用户指定记录文件，不写入知识卡正文。

## 自有视觉词库

### 读取最小索引

复用 Icon 索引时：

- 按条目标题和 `关键词` 找候选，再打开完整路径嵌入的实际 Excalidraw icon 组件；不凭名称猜测；
- 把关键词当作检索把手，不把它们当作图标的固定意义；
- 通过叠加、替换局部、改变方向或关系形成新意义；
- 使用位置通过 Obsidian backlinks、links 或 Vault 搜索 `.excalidraw` 组件路径获得，不在索引中维护手工清单。

### 固定来源注册表与同步脚本

`references/icon-index-registry.json` 是标题、关键词和内部素材数据的手工维护入口。`scripts/sync_icon_index.py` 根据注册表重建 `Knowledge/Maps/Icon 索引.md` 的普通 Markdown，并逐字节保留 `# Excalidraw Data` 及其后的内容。Icon 索引不展示或保存来源／权利信息。

脚本固定输出每项的最小结构：

```md
## 名称

![[Knowledge/Assets/Excalidraw/Icon - Example.excalidraw|180]]

- **关键词**：最多 8 个检索词
```

不要直接在索引中恢复来源／权利、`使用`、`同步引用`、`去标签观察`、`可能读法`、`联想／语境`、`处理`或手工数量／样式字段。需要修正内部素材数据、关键词或条目顺序时，修改注册表后同步；只有用户明确要求扩充或修正视觉词库时才执行。

从 Git 根目录运行：

```bash
# 修改注册表前先确认当前索引没有漂移
python3 .agents/skills/visual-pkm-concept-visualization/scripts/sync_icon_index.py \
  --vault-root content --check

# 修改注册表并准备好实际 .excalidraw icon 组件后同步，再复查
python3 .agents/skills/visual-pkm-concept-visualization/scripts/sync_icon_index.py \
  --vault-root content --apply
python3 .agents/skills/visual-pkm-concept-visualization/scripts/sync_icon_index.py \
  --vault-root content --check
```

脚本会验证条目 ID、完整路径、`.excalidraw` 后缀、1–8 个关键词、注册表内部素材数据，以及每个 icon 是否为无嵌套 image／frame、具有单一公共 group 的原生 Excalidraw 场景；颜色不参与 Gate。脚本保留现有 `date`／`updated`，这些内部数据不会渲染到 Icon 索引。脚本不修改 Excalidraw 视觉画廊；新增或移除图标后，通过 Excalidraw 插件把对应 `.excalidraw` 文件作为 image reference 嵌入画廊，不能手工改写 `compressed-json`。

## 完成判断

- 是否只检查最终使用的组件？
- 是否先尝试了自己的视觉词库、基础形状和用户草图？
- 每个外部素材是否来自本任务开始前已有的注册来源，或用户明确指定的范围？
- 每个外部素材是否语义准确且能回到原始来源？
- 目标用途的权利和署名是否清楚？
- 不确定时是否改成了自制表达？
- 最终永久 icon 是否全部描摹为只含原生元素的纯 JSON `.excalidraw` 组件，没有直接复制、封装或嵌入外部图像，并保留了用户确认且许可允许的颜色？
- 若更新 Icon 索引，是否只修改固定注册表、没有输出来源／权利信息、通过 `--check`，并保持 Excalidraw Data 不变？

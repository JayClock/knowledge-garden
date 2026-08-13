# 入选素材的生产检查

## 使用时机

本规则不属于快速联想、框架尝试或五分钟草图。只有用户已经通过 ETC 选定方向，并且最终数字化方案实际采用外部素材、准备公开发布或需要长期复用时才执行。

不要为未入选联想搜索成品图、下载文件或建立追溯表。素材检查应当保护最终交付，而不是阻断视觉思考。

## 选择顺序

来源固定为以下两层：

1. **优先来源：自己的 Icon Library。** 先查看旧草图，并在 Excalidraw 中运行 `Downloaded/Icon Library`，按规定文件名里的关键词搜索 `Knowledge/Assets/Excalidraw/Icon - *.excalidraw` 组件，优先重组熟悉元素。
2. **外部搜索来源：Flaticon、The Noun Project、Google Images。** 只有 Icon Library 没有合适组件时才依次搜索这三处，不使用其他外部来源。

基础形状、自制表达和用户草图优先于语义错误的成品 icon。无论来源为何，语义准确都优先于画风；更可爱、更精致或同名不构成采用理由。外部候选只帮助观察与重绘，不能因为搜索可见就直接嵌入公开成品。

## 最终采用前的最低检查

只对最终实际使用的外部组件完成：

1. 确认候选来自 Flaticon、The Noun Project 或 Google Images；其他外部来源停止搜索、下载和采用。
2. 打开真实图像和原始详情页，不只看文件名、搜索缩略图或 CDN 地址。
3. 记录足以再次找到它的信息：标题／作者、素材 ID 或稳定记录、原始页面、访问日期。
4. 核对许可、署名、账户／订阅限制和目标用途；不同素材不能沿用站点级假设。
5. 无法确认公开或商业使用权时，只保留构图启发，改用用户拥有权利的草图、基础形状或自制表达。
6. 原始素材副本保持宽高比和原色；未经许可不改写颜色、删除署名或声称素材为自制。若许可允许最终使用，用户可以选择保留原色，也可以另行授权创建配色变体。
7. 外部 SVG、PNG/JPG、WebP 或其他图像只能作为描摹参考；进入知识卡或 Icon Library 前，必须按用户确认的外观与许可要求，通过 Obsidian／Excalidraw 插件描摹为只含原生元素的纯 JSON `.excalidraw` 组件。不得复制、封装或直接嵌入源图。项目语义色板不是永久 icon 的颜色白名单，描摹组件保留用户确认且许可允许的颜色；不得手工编造 Embedded Files 或改写 `compressed-json`。

## 当前任务中的来源核对

只对最终采用项核对来源、作者、原始页面、许可与署名要求，确保当前用途可用。这些信息用于本轮生产判断，不自动保存成 Icon Library 的清单、注册表或逐项元数据；只有用户另行要求交付证据记录时，才写入用户指定文件。永久 icon 的来源只保留在文件名末尾。

## 自有视觉词库

### 使用 Icon Library

复用视觉词库时：

- 在 Excalidraw 中运行 `Downloaded/Icon Library`，按逗号分隔关键词搜索缩略图，再打开实际 `.excalidraw` 组件观察；不凭关键词猜测含义；
- 文件名固定采用 `Icon - 关键词1, 关键词2 - 来源.excalidraw`，关键词是检索把手，不是图标的固定意义；
- 点击候选会把该 `.excalidraw` 组件作为 image reference 插入当前画布；仍可通过叠加、替换局部、改变方向或关系形成新意义；
- 使用位置通过 Obsidian backlinks、links 或 Vault 搜索组件完整路径获得，不维护手工使用清单。

### 文件名索引与确定性检查

文件名是唯一索引。永久组件统一命名为 `Icon - 关键词1, 关键词2 - 来源.excalidraw`：逗号分隔的关键词供 Icon Library 搜索，末尾来源标明出处；不另建 Markdown 清单、JSON 注册表或逐项元数据。

从 Git 根目录运行：

```bash
python3 .agents/skills/visual-pkm-concept-visualization/scripts/validate_icon_library.py \
  --vault-root content --check
```

检查脚本只扫描实际文件，验证规定文件名、逗号分隔关键词、来源字段，以及每个组件是否为无嵌套 image／frame、具有单一公共 group 的原生 Excalidraw 场景；颜色不参与 Gate。它不读取注册表，也不自动改名或改写画布。

## 完成判断

- 是否只检查最终使用的组件？
- 是否先尝试了自己的视觉词库、基础形状和用户草图？
- 每个外部素材是否来自 Flaticon、The Noun Project 或 Google Images？
- 每个外部素材是否语义准确且能回到原始来源？
- 目标用途的权利和署名是否清楚？
- 不确定时是否改成了自制表达？
- 最终永久 icon 是否全部描摹为只含原生元素的纯 JSON `.excalidraw` 组件，没有直接复制、封装或嵌入外部图像，并保留了用户确认且许可允许的颜色？
- 若更新 Icon Library，是否采用规定文件名、没有建立额外清单或注册表，并通过 `validate_icon_library.py --check`？

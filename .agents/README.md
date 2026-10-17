# 项目级 Agent Skills

项目技能存放于 `.agents/skills/`，Pi 会自动发现该目录下的技能。安装或更新后，在当前会话执行 `/reload`，或重新启动 Pi，即可加载。

## Obsidian Skills

- 上游：[kepano/obsidian-skills](https://github.com/kepano/obsidian-skills)
- 固定版本：[`3ccff5338ea700537839b21900aa5358a0402c98`](https://github.com/kepano/obsidian-skills/tree/3ccff5338ea700537839b21900aa5358a0402c98)
- 安装方式：将上游 `skills/` 中的以下目录完整复制到 `.agents/skills/`，保留原始内容及 `references/`；不使用符号链接或嵌套 Git 仓库。
- 许可证：MIT，原文保存在 [`licenses/obsidian-skills.txt`](licenses/obsidian-skills.txt)。

| 技能 | 用途 |
| --- | --- |
| [obsidian-markdown](skills/obsidian-markdown/SKILL.md) | Obsidian Markdown、双链、嵌入、Callout 和属性 |
| [obsidian-bases](skills/obsidian-bases/SKILL.md) | `.base` 视图、筛选、公式和汇总 |
| [json-canvas](skills/json-canvas/SKILL.md) | `.canvas` 节点、连线和布局 |
| [obsidian-cli](skills/obsidian-cli/SKILL.md) | 通过 Obsidian CLI 操作 Vault 和调试插件 |
| [defuddle](skills/defuddle/SKILL.md) | 将网页正文提取为 Markdown |
| [knap](skills/knap/SKILL.md) | 使用模板及 JSON／CSV 数据批量生成 Markdown |

可显式调用，例如 `/skill:obsidian-markdown` 或 `/skill:json-canvas`。这些技能提供格式和工具操作指导，不替代本仓库已有的职业事实确认、学习编排及 PKM 工作流。

### 运行环境

安装内容仅为技能文档，不修改 Quartz 依赖，也不额外安装全局 CLI。使用工具类技能时，仍需准备对应环境：

- `obsidian-cli`：安装并启用 Obsidian CLI，使 `obsidian` 命令可用，并保持 Obsidian 应用打开。
- `defuddle`：需要 `defuddle` 命令。
- `knap`：需要 Node.js 20+，以及 `knap` 命令或 `npx knap`。

### 更新

从上游选定并记录新的提交，审查技能及参考文件后，替换上述六个技能目录，同时同步许可证和本文件中的固定版本。不要覆盖其他项目技能。

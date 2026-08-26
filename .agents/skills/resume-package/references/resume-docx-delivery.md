# 岗位定制简历 DOCX 交付

用户明确要求 DOCX 时使用。本规范只处理已经通过 opportunity Gate 的内容，不发现或确认新事实。

## 输入与事实

生成前必须读取：

- `.career/claims.json`；
- `.career/opportunities/<opportunity_id>/opportunity.json`；
- 同一 opportunity 的 `outputs/resume.md`；
- selected claim 的 ownership、completion 和 constraints。

课程、旧讲稿和通用知识只能帮助表达，不能绕过 confirmed claim。

## 模板与工具

模板随 `resume-package` 打包：

```text
assets/templates/钟杰-岗位定制简历模板.docx
```

相对路径以 `resume-package/SKILL.md` 所在目录解析。绝不修改模板原件。

使用 OfficeCLI：

```bash
officecli load_skill word
```

遵循当前版本 `officecli help`。不要用 python-docx、LibreOffice 脚本或手工解压 XML 替代；只有 OfficeCLI DOM 无法表达且用户仍要求时，才使用 OfficeCLI 自带的 `raw` / `raw-set`。

## 当前模板结构

当前模板是两页 VML / AlternateContent 文本框布局：

- 2 个正文锚点；
- 14 个可见文本框；
- 标题、能力概述、4 个项目、工作经历、教育背景和自我评价位于文本框；
- 占位符是 `【填写】...`，不是 `{{key}}`；
- 没有 Word 表单字段。

因此：

- 不直接使用 `officecli merge`；
- 不只依赖 `officecli view ... text`；
- 使用 `officecli query "$FILE" 'textbox' --json` 盘点可见文本；
- 全局精确 find / replace 同步修改 AlternateContent 的 Choice 与 Fallback；一个可见占位符通常返回 `2 matched`。

## 生成前确认

至少取得：

- opportunity ID、公司、岗位和 JD；
- 是否需要两页；
- 已冻结的 selected claim IDs 与项目排序；
- 输出文件名。

默认输出：

```text
.career/opportunities/<opportunity_id>/outputs/<姓名>-<岗位>-<公司>.docx
```

## 安全工作流

### 1. 复制模板

```bash
SKILL_DIR='/absolute/path/to/resume-package'
TEMPLATE="$SKILL_DIR/assets/templates/钟杰-岗位定制简历模板.docx"
OUTPUT='<state-dir>/opportunities/<opportunity_id>/outputs/钟杰-岗位-公司.docx'
test -f "$TEMPLATE"
test ! -e "$OUTPUT"
cp "$TEMPLATE" "$OUTPUT"
```

输出已存在时先确认覆盖或生成新版本，不能静默替换已投递文件。

### 2. 盘点文本框

```bash
officecli load_skill word
officecli open "$OUTPUT"
officecli view "$OUTPUT" outline
officecli query "$OUTPUT" 'textbox' --json
```

主要区域：

- `钟杰 【填写目标岗位】`；
- 能力概述中的 7 个占位条目；
- 项目一、项目二、项目三与可选项目四；
- 自我评价中的 3 个占位条目。

联系方式、工作经历和教育背景已有内容，但仍要与 confirmed claims 核对。

### 3. 精确替换

```bash
officecli set "$OUTPUT" / \
  --find '【填写目标岗位】' \
  --replace '高级前端工程师' \
  --json
```

规则：

- 每次检查 `matched`；当前模板通常应为 2。
- `matched = 0` 时停止并重新查询，不继续猜占位符。
- 只匹配完整占位句，不统一替换 `【填写】` 前缀。
- 尽量逐条填充现有项目符号，不用超长字符串覆盖整页文本框。
- 内容超出空间时先压缩次要信息，不擅自缩小到难以阅读的字号。
- 操作较多时可使用 OfficeCLI 原子 `batch`；先用少量替换确认路径。

### 4. 保存和检查

```bash
officecli save "$OUTPUT"
officecli query "$OUTPUT" 'textbox' --json
officecli view "$OUTPUT" issues --limit 100
officecli view "$OUTPUT" html
officecli close "$OUTPUT"
```

确保不存在：

- `【填写】`；
- `{{...}}`；
- `<TODO>`、`xxxx`、`lorem`；
- 不在 selected confirmed claims 中的客户、数字和能力；
- 与 manifest 不一致的项目。

## 模板基线

当前模板已有 30 个 OpenXML 验证错误，主要来自 VML Fallback 的 `anchory="line"` 和重复 `officeArt object` ID。这是模板基线。

1. 记录原模板 `officecli validate` 结果。
2. 再验证输出。
3. 要求不新增错误，不强行把基线降到零。
4. 不为消除基线错误重写 VML，除非用户明确要求维护模板。

## 岗位自我介绍

DOCX 内容确定后，使用相同 claim IDs 生成：

```text
.career/opportunities/<opportunity_id>/outputs/self-introduction.md
```

读取 `../interview-package/references/interview-oralization.md`，控制在 90～120 秒。岗位简历可以放更多项目，自我介绍通常只展开最匹配的两个，但不能引入新的 claim。

不要覆盖全局 `自我介绍.md`；它只保留通用基础版。

## Manifest

为 DOCX 和自我介绍分别写 manifest：

```json
{
  "schema_version": 1,
  "artifact": ".career/opportunities/<id>/outputs/resume.docx",
  "artifact_type": "resume_docx",
  "opportunity_id": "<id>",
  "generated_by": "resume-package",
  "claim_ids": [],
  "status": "current"
}
```

## 完成 Gate

- 精确替换全部命中；
- 文本框无占位符；
- `view issues` 没有新增问题；
- validate 不新增基线错误；
- HTML 或截图无截断、重叠和溢出；
- DOCX 与岗位自我介绍使用同一 claim 集；
- 两个 manifest 和 opportunity artifacts 已更新；
- 用户最终用 Word / WPS / Pages 打开确认。

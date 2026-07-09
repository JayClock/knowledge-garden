---
title: 简历回答逐字稿：Evidence AI 辅助建模与协同治理
date: 2026-07-03 22:30:00
updated: 2026-07-09 10:45:13
tags:
  - interview/script
  - resume/evidence
  - ai
---

# 简历回答逐字稿：Evidence AI 辅助建模与协同治理

关联：[[简历追问：Evidence AI 辅助建模与协同治理]]、[[Evidence 项目简历描述与面试话术]]、[[15 分钟：Evidence 面试逐字稿]]。

## 30 秒开场

Evidence 里的 AI 我没有设计成“直接替用户改模型”，而是 proposal-first。原因是业务建模会影响概念、关系和后续协作，如果 AI 直接写入模型，用户很难审查它到底改了什么。

所以用户输入自然语言后，后端通过 Pi RPC 调受控 agent，工具范围限制在 `.evidence` 模型目录。前端通过 SSE 展示 reasoning、tool call、tool execution 和最终 proposal。proposal 里是结构化的 add/update/delete entities 和 relationships，用户审查后再决定应用。

## 如果面试官问：为什么不直接让 AI 修改 YAML？

我会说风险主要有三类。

第一是业务风险：AI 可能误解合同、角色和履约关系，直接修改会污染模型。第二是工程风险：AI 可能生成不符合 schema 的 YAML，或者删除重要关系。第三是安全风险：如果工具边界不限制，它可能读写模型目录外的文件。

proposal-first 的好处是 AI 可以提速，但最终变更进入审查态。用户能看摘要、数量、JSON 原文，最好还能看 diff 或 Canvas 预览，再决定是否应用。

## 如果面试官追：proposal 结构长什么样？

我会这样说：

proposal 至少会有几类变更：

```json
{
  "addEntities": [],
  "updateEntities": [],
  "deleteEntities": [],
  "addRelationships": [],
  "updateRelationships": [],
  "deleteRelationships": [],
  "summary": "..."
}
```

每个变更要带 id、类型、字段、理由。删除类变更要特别标红，因为它影响更大。应用前要做 schema 校验、关系完整性校验，比如不能新增一条 source/target 不存在的关系。

## 如果面试官追：工具边界怎么限制？

我会说工具限制是这块的底线。

Pi RPC 启动 agent 时，工作目录限定在当前 workspace 的 `.evidence` 下。工具只开放 read、edit、write、ls、find、grep 这类必要文件工具，不给任意 shell。每个路径都要 canonicalize 后检查是否仍然在允许目录内，防止 `.evidence/../.ssh/config` 这种 path traversal。

另外，AI 即使生成了文件修改，也不应该直接绕过 proposal 应用流程。最终写入要经过服务端校验和用户确认。

## 如果面试官追：SSE 事件流怎么设计？

我会说前端不应该只等最后答案，因为建模过程需要可观察。

后端把 Pi RPC 的事件转换成前端事件，比如：

- reasoning started / chunk
- tool call started
- tool execution started
- tool execution ended
- proposal generated
- agent ended
- error

前端分别展示思考摘要、正在读哪些文件、工具是否成功、最终变更摘要。用户中途取消时，后端要中断 agent 进程或标记 run cancelled，前端状态收敛到 cancelled，而不是一直 loading。

如果 JSON 解析失败，也不能直接丢失过程，应该保留原始输出并提示“proposal 解析失败”。

## 如果面试官追：AI 提出删除 Contract 怎么处理？

我会说删除是高风险变更，不能静默应用。

如果 AI 提出删除现有 Contract 并新建一个 Contract，我会在 proposal 里把 deleteEntities 单独高亮，展示它会影响哪些 relationships 和 Canvas 节点。用户必须明确确认。更稳的做法是默认建议 update 或 rename，而不是 delete + recreate，因为后者会破坏稳定 id 和历史关系。

应用前可以生成快照或依赖 Git diff，应用后如果发现问题可以回滚。

## 如果面试官追：怎么评估 AI 建模质量？

我会说不只看生成成功率。更有用的指标包括：proposal 通过人工审查的比例、被用户修改最多的字段、schema 校验失败次数、关系断裂次数、删除类变更被拒绝比例、用户从需求到可用模型的耗时。

这些能反映 AI 是否真的降低建模成本，而不是只是生成一堆看起来完整的 YAML。

## 收尾句

所以 Evidence 里的 AI 定位是建模加速器，不是模型权威。它可以读取上下文、提出结构化变更、展示过程，但必须保留工具边界、人工审查和回滚空间。

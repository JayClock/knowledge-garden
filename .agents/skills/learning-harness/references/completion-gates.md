# Learning Harness 完成政策

## 五类学习信号

1. **Coverage**：接触到哪些来源范围。
2. **Source Grounding**：至少一个用户选择的关键理解是否经过来源核验。
3. **Distillation**：实际出现的用户命题是否已决定 new／update／skip。
4. **Retrieval**：是否有脱离来源的成功复述、比较或反例测试。
5. **Application**：是否存在真实任务中的成功应用。

这些信号不能压成单一百分比。页数、章节数、知识卡数、链接数和视觉数量都不等于掌握。

## 来源单元完成

来源单元默认只要求：

- `coverage` 为 `read` 或 `revisited`。

没有发生语义动作时：

- `expression_status = not_requested`；
- `evidence_status = not_requested`。

不要为了完成来源单元而要求用户制造复述。Coverage 只回答“读到哪里”，不回答“是否理解”。

## 语义动作完成

当用户明确要核验某个理解、提出候选命题，或 Agent 即将给出来源意义解释时，才进入语义动作：

```text
人类先表达
→ expression_captured
→ Agent 判断是否构成认知起点
→ expression_qualified
→ 对照来源
→ evidence_checked
```

语义动作一旦开始，就必须完成或明确阻塞：

- `qualified` 后才能进行 evidence check；
- `supported` 或 `supported_with_boundary` 表示来源核验完成；
- `partial`、`contradicted`、`blocked` 会继续路由到 `verify-expression`；
- 同一表达可被候选命题检查和沉淀决定复用。

项目默认只要求至少一个用户自己选择的关键理解完成来源核验，不要求每个来源单元都表达。

## 用户命题完成

只有用户实际提出 claim 后才要求沉淀决定：

- `new`：已新建真实知识卡；
- `update`：已更新真实知识卡；
- `skip`：用户明确本轮不沉淀。

没有用户命题的来源单元不制造 `skip` 事件。`new/update` 必须引用真实 artifact；状态记录授权不能替代 Vault 写入授权。

## 检索证据

Retrieval 是新的测试回答，不是新的 Human First Expression。以下成功尝试可以满足项目级 retrieval：

- 合上来源后复述；
- 有明确维度的概念比较；
- 找出反例或适用边界。

只重新浏览笔记不算检索。每次 partial/failure 都保存真实回答和 gap，不覆盖历史。

## 应用证据

只有 `kind=application` 且 `result=success` 的真实任务可以满足 application。写摘要、创建知识卡或生成视觉不会自动成为应用。

## 项目完成

默认政策：

- 所有计划来源单元完成 coverage；
- 至少一个用户选择的关键理解完成来源核验；
- 所有实际注册的用户命题有沉淀决定；
- retrieval 和 application 均有成功证据；
- 没有开放 blocker；
- 用户明确确认 complete。

Reducer 只能报告 `complete_by_policy=true`，不能替用户自动结束项目。

## 计算型与推断型 Sensors

计算型：事件顺序、证据路径、snapshot 重放、完成政策和 TaskNote event seq。

推断型：表达是否来自用户、来源是否支持理解、检索是否成功、应用是否真实，以及失败原因。

脚本不得把“非空文本”直接等同于合格表达，也不得把“有文件”直接等同于成功应用。

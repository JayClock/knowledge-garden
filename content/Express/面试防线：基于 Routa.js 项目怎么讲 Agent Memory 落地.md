---
date: 2026-05-23 10:30:00
updated: 2026-05-27 20:06:00
share: true
---
# 面试防线：基于 Routa.js 项目怎么讲 Agent Memory 落地

如果面试官先看了你做的 [[15分钟：多智能体协同平台|多智能体协同平台]]，再追问 Agent Memory，这一题不要讲成通用 RAG，也不要硬说自己把腾讯云方案 1:1 全复刻了。更稳的说法是：**我把它拆成了当前项目里已经落地的几层能力，并把可恢复、可追踪、可委派这三件事先做扎实。**

## 先给面试官的 30 秒版本

> 我在 Routa.js 里落地的 Agent Memory，不是简单做一个摘要缓存，而是把多智能体执行过程沉淀成可恢复的工程记忆。底层保留原始 trace 和工具调用上下文，中间层做 JSONL 和 digest 归档，上层再把委派关系、子 Agent 启动上下文、完成结果写成 file-backed memory。这样长任务里不是把所有历史一直塞进 prompt，而是让 Agent 在需要时按层回看执行证据、任务摘要和协作状态。

## 用当前项目怎么映射“腾讯云 Agent Memory 分层”

### 第一层：原始证据层

这一层在 Routa 里已经比较完整了。

- 每次工具调用和结果都会被写成 trace。
- 本地模式下 trace 走 JSONL 文件存储，不依赖远端数据库才能恢复。
- Tool call 还会把内容路径、metadata 路径、context 目录写进 trace metadata，保证后续可以按引用回溯完整上下文。

你可以把它讲成：**不是把原文塞进上下文，而是把原文外置成可引用证据。**

对应项目实现可以提：
- `src/core/storage/local-trace-provider.ts`
- `src/core/acp/provider-adapter/trace-recorder.ts`

### 第二层：执行摘要层

腾讯云方案里这一层更强调 offload summary。Routa 当前更像“trace digest + run outcome”。

- 子任务完成后会读取该 session 的 trace。
- 系统会构建 `TraceRunDigest`，提取文件触达、工具调用、错误摘要、验证信号、churn markers。
- 这些摘要不是替代原文，而是给后续 specialist prompt 和复盘提供一个轻量入口。

你可以这样回答：**我们做的不是删历史，而是把历史压成可消费的执行摘要，优先让下游 Agent 读 digest，不够再下钻 trace。**

对应项目实现：
- `src/core/trace/trace-run-digest.ts`
- `src/core/orchestration/orchestrator.ts`

### 第三层：协作记忆层

这是当前项目和普通 Agent Demo 最容易拉开差距的地方。

Routa 不是只有单 Agent 对话，它会把多 Agent 委派过程写成 durable memory：

- `delegation-tree.jsonl`：记录父子委派关系。
- `decisions.md`：记录 ROUTA 为什么把任务委派出去。
- `context-summary.txt`：记录子 Agent 启动时的任务、角色、父节点、provider。
- `implementation-notes.md` / `review-findings.md`：记录子 Agent 的工作上下文。
- `activity-log.jsonl`：记录子 Session 的开始和完成。
- `verification-status.json` / `test-results.json`：记录完成快照。

这层很适合拿来回答：**多智能体系统的 memory 不只是“记住知识”，更重要的是“记住协作过程”。**

对应项目实现：
- `src/core/storage/agent-memory-writer.ts`
- `src/core/storage/__tests__/agent-memory-writer.test.ts`

### 第四层：任务状态与恢复层

腾讯云文章里这里偏向 Mermaid 画布和 metadata。Routa 当前更偏 Workspace / Session / Kanban / Trace 的组合恢复。

- Workspace 是顶层边界，不是全局乱跑。
- Session 是执行线程。
- Kanban 列迁移决定任务处于哪个责任阶段。
- Trace 和 run outcome 决定出了问题后能从哪里恢复。

所以你不要硬说“我们已经做了 Mermaid 无限画布”，更稳的说法是：**我们把任务状态恢复做成了 Kanban + Session + Trace 的组合式状态管理，画布可视化可以继续演进，但恢复入口已经具备。**

## 如果写进简历，可以怎么写

> 设计并实现多智能体执行的分层记忆机制，基于 JSONL trace、trace digest 与 file-backed agent memory，解决长任务执行中上下文膨胀、协作状态丢失和子任务难恢复的问题；将委派关系、子会话上下文、验证结果与执行摘要结构化沉淀，支持多 Agent 任务的可追踪、可恢复和可复盘。

如果你手里已经跑过数据，再补一条量化结果；如果没有稳定数据，就不要编百分比。

## 面试官大概率会怎么追问

### 1. 你这个方案和 RAG 有什么区别？

标准回答：

> RAG 主要解决的是外部知识检索，把知识重新注入上下文；我在这个项目里做的 memory 更偏执行态管理，管理的是 Agent 自己做过什么、调用过什么工具、改过哪些文件、任务怎么委派、验证结果是什么。一个偏知识召回，一个偏过程恢复，两者可以共存。

### 2. 为什么不用单纯的滑动窗口或 summary memory？

标准回答：

> 因为多智能体编程任务的问题不只是 token 超限，而是协作过程会断。单纯滑动窗口只能丢弃历史，summary memory 也容易把委派关系、测试证据、失败重试这些工程上下文抹平。我们这里保留了 trace 原始证据和 file-backed memory，所以摘要不准确时还能按引用回钻，不会永久丢信息。

### 3. 你们的 memory 为什么放文件系统，不直接只放数据库？

标准回答：

> 因为这个项目有 desktop / local-first 诉求。文件化 memory 的好处是本地可恢复、可迁移、可审查，不依赖数据库在线；同时 Web 侧也能继续保留数据库存储。这里不是反数据库，而是把文件系统当成 Agent 执行过程的一等持久化介质。

### 4. 这个方案最大的 trade-off 是什么？

标准回答：

> 最大 trade-off 不是存储成本，而是摘要层和恢复层的一致性维护成本。你做了 trace、digest、agent memory 之后，就要保证这些层之间能相互引用、不会漂移。否则看起来是分层，实际上会变成三套不一致的日志。我们现在的做法是让 digest 和 completion snapshot 都从 trace / task 状态派生，而不是手写第二份真相。

### 5. 你们现在和腾讯云方案相比，还差哪一步？

标准回答：

> 当前项目已经把原始证据、执行摘要、协作记忆、任务恢复这几层打通了，但还没有把任务执行过程完全抽象成 Mermaid 无限画布那种统一可视化记忆载体。现在更偏 Kanban + Session + Trace + file-backed memory。下一步如果继续演进，我会把这些结构再汇总成更轻量、可展开的任务画布视图。

这个回答很关键，因为它体现你有边界感，不会为了显得厉害而乱认领功能。

### 6. 这个方案在多智能体协作里真正解决了什么问题？

标准回答：

> 它解决的不是“模型记不住知识”，而是“团队和 Agent 都记不住执行过程”。一个长任务里会反复读文件、跑命令、失败重试、拆子任务、交给 Review Agent。如果没有分层 memory，后面参与的 Agent 和人类只能看见零散聊天；有了这套结构后，后续节点可以沿着 delegation、digest、trace、verification 逐层恢复现场。

## 更像高级工程师的回答姿势

这题别答成“我做了一个记忆模块”。你要答成四句话：

1. 先承认问题不是知识不足，而是长任务里的执行态失控。
2. 再说明你没有做暴力压缩，而是做了分层外置和可恢复索引。
3. 然后强调多智能体场景里，memory 的核心对象是委派关系、验证结果、文件变更和 trace，而不只是自然语言摘要。
4. 最后诚实说明当前项目已落地到哪一层，哪些还是下一步演进。

## 一句收尾

> 如果让我总结，我在这个项目里做的 Agent Memory，本质上不是让模型“背更多内容”，而是让系统把执行过程变成一种可以被引用、被恢复、被审查的工程记忆。这样多智能体协作到了后半程，靠的不是上下文越堆越长，而是结构化记忆越用越准。
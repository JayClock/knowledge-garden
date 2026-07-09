---
date: 2026-05-30 18:53:11
noteId: 1780277619180
updated: 2026-07-09 20:21:41
---
**层级（Hierarchy），分**。多层委派，父节点管目标，子节点管局部，孙节点继续细分。Hierarchy 和 Orchestrate 容易混，但它们不是一回事。Orchestrate 是一层中心编排多个 worker；Hierarchy 是多层责任分解。Claude Code 的 Subagents、企业里的分层审批、多级 sandbox，都更像 Hierarchy。它的失败模式是隔离没做好：父级上下文泄漏给所有子级，权限继承太宽，低层失败向上雪崩。
---
date: 2026-05-30 18:52:29
noteId: 1780277619129
updated: 2026-07-09 11:00:29
---
**编排（Orchestrate），协**。一个中心节点负责任务拆解、分发和汇总。它适合复杂但仍然能由中心理解全局目标的任务。计划 - 执行（Plan-and-Execute）是典型 Orchestrate：Planner 拆任务，Executor 执行，Planner 或 Synthesizer 汇总。它的失败模式是拆错边界：该选链式的拆成并行，该共享状态的拆成独立，该委派给专家的留在中心硬做。
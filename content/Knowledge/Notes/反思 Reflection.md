---
date: 2026-05-30 17:48:11
noteId: 1780277619196
updated: 2026-07-09 20:21:41
---
反思（Reflection）是**校正预算**。它回答刚才做得对不对，错在哪里，下一步怎么改。

生成批评（Generator-Critic）、自愈循环（Self-Heal Loop）、经验回放 Experience Replay 都属于这一脉。反思的工程价值在于把错误尽早暴露出来，不在于让模型显得更聪明。反思也有失败模式：Self-Critic 容易自我合理化，Loop 容易过度修补，Critic 标准不清会制造伪问题。所以反思必须有终止条件、评价标准和必要时的外部基准事实（Ground Truth）。
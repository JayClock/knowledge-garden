---
title: Agents.md、Prompt Templates 和自定义扩展
date: 2026-06-27
updated: 2026-07-09 20:21:41
tags:
  - AI
  - coding-agent
  - workflow
---

# Agents.md、Prompt Templates 和自定义扩展

Mario 使用 Pi 的一个核心特点是：工具本身很小，但工作流可以被不断塑形。这个塑形主要靠三类东西：Agents.md、Prompt Templates 和自定义扩展。

Agents.md 负责提供项目级上下文。里面可以写沟通风格、代码质量要求、测试命令、Git 操作规则、安全约束、changelog 规范等。比如他会要求模型像“星舰电脑”一样简洁回答，不要说太多客套话；要求改完代码后运行 `npm run check`；要求不要做危险 Git 操作；要求依赖版本必须被锁定；要求 changelog 按固定规则更新。

但他也提醒，Agents.md 不是法律。模型不一定永远遵守它，尤其在长会话里，模型可能会逐渐忘记某些细节。比如“不使用 inline import”这类规则，模型经常会违反，因为训练数据里这种写法太常见。所以 Agents.md 更像是降低错误概率的提示，而不是最终保障。最终保障仍然要靠 lint、typecheck、pre-commit 和 CI。

Prompt Templates 则负责把高频流程固化下来。比如 `/is` 用来处理 issue：读取 GitHub issue、打标签、分配、复现、分析、给出结论。`/wrap` 用来收尾：更新 changelog、写 GitHub 评论、commit、push、关闭 issue。它们不是复杂系统，而是把一串重复指令封装成可复用入口，让 Agent 每次都按相似流程工作。

这类模板的价值在于把“隐性习惯”变成“显性流程”。以前人会凭经验记得修完 bug 要补 changelog、要评论 issue、要跑检查。现在这些步骤变成模板，Agent 就可以自动完成，人只需要判断内容是否正确。

自定义扩展则解决更个性化的问题。Mario 演示了几个很小但很实用的扩展：一个是在终端底部显示当前会话关联的 issue 信息；一个是 diff review 工具，可以在 diff 上写行内反馈，再把反馈送回 Agent；还有一个 comment 扩展，可以把 Agent 上一条长回答打开到外部编辑器里，人直接在文本里批注，然后重新注入会话。

这些扩展都不复杂，但非常贴合个人工作流。也正是这种设计让 Pi 显得特别：它不是预设一整套“正确工作流”，而是提供一个足够小的核心，让用户和 Agent 一起把需要的工具长出来。

这背后有一个更大的判断：未来的软件可能越来越多是可自我修改的。不是所有功能都必须由框架作者内置。如果一个扩展只需要几分钟就能让 Agent 写出来，并且只服务于某个人的工作习惯，那就没有必要把它做成庞大的通用功能。

所以 Agents.md、Prompt Templates 和扩展，分别对应三层能力：规则、流程和工具。规则告诉 Agent 该遵守什么，流程告诉 Agent 该怎么推进，工具让人和 Agent 的协作变得更顺手。

相关：Mario 的日常 AI 编程工作流、如何让 Agent 不把代码库写烂、大代码库里如何管理上下文

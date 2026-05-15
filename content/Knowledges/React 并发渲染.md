---
date: 2026-03-09T16:50:55
updated: 2026-05-15 10:03:23
share: true
in:
  - "[[Maps]]"
---
React 并发渲染不适合被理解成“React 终于异步了”，更适合理解成：React 开始能够区分不同更新的轻重缓急，并按优先级调度它们，从而优先保证用户当下最重要的反馈。

 一条主线

[[./React Fiber|React Fiber]] -> [[../Cards/React-useTransition|useTransition]] / [[../Cards/React-useDeferredValue|useDeferredValue]] / [[../Cards/React-useOptimistic|useOptimistic]] / [[./React-useActionState|useActionState]]

如果说 [[./React Hooks|React Hooks]] 讲的是函数组件能力如何升级，那么这张图讲的是：当 React 进入并发语义后，交互体验是如何被重新组织的。

 第一层：为什么需要并发渲染

先看 [[./React Fiber|React Fiber]]。

它解决的核心问题是：

- 更新太重时会阻塞主线程
- 用户输入和关键反馈可能被拖慢
- React 需要有能力区分“现在必须做”和“可以稍后做”

所以并发渲染的重点不是“更炫的底层实现”，而是：

- 让高优先级更新先发生
- 让低优先级更新不要拖累当前交互

 第二层：调度哪些更新该先发生

 [[../Cards/React-useTransition|useTransition]]

适合：

- 把某些非紧急更新标记为过渡更新
- 优先保证输入、点击、焦点切换等即时反馈

它关注的是：

- 哪批更新应该后让一步

 [[../Cards/React-useDeferredValue|useDeferredValue]]

适合：

- 输入值要立刻变化
- 但依赖这个值的重区域可以晚一点更新

它关注的是：

- 哪个值的传播和消费可以慢一点

 第三层：不只调度优先级，还调度反馈节奏

 [[../Cards/React-useOptimistic|useOptimistic]]

适合：

- 写操作成功概率高
- 用户希望立刻看到结果
- 例如点赞、发消息、提评论

它关注的是：

- 用户应该先看到什么反馈

 [[./React-useActionState|useActionState]]

适合：

- 表单动作执行后的结果状态组织
- 成功、失败、提交中这些状态围绕 action 聚合

它关注的是：

- 动作完成后，结果状态如何自然落地

 三个维度区分

可以这样区分这几个 Hook：

- [[../Cards/React-useTransition|useTransition]]
 解决“哪些更新该先发生”
- [[../Cards/React-useDeferredValue|useDeferredValue]]
 解决“哪些值可以晚一点传播”
- [[../Cards/React-useOptimistic|useOptimistic]]
 解决“用户应该先看到什么反馈”
- [[./React-useActionState|useActionState]]
 解决“动作执行后的结果状态怎么组织”

 一个更准确的理解

React 并发渲染不是让开发者“异步写 UI”，而是给开发者更多能力去表达：

- 什么最紧急
- 什么可以延后
- 什么需要先反馈
- 什么应该围绕 action 的结果组织

这背后真正的基础仍然是 [[./React Fiber|React Fiber]] 的调度能力。

 相关笔记

- [[./React Hooks|React Hooks]]
- [[./React Fiber|React Fiber]]
- [[./React-useSyncExternalStore|useSyncExternalStore]]
- [[../Express/渐进式集成：从浏览器渲染到框架设计的统一哲学|渐进式集成：从浏览器渲染到框架设计的统一哲学]]

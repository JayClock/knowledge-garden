---
date: 2025-05-05T11:14:49
updated: 2026-05-15 12:17:48
share: true
noteId: 1778807092431
---
React Fiber 的核心作用和使用场景是什么？

---

`React Fiber` 是 React 为了解决“复杂更新会长时间阻塞主线程”而重写出来的协调架构。它不是一个单独可用的 API，而是并发渲染、优先级调度、Suspense、`useTransition` 这些能力的底层前提。

 它解决什么问题

浏览器的主线程既要执行 JavaScript，也要处理输入、布局和绘制。

如果一次 React 更新太重，就会出现：

- 用户输入卡顿
- 页面反馈变慢
- 长任务阻塞渲染

在早期 React 的同步协调模型里，一次更新开始后，很难中断。组件树一大、某些节点一重，整个渲染过程就可能把主线程占住。

Fiber 解决的核心问题就是：

**能不能把渲染工作拆小、排序、暂停、恢复，并优先处理更重要的更新。**

 一句话理解

Fiber 让 React 从“同步一路算到底”的更新模型，升级为“可拆分、可抢占、按优先级调度”的更新模型。

这里增强的是“渲染调度能力”。

 为什么它重要

Fiber 不是为了“让所有渲染都异步”，而是为了让 React 有能力区分不同更新的轻重缓急。

例如：

- 用户输入要优先响应
- 列表过滤可以稍后完成
- 首屏之外的内容可以延迟
- 副作用和 DOM 提交必须保持一致性

这也是为什么后来的这些能力都和 Fiber 强相关：

- [[../Cards/React-useTransition|useTransition]]
- [[../Cards/React-useDeferredValue|useDeferredValue]]
- Suspense
- 流式 SSR
- 选择性 hydration

 一个直观例子

假设页面正在渲染一个很重的列表，这时用户点击了输入框。

如果 React 只能同步一路算完：

- 输入反馈会被阻塞

如果 React 能把工作分片并调度：

- 低优先级列表更新可以先让开
- 输入相关更新优先执行
- 用户先看到最重要的反馈

这就是 Fiber 想达到的效果。

 Fiber 到底做了什么

可以先抓住 4 个关键点：

1. 把组件更新拆成更细的工作单元
2. 为这些工作单元附带调度信息
3. 允许高优先级任务打断低优先级任务
4. 在最终提交时，仍然保证 DOM 更新的一致性

所以 Fiber 不是单纯的数据结构，而是一整套“可中断协调 + 同步提交”的架构。

 两个阶段

 1. Render / Reconciliation 阶段

这一阶段的目标是：

- 计算出下一棵 UI 树应该长什么样
- 标记哪些节点需要插入、更新、删除

这一阶段可以被打断、恢复、重做。

也正是在这一层，React 才有机会做优先级调度。

 2. Commit 阶段

这一阶段的目标是：

- 把前面算好的修改真正提交到 DOM
- 执行布局相关和副作用相关逻辑

这一阶段必须保持同步和一致，不能随便中断。

所以 Fiber 不是“什么都可中断”，而是：

- 计算阶段可调度
- 提交阶段必须稳定

 为什么会影响 Hooks

Fiber 不只是影响调度，也反过来影响了 [[./React Hooks|React Hooks]] 的设计和运行方式。

 Hook 为什么强调调用顺序

Hooks 依赖稳定的调用顺序，React 才能在 Fiber 对应的组件工作单元上，把每个 Hook 的状态槽位正确对应起来。

这就是为什么：

- 不能在条件里调用 Hook
- 不能在循环里调用 Hook
- 必须保证顺序稳定

 为什么副作用分成不同阶段

像 [[./React-useEffect|useEffect]] 和 [[../Cards/React-useLayoutEffect|useLayoutEffect]] 的差异，本质上也和 Fiber 的提交顺序有关：

- `useEffect` 更偏向提交后的异步副作用
- [[../Cards/React-useLayoutEffect|useLayoutEffect]] 更靠近 DOM 变更后的同步布局阶段

 为什么会有并发相关 Hook

[[../Cards/React-useTransition|useTransition]]、[[../Cards/React-useDeferredValue|useDeferredValue]] 这些能力，本质上是在利用 Fiber 的调度系统，让不同更新进入不同优先级通道。

 和优先级的关系

可以粗略把 Fiber 的调度理解成：

- 特别紧急的更新优先
- 用户交互相关的更新优先
- 普通状态更新随后
- 可推迟的更新延后
- 空闲任务放到最后

这也是为什么：

- `flushSync` 很重，但有时必须同步
- 输入响应必须足够快
- [[../Cards/React-useTransition|useTransition]] 适合把“能晚一点”的 UI 放后面

 Fiber 节点可以怎么理解

如果不深究实现细节，可以把一个 Fiber 节点理解成：

- 某个组件或元素的工作描述
- 里面不仅有类型、props、state
- 还带着这次更新需要的调度和副作用信息

它让 React 不只是“知道 UI 长什么样”，还“知道这份工作该怎么被调度”。

 一个常见误区

很多人会把 Fiber 理解成“React 变成了多线程”。

这不准确。

更准确的说法是：

- React 仍然主要运行在单线程 JavaScript 环境里
- Fiber 做的是更细粒度的任务拆分与调度
- 它让主线程上的工作更容易被安排，而不是平白多出线程

 和其它笔记的关系

- 在 [[./React Hooks|React Hooks]] 里，Fiber 是并发渲染和 Hook 调度的底层背景
- 在 [[./React-useEffect|useEffect]] 里，可以继续连接到副作用提交时机
- 在 [[../Express/渐进式集成：从浏览器渲染到框架设计的统一哲学|渐进式集成：从浏览器渲染到框架设计的统一哲学]] 里，它对应“按优先级渐进渲染”的框架实现
- 在 [[./React-useSyncExternalStore|useSyncExternalStore]]、[[../Cards/React-useTransition|useTransition]]、[[../Cards/React-useDeferredValue|useDeferredValue]] 这些能力里，可以继续看到 Fiber 的调度影响

## 拆分卡片

- [[../Cards/React Fiber 把同步协调升级为可中断调度|React Fiber 把同步协调升级为可中断调度]]
- [[../Cards/Fiber 让高优先级更新可以打断低优先级渲染|Fiber 让高优先级更新可以打断低优先级渲染]]
- [[../Cards/Fiber 的提交阶段仍然必须保持同步一致|Fiber 的提交阶段仍然必须保持同步一致]]
- [[../Cards/Fiber 是 Suspense 和并发特性的基础|Fiber 是 Suspense 和并发特性的基础]]

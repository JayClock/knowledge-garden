---
title: 简历回答逐字稿：监控 SDK 架构与插件化设计
date: 2026-07-03 22:30:00
updated: 2026-07-09 10:45:13
tags:
  - interview/script
  - resume/sdk
---

# 简历回答逐字稿：监控 SDK 架构与插件化设计

关联：[[简历追问：监控 SDK 架构与插件化设计]]、[[15分钟：前端埋点与监控 SDK]]。

## 30 秒开场

我做这个监控 SDK 时，重点不是做一个大而全的数据平台，而是做一套业务前端愿意接、接了以后不容易出问题的采集基础设施。

所以架构上我拆成 core 包和适配包。core 负责上下文、队列、上报、插件生命周期、错误隔离；React、Vue、Vanilla 适配包只负责框架接入。业务事件尽量声明式采集，比如通过 `data-track-event` 表达业务语义，SDK 负责事件发现、上下文补齐、队列和降级上报。

## 如果面试官问：为什么不直接提供 `track()`？

我会说 `track()` 一定需要，但不能只靠它。

纯手动 `track()` 很灵活，但长期容易污染业务代码，也容易漏埋、误删、重复上报。尤其是低代码页面、动态列表、弹窗和微前端场景，业务函数里到处插埋点很难维护。

所以我采用“声明式为主，编程式补充”。常规点击、曝光用声明式事件，让业务声明“这是 submit_form”这类稳定语义；复杂业务成功、异步结果、后端返回后的转化事件，可以手动 `track()`。

## 如果面试官追：core 包和适配包怎么拆？

我会这样说：

core 不依赖 React/Vue，它只提供：

- SDK 初始化和配置。
- 公共上下文管理，比如 user、tenant、session、route、app version。
- 事件队列和上报通道。
- 插件注册、执行和 teardown。
- 错误隔离和远程开关。

React 适配包可以提供 hook 或 Provider，自动接路由上下文；Vue 适配包可以提供 plugin install；Vanilla 只提供直接初始化。这样 core 体积更可控，也避免为了某个框架引入额外依赖。

## 如果面试官追：插件接口怎么设计？

我会说插件不是随便执行一段代码，应该有生命周期：

```ts
type MonitorPlugin = {
  name: string
  setup(ctx): void
  teardown?(): void
  onEvent?(event): event | void
  beforeSend?(batch): batch
  onError?(error): void
}
```

比如点击采集、曝光采集、Web Vitals、Fetch/XHR 监控都可以是插件。每个插件内部出错不能影响主业务，也不能影响其他插件。SDK 会在插件调用外层做隔离，插件失败最多丢监控，不拖垮页面。

## 如果面试官追：声明式点击怎么不漏？

我会说我不会给每个元素单独绑监听器，而是在 document 或应用 root 上做事件委托。

点击事件冒泡后，用 `event.composedPath()` 找到最近的 `data-track-event` 节点。这样 React/Vue 动态渲染、节点销毁重建都不需要重新绑定。对于 Shadow DOM、iframe、微前端，要根据容器边界单独接入，不能假设一个 document 能覆盖所有上下文。

事件 payload 里会补公共上下文，比如 route、tenant、session、app version。业务方只需要声明事件语义和少量扩展字段。

## 如果面试官追：微前端重复初始化怎么办？

我会说这是实际接入里必须处理的问题。

主应用和子应用都可能初始化 SDK，所以要有 instance id、app id 和 namespace。可以让主应用提供公共上下文，子应用只注册自己的 app context；上报时用幂等 id 或 event id 做去重。更重要的是约定谁负责全局事件监听，避免主子应用各绑一套导致重复采集。

如果 iframe 跨域，就不能直接读上下文，要通过 postMessage 传递有限的上下文字段，并做来源校验。

## 收尾句

所以这个 SDK 的核心不是一个 `track()` 方法，而是一套低侵入、可插件化、可隔离、可降级的采集运行时。它让业务表达事件语义，SDK 负责稳定采集和可靠上报。

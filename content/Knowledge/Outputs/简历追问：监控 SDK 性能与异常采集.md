---
title: 简历追问：监控 SDK 性能与异常采集
date: 2026-07-03 22:00:00
updated: 2026-07-09 10:45:13
tags:
  - interview/follow-up
  - resume/sdk
  - observability
---

# 简历追问：监控 SDK 性能与异常采集

关联：[[全栈工程师简历#全链路埋点与监控 SDK]]、[[15分钟：前端埋点与监控 SDK]]、[[SDK 异常劫持会不会影响主业务的正常请求]]、[[sendBeacon 失败时的降级与兜底策略]]。

## 对应简历描述

> 构建了全方位的性能与异常数据采集方案，利用底层 API 结合全局事件拦截，全面覆盖 FCP、LCP、CLS 等核心 Web Vitals 性能指标以及复杂的 JavaScript 运行期异常。

## 面试官真正想确认

你是否理解浏览器观测 API 的边界和 SDK “Do No Harm” 原则，而不是简单监听 `error` 和覆写 `fetch`。

## 连续追问链

### 1. Web Vitals

- FCP、LCP、CLS 分别用哪些 PerformanceObserver entry？是否开启 `buffered`？
- SPA 路由切换后，LCP 和首屏指标如何定义？是只统计首次加载还是每个 route view？
- CLS 如何定位具体元素？布局抖动和用户交互导致的变化如何区分？
- 指标上报时带哪些上下文：route、app version、device、network、tenant？

### 2. 异常类型

- `window.onerror`、`unhandledrejection`、资源加载错误分别覆盖什么？
- Promise rejection 如果 reason 不是 Error，如何标准化？
- Fetch/XHR 的 HTTP 500、网络失败、AbortController 主动取消是否都算异常？
- 跨域脚本 `Script error` 如何处理 sourcemap 和 CORS？

### 3. 劫持安全

- 覆写 fetch 时如何保留原生 Promise、headers、body stream、AbortController 语义？
- 为什么读取 response body 可能破坏业务？什么时候必须使用 `response.clone()`？
- SDK 自己抛错时如何旁路，确保主业务请求继续执行？

### 4. 性能与上报

- SDK 加载时机如何避免影响首屏？哪些插件可以延迟初始化？
- 指标、异常、业务事件如何采样、去重、批量上报？
- 页面卸载时 sendBeacon 失败、payload 超限、离线分别怎么降级？

## 场景推演题

> 一个接口请求被用户切换页面时 AbortController 取消了，同时 SDK 代理了 fetch。这个事件要不要上报成接口异常？你如何判断它不是服务端故障？

继续追：同一个 SPA 页面路由切换后 LCP 指标很差，你怎么定义采集口径？

## 准备证据

- Web Vitals 采集代码片段或 API 列表。
- Fetch/XHR 代理安全清单。
- 异常标准化后的事件 payload。
- 弱网、卸载、Abort 的回放测试用例。

## 容易露馅的回答

- “监听全局 error 就能覆盖异常。”
- “所有非 2xx 都算错误。”
- “SDK 不影响性能，因为代码很少。”
- “覆写 fetch 后直接读取 response.json() 上报。”

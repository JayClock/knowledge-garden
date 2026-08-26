---
title: 简历追问：监控 SDK 性能与异常采集
date: 2026-07-03 22:00:00
updated: 2026-08-26 08:30:30
tags:
  - interview/follow-up
  - resume/sdk
  - observability
---

# 简历追问：监控 SDK 性能与异常采集

关联：[[15分钟：前端埋点与监控 SDK]]、[[简历回答逐字稿：监控 SDK 性能与异常采集]]、[[1.需求评审、项目架构设计与上报数据盘点]]。

## 对应简历描述

> 使用 PerformanceObserver、Web Vitals、全局异常监听及 Fetch／XHR、DOM、导航代理统一采集性能、异常、接口与操作数据，通过本地队列控制批量上报，并以 Sourcemap 还原生产堆栈。

## 面试官真正想确认

你是否理解浏览器观测 API、代理安全、上报队列和 Sourcemap 链路，并遵守监控 SDK 的“不能伤害主业务”原则。

## 连续追问链

### 1. Web Vitals

- FCP、LCP、CLS、TTFB 和 INP 分别反映什么体验？
- PerformanceObserver 回调为什么要保持轻量？
- SPA 路由指标与浏览器原生首屏指标怎样区分？
- 指标事件需要携带哪些页面、设备和版本上下文？

### 2. 异常采集

- 全局 error、`unhandledrejection` 和业务自定义错误分别覆盖什么？
- Promise rejection 的 reason 不是 Error 时怎样标准化？
- 请求状态、运行期异常和业务异常为什么不能混成一种事件？

### 3. 代理安全

- Fetch／XHR 代理怎样保留原始参数、返回值和错误语义？
- 为什么直接读取 response body 可能破坏业务？
- SDK 自身抛错时怎样确保原请求继续执行？

### 4. 上报队列

- 为什么不能每个事件都发一个请求？
- 时间间隔、数量阈值和路由变化三种触发方式如何取舍？
- 失败重试怎样控制节奏？
- `sendBeacon`、IndexedDB 离线续传是否有当前项目证据？

### 5. Sourcemap

- 生产堆栈为什么不能直接定位源码？
- 构建版本、产物文件和 Sourcemap 怎样匹配？
- 为什么映射文件不应直接暴露给终端用户？

## 场景推演题

> 业务接口正常返回，但 SDK 的 Fetch 代理在记录耗时时抛出异常。请说明怎样保证业务 Promise 和返回值不受影响，同时记录或降级 SDK 自身错误。

继续追：如果监控平台只有压缩产物的行列号，怎样找到对应源码？

## 准备证据

- 项目范围以候选人确认和 [[企业级监控平台全栈架构设计与实践面试专项突击]] 为准，准备 Web Vitals、异常、Fetch／XHR、队列和 Sourcemap 的原文说明。
- `miaoma-monitor` 作为代表性内部重实现，可辅助展示 PerformanceObserver、全局异常、Promise rejection 和 HTTP Transport 等机制；代码范围不要求与原项目逐项一致。

## 容易露馅的回答

- “监听全局 error 就覆盖所有异常。”
- “覆写 fetch 后直接读取 response.json()。”
- “每条事件实时发送最准确。”
- 把 `sendBeacon`、离线续传和具体故障案例说成已经完成。

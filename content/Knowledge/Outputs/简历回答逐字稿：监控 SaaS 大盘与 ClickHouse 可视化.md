---
title: 简历回答逐字稿：监控 SaaS 大盘与 ClickHouse 可视化
date: 2026-07-03 22:30:00
updated: 2026-10-03 11:16:32
tags:
  - interview/script
  - resume/sdk
  - data
---

# 简历回答逐字稿：监控 SaaS 大盘与 ClickHouse 可视化

关联：[[简历追问：监控 SaaS 大盘与 ClickHouse 可视化]]、[[15分钟：前端埋点与监控 SDK]]。

## 30 秒开场

作为端侧监控 SDK 负责人，我从下游分析与排障需求倒推事件模型与上下文契约。在 AI Flow 中，通过 `executionId` 关联校验、测试运行、发布事件与底层执行引擎日志；与后端及数据团队分工协作，由他们承接 Kafka、ClickHouse 存储与大盘展现。

## 如果面试官问：为什么 SDK 需要理解下游怎样消费？

如果只从浏览器能够采什么出发，容易得到大量无法支持判断的数据。AI Flow 的验收需要区分用户是在校验、测试运行还是发布环节失败，所以我为这些路径设计自定义事件；节点状态、耗时和错误仍由执行引擎日志记录，再通过 `executionId` 关联。

这种自底向上的设计思路，保证了端侧采集的每个字段都能精准匹配下游的分析诉求。

## 如果面试官问：ClickHouse 表怎么设计？

在与数据团队协同制定事件协议时，重点保证字段设计满足高效的多维分析与时序聚合。一个通用的监控事件模型通常包含：

- `event_time`
- `app_id`
- `tenant_id`
- `version`
- `route`
- `session_id`
- `user_id`
- `event_type`
- `metric_name`
- `metric_value`
- `trace_id`
- `payload`

在协作中，结合 ClickHouse 按日期分区、主键稀疏索引和低基数字段压缩的特性，端侧提供稳定规范的枚举与标识，减少后端的清洗成本。

## 如果面试官追：怎么查 LCP p75 或接口耗时 p95？

分位数比平均值更适合观察体验尾部，但查询实现不属于我的个人交付。下面的 SQL 只用于说明 SDK 字段怎样被下游消费：

```sql
SELECT
  app_id,
  version,
  route,
  quantile(0.75)(metric_value) AS lcp_p75
FROM events
WHERE event_time >= now() - INTERVAL 1 DAY
  AND event_type = 'web_vital'
  AND metric_name = 'LCP'
GROUP BY app_id, version, route
ORDER BY lcp_p75 DESC
LIMIT 100
```

这说明 SDK 上报的 `app_id`、`version`、`route`、指标名和指标值需要保持稳定口径，才能有力支持下游计算分位数分布。

## 如果面试官追：数据量大了查询慢怎么办？

从整体架构视角看，面对海量数据时，通常采用排序键过滤、物化视图预聚合、冷热数据分层以及明细/指标分离存储等方案来保障查询的高性能。

## 如果面试官追：指标口径怎么保证可信？

指标口径是大盘很容易被忽略的部分。

比如“错误率”要明确分母是请求数、会话数还是页面访问数；Abort 请求是否算错误；采样后如何还原；同一个错误是否去重；SPA 路由切换算不算一次页面访问。

从 SDK 协作角度，我会在协议中区分事件类型和必要上下文，并与下游确认 Abort、SPA 路由、采样和去重口径。

## 如果面试官追：多租户权限怎么做？

多租户查询安全必须由服务端和网关层依据当前身份强制限制查询范围，SDK 端侧仅作为租户上下文的透传方，保障租户间数据隔离。

## 收尾句

这体现了全链路协作的价值：端侧负责产生稳定、可解释、可关联的证据契约，后端负责高效存储与计算展现，共同打通企业级可观测性闭环。

---
title: 简历回答逐字稿：监控 SaaS 大盘与 ClickHouse 可视化
date: 2026-07-03 22:30:00
updated: 2026-07-09 10:45:13
tags:
  - interview/script
  - resume/sdk
  - data
---

# 简历回答逐字稿：监控 SaaS 大盘与 ClickHouse 可视化

关联：[[简历追问：监控 SaaS 大盘与 ClickHouse 可视化]]、[[15分钟：前端埋点与监控 SDK]]。

## 30 秒开场

监控大盘这块，我不会把重点放在“图表好看”上。真正难的是指标口径、数据模型和查询性能。SDK 把业务事件、性能事件、异常事件采回来以后，如果大盘不能按应用、版本、租户、路由、会话这些维度稳定查询，产品和研发也很难信它。

所以我用 React 和 shadcn/ui 做控制台，用 ClickHouse 承接大规模事件查询。前端大盘负责把错误率、接口耗时、Web Vitals、业务漏斗这些指标可视化，但每个图背后都要有清楚的统计口径。

## 如果面试官问：ClickHouse 表怎么设计？

我会说监控事件一般适合宽表或按事件类型分表，具体取决于量级和查询模式。一个基础事件表会包含：

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

ClickHouse 里 partition 通常按日期，order by 会优先考虑查询最常用的维度，比如 app、event type、time。低基数字段可以用 LowCardinality。高基数字段，比如完整 URL、userId、traceId，要谨慎放排序键，否则会影响压缩和查询性能。

## 如果面试官追：怎么查 LCP p75 或接口耗时 p95？

我会这样说：

这类指标不能用平均值糊弄，通常看分位数。ClickHouse 可以用 `quantile(0.75)(value)` 查 LCP p75，用 `quantile(0.95)(duration)` 查接口耗时 p95。

比如按 app、version、route 聚合过去 24 小时 LCP：

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

大盘上展示 p75/p95，比展示平均值更能反映用户体验尾部问题。

## 如果面试官追：数据量大了查询慢怎么办？

我会说先看查询模式和表设计，不会只说“ClickHouse 很快”。

常见优化包括：时间范围必须收敛；order by 是否匹配过滤条件；高基数字段是否拖累；是否需要物化视图或预聚合表；热门大盘是否加缓存；明细查询和聚合查询是否分开。

比如实时大盘不应该每个用户打开页面都直接扫原始大表，可以按分钟预聚合，前端定时刷新聚合结果。点击某个异常点再下钻到明细样本。

## 如果面试官追：指标口径怎么保证可信？

我会说这是大盘最容易被忽略的地方。

比如“错误率”要明确分母是请求数、会话数还是页面访问数；Abort 请求是否算错误；采样后如何还原；同一个错误是否去重；SPA 路由切换算不算一次页面访问。

我会在大盘里尽量展示口径说明，比如“当前错误率不包含用户主动取消请求”“LCP 为首次页面加载口径”。如果数据被采样，也要提示采样率。否则图表再好看也会误导决策。

## 如果面试官追：多租户权限怎么做？

我会说监控数据也属于业务数据，不能因为是日志就忽略权限。查询 API 必须带当前用户和租户上下文，后端在查询条件里强制加 tenant/app 范围。前端选择器只是 UI，不能作为权限边界。

运营、研发、客户管理员看到的数据范围应该不同，尤其是 SaaS 场景不能跨租户泄露。

## 收尾句

所以这块我想表达的是，我不是只搭了一个图表页面，而是把 SDK 采集上来的事件变成可查询、可解释、可下钻的数据反馈链路。大盘可信，前面的采集才有业务价值。

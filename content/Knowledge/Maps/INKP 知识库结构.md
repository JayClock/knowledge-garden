---
date: 2026-07-09 10:35:11
updated: 2026-07-09 11:00:29
---
# INKP 知识库结构

> 这篇是当前库的 INKP 目录地图，用来说明各目录的职责边界。

## 目录映射

| INKP | 当前目录 | 职责 |
|---|---|---|
| I / Inbox | `Inbox/` | 临时收集、未处理输入、剪藏内容 |
| N / Note | `Knowledge/Notes/` | 概念笔记、术语笔记、知识点笔记 |
| K / Knowledge | `Knowledge/Maps/` | 主题笔记、知识地图、MOC |
| P / Project | `TaskNotes/Projects/` | 项目、行动计划、阶段复盘 |

## 辅助目录

| 目录 | 职责 |
|---|---|
| `Knowledge/Sources/` | 来源材料、原文笔记、书籍/文章摘录 |
| `Knowledge/Outputs/` | 输出层：观点稿、面试回答、文章草稿、论述型输出 |
| `TaskNotes/Tasks/` | 短期任务、一次性待办 |
| `Knowledge/Assets/` | 图片、Excalidraw、脚本、附件资源 |
| `Knowledge/Meta/` | 迁移日志、结构说明、维护记录 |

## 流动规则

```text
Inbox
  ↓ 整理、筛选、补全来源
Sources
  ↓ 提炼概念
Notes
  ↓ 组织主题
Maps
  ↓ 形成表达或行动
Outputs / Projects
  ↓ 复盘反馈
Notes / Maps
```

## 使用原则

- 新剪藏、临时材料先进入 `Inbox/`。
- 原文、书摘、视频稿、外部资料进入 `Knowledge/Sources/`。
- 一个概念、机制、模型或术语进入 `Knowledge/Notes/`。
- 一个主题、领域、问题地图进入 `Knowledge/Maps/`。
- 需要输出给别人看的论述、面试话术、文章草稿进入 `Knowledge/Outputs/`。
- 图片、Excalidraw、脚本和附件资源进入 `Knowledge/Assets/`。
- 迁移日志、结构说明和维护记录进入 `Knowledge/Meta/`。
- 有明确目标、周期和复盘的事情进入 `TaskNotes/Projects/`。

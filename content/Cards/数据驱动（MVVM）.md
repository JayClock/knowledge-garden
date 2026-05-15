---
date: 2024-10-14T14:38:51
updated: 2026-05-15 09:58:44
share: true
noteId: 1778807089047
---
数据驱动（MVVM） 中“如何理解数据驱动（MVVM）”的关键方法是什么？

---

传统软件开发，都是静态渲染，更新还要操作 DOM。通过 MVVM 可以让开发人员专注于业务数据本身，而不是如何操作 DOM 上。
# 如何理解数据驱动（MVVM）
MVVM 表示的是 Model - View - ViewModel
- Model：模型层，负责处理业务逻辑以及和服务端的交互
- View：视图层，负责将数据模型转化为 UI 展示出来，可以简单理解为 [[HTML|HTML]] 页面
- ViewModel: 视图模型层，用来连接 Model 和 View，是 Model 和 View 之间的桥梁
## 理解 ViewModel
数据变化后更新视图、视图变化后更新数据
- 监听器（Observer）：对所有数据的属性进行监听
- 解析器（Compiler）：对每个元素节点的指令进行扫描和解析，根据指令模板替换数据，以及绑定响应的更新数据

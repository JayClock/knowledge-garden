---
date: 2025-04-16T13:14:31
updated: 2026-03-09 16:48:21
share: true
in:
  - "[[Maps]]"
---
React Hooks 不适合只按“API 清单”去记，更适合按 [[./渐进增强|渐进增强]] 的方式理解：函数组件先获得最基础的状态能力，再逐步获得派生能力、引用能力、副作用能力、共享能力、并发调度能力和抽象复用能力。

## 一条渐进增强的主线

[[../Cards/React-useState|useState]] -> [[React-useReducer|useReducer]] -> [[../Cards/React-useRef|useRef]] -> [[../Cards/React-useEffect|useEffect]] -> [[../Cards/React-useContext|useContext]] -> [[../Cards/React-useSyncExternalStore|useSyncExternalStore]] -> [[../Cards/React-useTransition|useTransition]] / [[../Cards/React-useDeferredValue|useDeferredValue]] / [[../Cards/React-useOptimistic|useOptimistic]] -> 自定义 Hooks

如果把 [[./React 状态管理|React 状态管理]] 看成“状态如何升级”，那么 React Hooks 可以看成“函数组件的能力如何升级”。

## 为什么需要 Hooks

Hooks 的出现，本质上是为了让函数组件逐步具备过去类组件才有的能力：

- 保存状态
- 响应状态变化并重新渲染
- 执行副作用
- 访问 DOM 和可变引用
- 复用状态逻辑

它解决的不是“语法糖”问题，而是函数组件如何在保持声明式风格的前提下，承载越来越复杂的 UI 逻辑。

## 第一层：先让函数组件有状态

### [[../Cards/React-useState|useState]]

这是 Hook 体系的起点。

适合：

- 管理局部状态
- 处理输入、开关、展开收起、分页等简单交互
- 用最小成本让函数组件变成有状态组件

这里增强的是“记住值”的能力。

### [[React-useReducer|useReducer]]

当状态逻辑变复杂时，从 `useState` 进一步升级到 `useReducer`。

适合：

- 多字段状态联动
- 状态迁移明显
- 更新依赖前一个状态

这里增强的是“组织状态变更”的能力。

## 第二层：让组件拥有稳定引用和派生结果

### [[../Cards/React-useRef|useRef]]

适合：

- 访问 DOM
- 保存不参与渲染的可变值
- 在多次渲染之间保留引用

这里增强的是“跨渲染保持引用”的能力。

和它相关的还有 [[../Cards/react-forwardRef|forwardRef]] 与 [[../Cards/React-useImperativeHandle|useImperativeHandle]]，主要用于 [[../Cards/React 组件通信方式|父子组件传递]] 中的实例暴露。

### [[../Cards/React-useMemo|useMemo]]

适合：

- 缓存昂贵计算结果
- 稳定派生值
- 避免每次渲染重复做相同计算

这里增强的是“派生结果复用”的能力。

### [[../Cards/React-useCallback|useCallback]]

适合：

- 稳定函数引用
- 配合 `memo` 或依赖数组减少无意义更新
- 避免把“函数每次都变”传递给下游组件

这里增强的是“函数身份稳定”的能力。

`useMemo` 和 `useCallback` 不是默认应该上的优化，而是在引用稳定性已经成为问题时，再做增强。

相关补充：

- [[../Cards/React-useId|useId]]：用于生成稳定且适合无障碍关联的唯一 ID

## 第三层：组件开始和外部世界同步

### [[../Cards/React-useEffect|useEffect]]

当组件不再只是“根据 state 渲染 UI”，而是要与外部系统交互时，就会进入副作用阶段。

适合：

- 请求数据
- 订阅事件
- 同步浏览器 API
- 操作非 React 管理的外部系统

这里增强的是“渲染之后与外部世界对接”的能力。

相关延伸：

- [[../Cards/React-useLayoutEffect|useLayoutEffect]]：在 DOM 更新后、浏览器绘制前同步执行，适合布局测量和同步 DOM 操作
- [[useEffect 的底层是如何实现的|useEffect 的底层是如何实现的]]：理解副作用调度机制

## 第四层：状态和能力开始跨组件共享

### [[../Cards/React-useContext|useContext]]

适合：

- 在组件树中共享数据
- 避免多层 `props drilling`
- 提供主题、用户信息、语言、配置等跨层状态

这里增强的是“在组件树中传播能力”的方式。

它和 [[./React 状态管理|React 状态管理]] 是直接相连的：当共享需求继续扩大，就会从 `useContext` 进一步走向外部 store。

### [[../Cards/React-useSyncExternalStore|useSyncExternalStore]]

当状态来源不再只属于 React 内部，而是来自外部 store 时，就需要这个 Hook。

适合：

- 订阅 Redux、Zustand 等外部存储
- 让 React 与外部状态源保持一致
- 在并发渲染语义下安全读取外部状态

这里增强的是“与 React 之外的状态系统对接”的能力。

## 第五层：并发渲染时代的调度增强

React 进入并发能力之后，Hook 不只是负责“拿状态”，还开始参与“调度体验”。

### [[../Cards/React-useTransition|useTransition]]

适合：

- 区分紧急更新和非紧急更新
- 在切换 tab、筛选列表、跳转界面时维持交互流畅性

### [[../Cards/React-useDeferredValue|useDeferredValue]]

适合：

- 输入要立即响应，但某些下游 UI 可以稍后更新
- 搜索联想、过滤列表、复杂渲染场景

### [[../Cards/React-useOptimistic|useOptimistic]]

适合：

- 用户操作后先乐观更新 UI
- 提交评论、点赞、发送消息等需要先反馈再等待服务端确认的场景

### [[../Cards/React-useActionState|useActionState]]

适合：

- 围绕表单动作维护提交状态和结果状态

这一层增强的是“用户感知上的流畅度和反馈节奏”。这背后可以继续关联到 [[../Cards/React Fiber|React Fiber]] 与 [[../Express/渐进式集成：从浏览器渲染到框架设计的统一哲学|渐进式集成：从浏览器渲染到框架设计的统一哲学]]。

## 第六层：抽象复用能力上升为自定义 Hook

当多个组件反复出现相同状态逻辑时，就不该只是在组件里复制 Hook 调用，而应该抽成自定义 Hook。

例如：

- [[../Cards/React useTimer|useCount]]
- [[react useRequest|useRequest]]

适合：

- 抽取业务逻辑
- 封装通用逻辑
- 监听浏览器状态
- 拆分复杂组件

这里增强的是“逻辑复用和领域抽象”的能力。

## Hook 的使用规则

这些规则不是语法洁癖，而是 React 能正确把状态槽位和当前组件绑定起来的前提：

1. 只能在组件顶层或自定义 Hook 顶层调用
2. 不能放进条件、循环或任意嵌套函数里
3. 必须保持调用顺序稳定

## 一个更准确的理解

React Hooks 的核心价值不是“提供很多 API”，而是把函数组件的能力按层次逐步打开：

- `useState` / `useReducer`：让函数组件有状态
- `useRef` / `useMemo` / `useCallback`：让函数组件有稳定引用和派生能力
- `useEffect`：让函数组件和外部世界同步
- `useContext` / `useSyncExternalStore`：让函数组件接入共享状态和外部系统
- [[../Cards/React-useTransition|useTransition]] / [[../Cards/React-useDeferredValue|useDeferredValue]] / [[../Cards/React-useOptimistic|useOptimistic]]：让函数组件参与并发调度和体验优化
- 自定义 Hook：让这些能力可以沉淀成可复用抽象

所以，学习 Hooks 最好的方式不是背列表，而是理解：当组件复杂度上升时，React 给了你哪些渐进增强的能力。

## 相关笔记

- [[./React 状态管理|React 状态管理]]
- [[../Cards/React 组件通信方式|父子组件传递]]
- [[../Cards/React Fiber|React Fiber]]
- [[./渐进增强|渐进增强]]
- [[../Express/渐进式集成：从浏览器渲染到框架设计的统一哲学|渐进式集成：从浏览器渲染到框架设计的统一哲学]]

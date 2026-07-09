---
date: 2025-04-16T13:14:31
updated: 2026-07-09 20:21:41
---
React Hooks 不适合只按“API 清单”去记，更适合按 [[渐进增强]] 的方式理解：函数组件先获得最基础的状态能力，再逐步获得派生能力、引用能力、副作用能力、共享能力、并发调度能力和抽象复用能力。

## 核心判断

React Hooks 的核心价值不是“提供很多 API”，而是把函数组件的能力按层次逐步打开。

如果把 [[React 状态管理]] 看成“状态如何升级”，那么 React Hooks 可以看成“函数组件的能力如何升级”：

1. 先让函数组件拥有局部状态和状态迁移能力。
2. 再让组件在复杂渲染中保留稳定引用、稳定函数身份和派生结果。
3. 然后让组件能在渲染之后和外部世界同步。
4. 当状态和能力需要跨组件流动时，再接入 Context、外部 store 和状态管理结构。
5. 在并发渲染时代，Hooks 进一步参与更新优先级、延迟策略、乐观反馈和动作结果组织。
6. 最后，自定义 Hook 把这些能力组合成可复用抽象。

所以，学习 Hooks 最好的方式不是背列表，而是理解：当组件复杂度上升时，React 给了你哪些渐进增强的能力。

## 这个主题下我目前知道的内容

### 一条渐进增强的主线

[[React useState 的问题解决和核心用法|useState]] -> [[React useReducer 的问题解决和核心用法|useReducer]] -> [[React-useRef|useRef]] -> [[React-useEffect|useEffect]] -> [[React-useContext|useContext]] -> [[React-useSyncExternalStore|useSyncExternalStore]] -> [[React useTransition 的问题解决和核心用法|useTransition]] / [[React useDeferredValue 的问题解决和核心用法|useDeferredValue]] / [[React useOptimistic 的问题解决和核心用法|useOptimistic]] / [[React-useActionState|useActionState]] -> 自定义 Hooks

### 为什么需要 Hooks

Hooks 的出现，不是为了给函数组件补一组零散 API，而是为了让函数组件在保持声明式风格的前提下，逐步承载越来越复杂的 UI 逻辑。

它们让函数组件能够：

- 保存状态
- 响应状态变化并重新渲染
- 执行副作用
- 访问 DOM 和可变引用
- 在组件树中共享能力
- 复用状态逻辑
- 在并发渲染语义下优化用户体验

### Hook 的使用规则

这些规则不是语法洁癖，而是 React 能正确把状态槽位和当前组件绑定起来的前提：

1. 只能在组件顶层或自定义 Hook 顶层调用
2. 不能放进条件、循环或任意嵌套函数里
3. 必须保持调用顺序稳定

## 六层能力地图

### 第一层：先让函数组件有状态

这一层解决的是：组件不再只是“输入 props，输出 UI”，而是开始拥有自己的局部状态与状态迁移。

相关概念 / 下层卡片：

- [[React useState 的问题解决和核心用法|useState]]
- [[React useReducer 的问题解决和核心用法|useReducer]]

### 第二层：让组件拥有稳定引用和派生结果

这一层解决的是：当组件复杂度上升后，单纯“有状态”还不够，还需要稳定引用、稳定函数身份和派生结果复用，避免把所有东西都重新创建、重新计算。

相关概念 / 下层卡片：

- [[React-useRef|useRef]]
- [[React useMemo 的问题解决和核心用法|useMemo]]
- [[React useCallback 的问题解决和核心用法|useCallback]]
- [[React useId 的问题解决和核心用法|useId]]
- [[React forwardRef 的问题解决和使用方式|forwardRef]]
- [[React useImperativeHandle 的问题解决和核心用法|useImperativeHandle]]

相关入口：[[从渐进增强角度理解 react 组件通信方式]]

### 第三层：组件开始和外部世界同步

这一层解决的是：组件不再只做渲染计算，而开始接触网络、浏览器 API、订阅系统和第三方库。也就是说，组件开始承担“渲染之后与外部系统同步”的职责。

相关概念 / 下层卡片：

- [[React-useEffect|useEffect]]
- [[React useLayoutEffect 的问题解决和核心用法|useLayoutEffect]]

相关材料：[[useEffect 的底层是如何实现的]]

### 第四层：状态和能力开始跨组件共享

这一层解决的是：当共享需求从局部直连升级到跨层传播，组件就需要新的能力去传递值、共享能力，并进一步接入 React 之外的状态系统。

相关概念 / 下层卡片：

- [[React-useContext|useContext]]
- [[React-useSyncExternalStore|useSyncExternalStore]]

相关入口：[[React 状态管理]]

### 第五层：并发渲染时代的调度增强

这一层解决的是：Hook 不再只负责“拿到状态”，还开始参与更新优先级、延迟策略、乐观反馈和动作结果组织，从而直接影响用户感知到的流畅度与反馈节奏。

相关概念 / 下层卡片：

- [[React useTransition 的问题解决和核心用法|useTransition]]
- [[React useDeferredValue 的问题解决和核心用法|useDeferredValue]]
- [[React useOptimistic 的问题解决和核心用法|useOptimistic]]
- [[React-useActionState|useActionState]]

相关入口：[[React Fiber]]、[[渐进式集成：从浏览器渲染到框架设计的统一哲学]]

### 第六层：抽象复用能力上升为自定义 Hook

这一层解决的是：当多个组件反复出现同类状态逻辑时，问题已经不再是“会不会用 Hook”，而是“能不能把 Hook 组合沉淀为稳定抽象”。

典型方向：

- 业务逻辑抽取
- 通用逻辑封装
- 浏览器能力监听
- 复杂组件拆分

相关概念 / 下层卡片：

- [[React useTimer 的问题解决和核心用法|useCount]]
- [[React useRequest 封装的请求状态和使用方式|useRequest]]

## 学习顺序

如果按能力升级来学习，可以采用下面的顺序：

1. [[React useState 的问题解决和核心用法|useState]]
2. [[React useReducer 的问题解决和核心用法|useReducer]]
3. [[React-useRef|useRef]] / [[React useMemo 的问题解决和核心用法|useMemo]] / [[React useCallback 的问题解决和核心用法|useCallback]]
4. [[React-useEffect|useEffect]]
5. [[React-useContext|useContext]]
6. [[React-useSyncExternalStore|useSyncExternalStore]]
7. [[React useTransition 的问题解决和核心用法|useTransition]] / [[React useDeferredValue 的问题解决和核心用法|useDeferredValue]] / [[React useOptimistic 的问题解决和核心用法|useOptimistic]] / [[React-useActionState|useActionState]]
8. 自定义 Hooks

## 相关概念 / 下层卡片

- [[React useState 的问题解决和核心用法|useState]]
- [[React useReducer 的问题解决和核心用法|useReducer]]
- [[React-useRef|useRef]]
- [[React useMemo 的问题解决和核心用法|useMemo]]
- [[React useCallback 的问题解决和核心用法|useCallback]]
- [[React-useEffect|useEffect]]
- [[React-useContext|useContext]]
- [[React-useSyncExternalStore|useSyncExternalStore]]
- [[React useTransition 的问题解决和核心用法|useTransition]]
- [[React useDeferredValue 的问题解决和核心用法|useDeferredValue]]
- [[React useOptimistic 的问题解决和核心用法|useOptimistic]]
- [[React-useActionState|useActionState]]

## 相关入口

- [[React 状态管理]]
- [[从渐进增强角度理解 react 组件通信方式]]
- [[React Fiber]]
- [[渐进增强]]
- [[渐进式集成：从浏览器渲染到框架设计的统一哲学]]
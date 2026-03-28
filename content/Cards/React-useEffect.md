---
date: 2025-04-16T13:48:17
updated: 2026-03-09 16:31:49
up:
  - "[[../Knowledges/React Hooks|React Hooks]]"
share: true
---
`useEffect` 是 React 组件从“只负责渲染”走向“与外部世界同步”的关键 Hook。当前面的状态、引用和派生能力都还不够时，说明组件已经需要副作用了。

## 它解决什么问题

React 组件的核心职责是：根据状态声明 UI。

但真实应用中，组件还要处理很多渲染之外的事情：

- 请求数据
- 订阅事件
- 操作浏览器 API
- 同步第三方库
- 注册和清理外部资源

这些都属于副作用，`useEffect` 就是用来处理这类逻辑的。

## 一句话理解

`useEffect` 负责在渲染提交之后，把 React 组件和外部系统连接起来，并在依赖变化或组件卸载时做同步和清理。

这里增强的是“渲染之后与外部世界对接”的能力。

## 一个典型例子

```tsx
import React, { useEffect, useState } from 'react'

function BlogView({ id }) {
  const [blogContent, setBlogContent] = useState(null)

  useEffect(() => {
    const doAsync = async () => {
      setBlogContent(null)
      const res = await fetch(`/blog-content/${id}`)
      setBlogContent(await res.text())
    }

    doAsync()
  }, [id])

  const isLoading = !blogContent
  return <div>{isLoading ? 'Loading...' : blogContent}</div>
}
```

这个 effect 的含义是：

- 当 `id` 变化时
- 去同步一份新的外部数据
- 然后再把结果放回 React 状态

## 依赖数组怎么理解

依赖数组不是“优化开关”，而是在声明：

“这个副作用依赖哪些值，当这些值变化时，我需要重新和外部世界同步。”

### 依赖变化时执行

```tsx
useEffect(() => {
  console.log('run on mount and when deps change')
}, [deps])
```

### 每次渲染后都执行

```tsx
useEffect(() => {
  console.log('run after every render')
})
```

### 只在首次挂载后执行

```tsx
useEffect(() => {
  console.log('did mount')
}, [])
```

## 清理函数

如果 effect 注册了外部资源，就应该在下一次 effect 执行前或组件卸载时清理。

```tsx
const [size, setSize] = useState({})

useEffect(() => {
  const handler = () => {
    setSize(getSize())
  }

  window.addEventListener('resize', handler)

  return () => {
    window.removeEventListener('resize', handler)
  }
}, [])
```

这类 effect 的重点不是“执行了什么”，而是“是否正确撤销了之前的副作用”。

## 什么时候该用

适合：

- 跟网络、浏览器、订阅系统、定时器、第三方库交互
- 需要在 React 渲染之后执行同步逻辑
- 需要在依赖变化时重新建立连接

## 什么时候不该用

很多 `useEffect` 其实都不该写。

不适合：

- 纯粹的派生计算
- 能在 render 阶段直接算出来的值
- 只是为了把一个 state 再同步到另一个 state

如果没有“外部系统”，就先怀疑自己是不是根本不需要 effect。

## 常见误区

### 1. 把 `useEffect` 当生命周期翻译器

它确实可以映射 class 组件里的：

- `componentDidMount`
- `componentDidUpdate`
- `componentWillUnmount`

但更准确的理解应该是“同步外部系统”，而不是“机械对应生命周期”。

### 2. 依赖数组写不全

依赖数组不是手工控制执行次数的工具。

如果 effect 内部用到了某个响应式值，通常就应该把它列进依赖。

### 3. 把很多业务逻辑都塞进 effect

一旦 effect 变成“大杂烩”，往往说明：

- 状态设计不合理
- 派生逻辑没有放回 render
- 自定义 Hook 抽象还没做好

## 相关延伸

- [[./React-useLayoutEffect|useLayoutEffect]]：适合布局测量和同步 DOM 读写，比 `useEffect` 更早执行
- [[useEffect 的底层是如何实现的|useEffect 的底层是如何实现的]]：可以继续看调度细节
- [[./React-useRef|useRef]]：常用来保存订阅句柄、定时器、外部实例

## 和其它笔记的关系

- 在 [[../Knowledges/React Hooks|React Hooks]] 里，它对应“组件开始和外部世界同步”这一层
- 在 [[../Knowledges/React 状态管理|React 状态管理]] 里，它经常和状态更新联动，但本身不是状态管理工具
- 在 [[./React Fiber|React Fiber]] 和 [[../Express/渐进式集成：从浏览器渲染到框架设计的统一哲学|渐进式集成：从浏览器渲染到框架设计的统一哲学]] 的语境里，它可以继续连接到渲染调度与副作用提交阶段

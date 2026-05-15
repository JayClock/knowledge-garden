---
date: 2025-04-17T16:31:32
updated: 2026-05-15 10:03:23
up:
  - "[[../Knowledges/React Hooks|React Hooks]]"
share: true
noteId: 1778807093039
---
React useRef 用来解决什么问题，核心用法是什么？

---

`useRef` 是函数组件获得“稳定引用能力”的关键 Hook。它不是用来替代状态的，而是用来保存那些需要跨渲染保留、但又不该触发重新渲染的值。

 它解决什么问题

函数组件每次渲染都会重新执行。

这意味着：

- 普通局部变量会被重新初始化
- 某些值需要跨渲染保留下来
- 但这些值变化后又不应该影响 UI

这就是 `useRef` 的位置。

 一句话理解

`useRef` 提供了一个稳定的容器对象，你可以把值放在 `current` 上，它会在多次渲染之间保留，但修改它不会触发重新渲染。

这里增强的是“跨渲染保持引用”的能力。

 两个最常见的用途

 1. 保存不参与渲染的可变值

例如定时器 ID、上一次值、请求句柄、外部实例等。

```tsx
import React, { useCallback, useRef, useState } from 'react'

export default function Timer() {
  const [time, setTime] = useState(0)
  const timer = useRef(null)

  const handleStart = useCallback(() => {
    timer.current = window.setInterval(() => {
      setTime((time) => time + 1)
    }, 100)
  }, [])

  const handlePause = useCallback(() => {
    window.clearInterval(timer.current)
    timer.current = null
  }, [])

  return (
    <div>
      {time / 10} seconds.
      <br />
      <button onClick={handleStart}>Start</button>
      <button onClick={handlePause}>Pause</button>
    </div>
  )
}
```

这里 `timer.current` 会一直保留，但它本身不是 UI 状态，所以不应该放到 `useState` 里。

 2. 获取 DOM 元素引用

```tsx
function TextInputWithFocusButton() {
  const inputEl = useRef(null)

  const onButtonClick = () => {
    inputEl.current?.focus()
  }

  return (
    <>
      <input ref={inputEl} type="text" />
      <button onClick={onButtonClick}>Focus the input</button>
    </>
  )
}
```

这是 `ref` 最经典的用法之一，用于 `focus`、滚动、测量尺寸、调用原生 DOM API。

 什么时候该用

适合：

- 值要跨渲染保留
- 值变化不需要驱动界面刷新
- 需要访问 DOM 或外部实例

 什么时候不该用

不适合：

- 需要展示到界面上的数据
- 改变后必须触发重新渲染的值
- 试图用它绕过 React 的状态流

如果值变化后 UI 需要更新，优先考虑 `useState` 或 [[React-useReducer|useReducer]]。

 和通信的关系

`useRef` 不只是一个“存值工具”，它还连接了组件通信中的命令式能力暴露。

当你配合 [[./react-forwardRef|forwardRef]] 与 [[./React-useImperativeHandle|useImperativeHandle]] 使用时，父组件可以调用子组件暴露的方法。这对应 [[./React 组件通信方式|React 组件通信方式]] 中的那条“`ref` 暴露实例能力”路线。

 一个常见误区

很多人会把 `useRef` 理解成“轻量 state”。

这通常是错的。

更准确的理解是：

- `state` 用来驱动渲染
- `ref` 用来保存稳定引用或命令式句柄

它们职责完全不同。

 和其它笔记的关系

- 在 [[../Knowledges/React Hooks|React Hooks]] 里，它属于“稳定引用和派生能力”这一层
- 在 [[./React 组件通信方式|React 组件通信方式]] 里，它是父组件触发子组件命令式能力的桥梁
- 在 [[./React-useEffect|useEffect]] 里，它经常用来保存 effect 相关的外部句柄

---
date: 2025-04-17T10:21:36
updated: 2026-05-16 19:29:23
up:
  - "[[../Knowledges/React Hooks|React Hooks]]"
share: true
noteId: 1778930949614
---
React useCallback 用来解决什么问题，核心用法是什么？

---

`useCallback` 和 [[./React useMemo 的问题解决和核心用法|useMemo]] 属于同一层能力增强，只不过它缓存的不是“计算结果”，而是“函数引用”。

 它解决什么问题

函数组件每次渲染时，函数体内定义的函数也会重新创建。

这意味着：

- 即使逻辑没变，函数引用也会变
- 传给子组件时，可能导致下游不必要更新
- 放进依赖数组时，也可能触发额外 effect 或 memo 失效

这时就可以用 `useCallback` 让函数在依赖不变时保持同一个引用。

 一句话理解

`useCallback` 用来缓存函数引用，只在依赖变化时重新创建这个函数。

这里增强的是“函数身份稳定”的能力。

 一个最小例子

```tsx
import React, { useCallback, useState } from 'react'

function Counter() {
  const [count, setCount] = useState(0)

  const handleIncrement = useCallback(() => {
    setCount(count + 1)
  }, [count])

  return <button onClick={handleIncrement}>+</button>
}
```

如果没有 `useCallback`，组件每次重新渲染都会重新创建一个新的 `handleIncrement`。

 什么时候该用

适合：

- 回调函数要传给 `memo` 过的子组件
- 回调函数本身会作为其他 Hook 的依赖
- 你明确遇到了函数引用不稳定带来的问题

 什么时候不该用

不适合：

- 只是因为“别人都这么写”
- 子组件根本不关心函数引用是否变化
- 代码因此变得更绕，却没有实际收益

和 `useMemo` 一样，`useCallback` 也不是默认就该加的优化。

 一个常见误区

很多人会把 `useCallback` 理解成“防止函数执行”。

这不对。

它防止的不是“执行”，而是“重新创建新的函数引用”。

函数该执行的时候还是会执行。

 和 `useMemo` 的关系

可以把它理解成一个语义更清晰的专用版本：

- `useMemo` 缓存值
- `useCallback` 缓存函数

如果只是为了拿到稳定函数引用，通常优先用 `useCallback`，而不是把函数塞进 `useMemo`。

 一个需要注意的点

`useCallback` 并不自动让你的代码“更快”。

如果依赖变化很频繁，或者下游根本不利用这个稳定引用，那它几乎没有收益。

所以真正的判断标准不是“能不能用”，而是：

- 这个函数引用稳定下来之后，是否真的减少了下游工作量

 和其它笔记的关系

- 在 [[../Knowledges/React Hooks|React Hooks]] 里，它属于“稳定引用和派生能力”这一层
- 在 [[./React useMemo 的问题解决和核心用法|useMemo]] 里，可以看到它们的角色分工
- 在 [[../Knowledges/React-useEffect|useEffect]] 里，它经常用于稳定 effect 依赖中的函数引用

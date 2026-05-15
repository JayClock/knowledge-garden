---
date: 2025-04-17T10:36:30
updated: 2026-05-15 10:03:24
up:
  - "[[../Knowledges/React Hooks|React Hooks]]"
share: true
noteId: 1778807092965
---
React useMemo 用来解决什么问题，核心用法是什么？

---

`useMemo` 不是“默认性能优化按钮”，而是当派生计算已经开始重复消耗、或者引用稳定性开始影响下游渲染时，用来做一次有边界的缓存增强。

 它解决什么问题

组件每次重新渲染时，函数体都会重新执行。

这意味着：

- 派生计算会重新跑一遍
- 即使依赖没变，结果也会重新创建
- 某些场景下会造成性能浪费或引用不稳定

这时就可以用 `useMemo` 缓存“某次计算的结果”，只在依赖变化时重新计算。

 一句话理解

`useMemo` 让派生值只在依赖变化时重新计算，而不是每次渲染都重算。

这里增强的是“派生结果复用”的能力。

 一个典型例子

```tsx
import React, { useEffect, useMemo, useState } from 'react'

export default function SearchUserList() {
  const [users, setUsers] = useState(null)
  const [searchKey, setSearchKey] = useState('')

  useEffect(() => {
    const doFetch = async () => {
      const res = await fetch('https://reqres.in/api/users/')
      setUsers(await res.json())
    }

    doFetch()
  }, [])

  const usersToShow = useMemo(() => {
    if (!users) return null

    return users.data.filter((user) => {
      return user.first_name.includes(searchKey)
    })
  }, [users, searchKey])

  return (
    <div>
      <input
        type="text"
        value={searchKey}
        onChange={(evt) => setSearchKey(evt.target.value)}
      />
      <ul>
        {usersToShow?.map((user) => {
          return <li key={user.id}>{user.first_name}</li>
        })}
      </ul>
    </div>
  )
}
```

这里 `usersToShow` 不是一份新的 state，而是从 `users + searchKey` 派生出来的结果，所以更适合 `useMemo`，而不是 [[./React-useState|useState]]。

 什么时候该用

适合：

- 计算比较重
- 结果是派生值
- 依赖集合明确
- 结果对象或数组的引用稳定性会影响子组件渲染

 什么时候不该用

不适合：

- 计算非常轻
- 只是为了“到处都优化一下”
- 依赖关系不清楚
- 试图用它替代正确的状态设计

如果计算很轻，`useMemo` 本身也有维护成本，反而可能让代码更复杂。

 一个常见误区

很多人会把 `useMemo` 当成“防止重新渲染”的工具。

这不准确。

`useMemo` 做的事情是：

- 缓存某次计算结果

它不直接阻止组件重新渲染，只是让渲染过程中某些派生值不必重复计算，或者保持稳定引用。

 和 `useCallback` 的关系

`useMemo` 缓存的是“计算结果”。

如果这个结果刚好是一个函数，那么理论上它也能工作：

```tsx
const myEventHandler = useMemo(() => {
  return () => {
    // handle event
  }
}, [dep1, dep2])
```

但在语义上，更合适的做法通常是使用 [[./React-useCallback|useCallback]]。

 和其它笔记的关系

- 在 [[../Knowledges/React Hooks|React Hooks]] 里，它属于“稳定引用和派生能力”这一层
- 在 [[./React-useState|useState]] 里提到的“不要把派生值放进 state”，通常就会落到 `useMemo`
- 在 [[./React-useCallback|useCallback]] 里，可以看到“缓存函数引用”的对应形态

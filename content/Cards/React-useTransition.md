---
date: 2026-03-09T16:20:01
updated: 2026-05-15 12:16:33
up:
  - "[[../Knowledges/React Hooks|React Hooks]]"
share: true
noteId: 1778807093126
---
React useTransition 用来解决什么问题，核心用法是什么？

---

`useTransition` 是 React 在并发渲染语义下提供的调度型 Hook。它不负责存状态本身，而是告诉 React：这次更新“可以晚一点”，不要和用户当前最紧急的交互抢优先级。

 它解决什么问题

有些更新对用户来说很急：

- 输入框回显
- 按钮点击反馈
- 焦点切换

有些更新则可以稍后一点完成：

- 大列表筛选结果
- tab 切换后的重内容区域
- 搜索结果面板

如果这些更新被放在同一优先级里，重更新就可能拖慢即时交互。

`useTransition` 的作用就是把“能稍后完成的更新”标记为过渡更新，让 React 优先处理更紧急的任务。

 一句话理解

`useTransition` 让你把某些 state 更新标记成“非紧急”，从而优先保证当前交互的流畅反馈。

这里增强的是“更新优先级调度”的能力。

 核心返回值

它通常长这样：

```tsx
const [isPending, startTransition] = useTransition()
```

- `startTransition`
 用来包裹那些可以延后的更新
- `isPending`
 表示这段过渡更新是否仍在进行中

 一个典型例子

```tsx
import { useState, useTransition } from 'react'

function SearchPage() {
  const [query, setQuery] = useState('')
  const [resultQuery, setResultQuery] = useState('')
  const [isPending, startTransition] = useTransition()

  const handleChange = (event) => {
    const nextValue = event.target.value

    setQuery(nextValue)

    startTransition(() => {
      setResultQuery(nextValue)
    })
  }

  return (
    <div>
      <input value={query} onChange={handleChange} />
      {isPending ? <p>Loading...</p> : <SearchResults query={resultQuery} />}
    </div>
  )
}
```

这里输入框本身的更新更紧急，而结果区域更新可以稍后一点。

 什么时候该用

适合：

- 输入联想
- 大列表筛选
- 切换重内容区域
- 会触发明显重新渲染压力的非即时更新

 什么时候不该用

不适合：

- 受控输入本身的值更新
- 必须立刻完成的同步交互
- 只是因为“看上去更高级”而把普通更新都包进去

如果一个更新本来就很轻，或者用户必须立即看到结果，那就没必要用 transition。

 一个常见误区

很多人会把 `useTransition` 理解成“异步执行 state”。

这不准确。

更准确的理解是：

- 它不是把更新变成 Promise
- 它是在告诉 React 这类更新可以用更低优先级调度

所以它的重点不是“异步”，而是“优先级”。

 和其它笔记的关系

- 在 [[../Knowledges/React Hooks|React Hooks]] 里，它属于“并发渲染时代的调度增强”
- 在 [[../Knowledges/React Fiber|React Fiber]] 里，可以理解它为什么建立在调度系统之上
- 和 [[./React-useDeferredValue|useDeferredValue]] 一样，它们都在解决“哪些更新该先发生”这个问题

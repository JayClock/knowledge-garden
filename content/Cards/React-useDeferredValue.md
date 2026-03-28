---
date: 2026-03-09T16:20:01
updated: 2026-03-09 16:27:18
up:
  - "[[../Knowledges/React Hooks|React Hooks]]"
share: true
---
`useDeferredValue` 也是并发渲染语义下的调度型 Hook。和 [[./React-useTransition|useTransition]] 不同，它不是让你包裹一段更新逻辑，而是让你拿到某个值的“延后版本”。

## 它解决什么问题

有时用户输入需要立即更新，但下游某个区域的渲染很重，例如：

- 搜索结果列表
- 大量过滤后的表格
- 复杂图表

这时你不想拖慢输入本身，只想让“依赖这个值的重区域”稍后更新。

`useDeferredValue` 就是在做这件事。

## 一句话理解

`useDeferredValue` 让某个值的消费节奏慢下来，从而优先保证当前输入或交互本身的流畅性。

这里增强的是“值传播节奏控制”的能力。

## 一个典型例子

```tsx
import { useDeferredValue, useState } from 'react'

function SearchPage() {
  const [query, setQuery] = useState('')
  const deferredQuery = useDeferredValue(query)

  return (
    <div>
      <input value={query} onChange={(event) => setQuery(event.target.value)} />
      <SearchResults query={deferredQuery} />
    </div>
  )
}
```

这里：

- 输入框总是立即跟随 `query`
- `SearchResults` 则消费一个“延后版本”的 `deferredQuery`

## 什么时候该用

适合：

- 输入立即变化，但下游渲染很重
- 你不想拆成两份手工状态
- 你只想延后“消费值的区域”，而不是自己组织 transition 逻辑

## 和 `useTransition` 的区别

可以这样粗略区分：

- [[./React-useTransition|useTransition]]
  更像“把一批更新标记成低优先级”
- `useDeferredValue`
  更像“给我这个值的一个延后版本”

前者更像从“更新动作”下手，后者更像从“被消费的值”下手。

## 什么时候不该用

不适合：

- 值更新必须严格实时同步的场景
- 下游渲染本来就不重
- 想拿它来代替正常的节流、防抖或数据请求控制

它解决的是渲染优先级问题，不是网络层节流问题。

## 一个常见误区

很多人会把 `useDeferredValue` 理解成“自动 debounce”。

这不准确。

它不会承诺固定延迟时间，也不是基于毫秒计时的防抖。

更准确的理解是：

- 它让 React 在调度层面延后某个值的传播与消费

## 和其它笔记的关系

- 在 [[../Knowledges/React Hooks|React Hooks]] 里，它属于“并发渲染时代的调度增强”
- 在 [[./React Fiber|React Fiber]] 里，可以看到它背后的优先级调度基础
- 和 [[./React-useTransition|useTransition]] 一起理解，会更容易把握“动作延后”和“值延后”的区别

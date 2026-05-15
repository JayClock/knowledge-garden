---
date: 2026-03-09T16:29:31
updated: 2026-05-15 10:03:24
up:
  - "[[../Knowledges/React Hooks|React Hooks]]"
share: true
noteId: 1778807092939
---
React useLayoutEffect 用来解决什么问题，核心用法是什么？

---

`useLayoutEffect` 和 [[./React-useEffect|useEffect]] 很像，但它解决的是“时机更靠前的副作用”问题。它适合那些必须在浏览器绘制之前同步完成的 DOM 读写，而不是普通的数据请求或订阅。

 它解决什么问题

大部分副作用放在 [[./React-useEffect|useEffect]] 里就够了，因为它发生在提交之后，不会阻塞浏览器绘制。

但有一类场景不一样：

- 需要读取布局信息
- 需要立即修正 DOM 位置
- 需要在用户看到页面之前完成同步测量和写入

如果这些逻辑放到 `useEffect` 里，用户可能先看到一个错误布局，再看到它被修正，产生闪动。

这时就需要 `useLayoutEffect`。

 一句话理解

`useLayoutEffect` 让你在 DOM 更新后、浏览器绘制前，同步执行副作用。

这里增强的是“布局阶段副作用控制”的能力。

 一个典型例子

```tsx
import { useLayoutEffect, useRef, useState } from 'react'

function Tooltip() {
  const ref = useRef(null)
  const [height, setHeight] = useState(0)

  useLayoutEffect(() => {
    const rect = ref.current?.getBoundingClientRect()
    setHeight(rect?.height ?? 0)
  }, [])

  return <div ref={ref}>Tooltip height: {height}</div>
}
```

这个场景里，如果你必须先测量、再决定布局，就更适合 `useLayoutEffect`。

 什么时候该用

适合：

- 读取元素尺寸和位置
- 同步滚动位置
- 在绘制前修正布局
- 集成依赖同步 DOM 测量的第三方库

 什么时候不该用

不适合：

- 普通数据请求
- 订阅事件
- 日志上报
- 不依赖布局时机的副作用

如果没有“必须在绘制前完成”的理由，优先使用 [[./React-useEffect|useEffect]]。

 一个常见误区

很多人会把 `useLayoutEffect` 理解成“更高级的 useEffect”。

这不对。

它不是更高级，而是时机更靠前、代价也更高，因为它会阻塞浏览器绘制。

所以默认选择应该仍然是 [[./React-useEffect|useEffect]]，只有在布局同步场景下才升级到 `useLayoutEffect`。

 和其它笔记的关系

- 在 [[../Knowledges/React Hooks|React Hooks]] 里，它属于副作用能力的细分节点
- 在 [[./React-useEffect|useEffect]] 里，它是更靠前的布局副作用版本
- 在 [[./React Fiber|React Fiber]] 里，它可以连接到提交阶段中更靠近 layout 的执行时机

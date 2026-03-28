---
date: 2025-04-16T13:38:56
updated: 2026-03-09 16:08:48
up:
  - "[[../Knowledges/React Hooks|React Hooks]]"
related:
  - "[[React-Redux]]"
share: true
---
`useState` 是函数组件获得状态能力的起点。只要一个组件需要“记住某个值，并在它变化时重新渲染”，就进入了 `useState` 的适用范围。

## 它解决什么问题

函数组件每次渲染都会重新执行，所以普通局部变量无法在多次渲染之间保留。

`useState` 提供了两件事：

- 在多次渲染之间保存状态
- 当状态变化时，触发组件重新渲染

这是 [[../Knowledges/React Hooks|React Hooks]] 体系里最基础的一层能力，也是 [[../Knowledges/React 状态管理|React 状态管理]] 的起点。

## 一句话理解

`useState` 让函数组件从“只会根据输入返回 UI”升级为“能记住局部状态并响应交互”。

这里增强的是“记住值并驱动渲染”的能力。

## 一个最小例子

```tsx
import React, { useState } from 'react'

function Example() {
  const [count, setCount] = useState(0)

  return (
    <div>
      <p>{count}</p>
      <button onClick={() => setCount(count + 1)}>+</button>
    </div>
  )
}
```

## 什么时候该用

适合：

- 输入框值
- 开关状态
- 展开收起
- 当前 tab
- 页码
- 局部 loading 状态

这类状态通常有几个特点：

- 作用域只在当前组件或少量子组件内
- 结构简单
- 更新逻辑直接

## 什么时候不该用

并不是所有值都应该进 state。

**不要把可以直接计算出来的值放进 state。**

例如：

1. 从 `props` 派生出来的值
2. 从 URL 读取到的值
3. 从 `cookie`、`localStorage` 中直接可获取的值
4. 可以由现有 state 通过计算得到的排序、过滤、映射结果

这些值更适合：

- 直接在 render 中计算
- 或者交给 [[./React-useMemo|useMemo]] 做缓存

如果一个值本身不是“源状态”，就不要把它再复制成另一份 state。

## 什么时候该升级

当下面这些问题开始出现时，说明你可能要从 `useState` 往上升级了：

- 一个组件里 state 数量变得很多
- 多个字段总是一起变化
- 更新逻辑开始依赖旧状态并形成明确的状态迁移

这时通常该进入 [[React-useReducer|useReducer]]。

如果共享范围继续扩大，再进入 [[./React-useContext|React-useContext]] 或更上层的 [[../Knowledges/React 状态管理|React 状态管理]]。

## 一个常见误区

很多人会把“所有会变化的值”都塞进 `useState`。

这会带来两个问题：

- 数据冗余，出现两份容易失真的状态
- 组件重新创建时，需要恢复更多状态，复杂度上升

更准确的做法是区分：

- 哪些是“源状态”
- 哪些只是“派生结果”

只有前者才适合放进 `useState`。

## 和其它笔记的关系

- 在 [[../Knowledges/React Hooks|React Hooks]] 里，它是函数组件有状态的起点
- 在 [[../Knowledges/React 状态管理|React 状态管理]] 里，它是最小、最局部的状态管理方案
- 在 [[React-useReducer|useReducer]] 里，可以看到它升级后的形态

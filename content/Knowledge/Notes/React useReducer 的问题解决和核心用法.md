---
date: 2025-09-30 20:04:49
noteId: 1778930949843
updated: 2026-07-09 11:00:29
---
React useReducer 的问题解决和核心用法

---

`useReducer` 是从 [[React useState 的问题解决和核心用法|useState]] 往上升级的一步。它不是为了“替代所有 state”，而是在状态逻辑开始复杂、更新规则开始成形时，让状态变更更可组织。

 它解决什么问题

当组件的状态不再是一个简单值，而是出现下面这些情况时，`useState` 会开始显得分散：

- 多个字段一起变化
- 更新依赖前一个状态
- 不同事件触发不同状态迁移
- 状态更新规则需要被集中描述

这时就可以把“状态是什么”和“状态如何变化”分开：

- `state` 负责保存当前状态
- `action` 描述发生了什么
- `reducer` 描述状态如何根据 action 变化

 一句话理解

`useReducer` 让组件从“零散地 set state”升级为“用动作和状态迁移来管理复杂状态”。

这里增强的是“组织状态变更逻辑”的能力。

 一个最小例子

```tsx
import { useReducer } from 'react'

const initialState = { count: 0 }

function reducer(state, action) {
  switch (action.type) {
    case 'INCREMENT':
      return { count: state.count + 1 }
    case 'DECREMENT':
      return { count: state.count - 1 }
    default:
      return state
  }
}

function Counter() {
  const [state, dispatch] = useReducer(reducer, initialState)

  return (
    <div>
      <p>Count: {state.count}</p>
      <button onClick={() => dispatch({ type: 'INCREMENT' })}>INCREMENT</button>
      <button onClick={() => dispatch({ type: 'DECREMENT' })}>DECREMENT</button>
    </div>
  )
}
```

 什么时候该用

适合：

- 表单状态较复杂
- 列表编辑器
- 向导流程
- 有明显状态迁移的交互
- 一个行为会影响多个字段

如果你已经开始写很多这样的代码：

- `setX(...)`
- `setY(...)`
- `setZ(...)`

并且它们总是成组出现，那通常就说明可以考虑 `useReducer` 了。

 和 `useState` 的关系

`useReducer` 不是因为“对象 state 不好”才存在。

更准确的区别是：

- `useState` 适合简单、局部、直接的状态
- `useReducer` 适合复杂、联动、规则明确的状态

它们的分界点不在于“是不是对象”，而在于“状态变更逻辑是否已经复杂到需要集中管理”。

 什么时候不该用

不适合：

- 只有一个简单布尔值或计数值
- 没有清晰的 action 语义
- 只是为了“看起来更架构化”而引入 reducer

如果一个状态更新写成 `reducer` 反而更绕，那就说明还没到该升级的时候。

 一个常见误区

很多人会把 `useReducer` 理解成“组件内版 Redux”。

这个理解有一点帮助，但不够准确。

更好的理解是：

- `useReducer` 是在单个组件或局部组件树中组织复杂状态逻辑
- [[React Redux 的核心作用和使用场景|Redux]] 则是把这种模式扩展为跨组件、跨模块的全局状态协作机制

也就是说，`useReducer` 更像是复杂状态管理的局部形态。

 和其它笔记的关系

- 在 [[React Hooks]] 里，它是 `useState` 之后的升级层
- 在 [[React 状态管理]] 里，它解决的是“逻辑复杂，但共享范围还没扩大”的阶段
- 如果共享需求继续扩大，就会继续进入 [[React-useContext]] 或更完整的状态管理方案

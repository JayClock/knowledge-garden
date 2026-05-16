---
date: 2026-03-09T16:36:31
updated: 2026-05-16 19:29:23
up:
  - "[[../Knowledges/React Hooks|React Hooks]]"
share: true
noteId: 1778930949712
---
React useId 用来解决什么问题，核心用法是什么？

---

`useId` 解决的不是“业务状态”问题，而是“组件需要稳定、唯一且适合可访问性关联的 ID”这个问题。它最常见的用途是把标签、描述、输入框等元素稳定关联起来。

 它解决什么问题

在组件里经常会需要 ID：

- `label` 关联 `input`
- `aria-describedby` 关联提示文本
- 表单元素和错误信息做语义连接

如果自己手写：

- 容易重复
- 在组件复用时不稳定
- 在服务端渲染和客户端 hydration 场景下还可能不一致

`useId` 就是 React 提供的稳定 ID 生成能力。

 一句话理解

`useId` 用来生成适合组件内部关联和无障碍属性使用的稳定 ID。

这里增强的是“结构化、可访问的标识生成”能力。

 一个最小例子

```tsx
import { useId } from 'react'

function NameField() {
  const id = useId()

  return (
    <div>
      <label htmlFor={id}>Name</label>
      <input id={id} />
    </div>
  )
}
```

这样 `label` 和 `input` 就能稳定关联起来。

 什么时候该用

适合：

- 表单控件和标签关联
- `aria-*` 描述关系
- 组件内部需要稳定唯一标识
- SSR / hydration 场景下需要一致 ID

 什么时候不该用

不适合：

- 列表渲染时的 `key`
- 业务主键
- 数据库存储 ID

`useId` 生成的是界面结构用的标识，不是业务实体标识。

 一个常见误区

最常见的误用就是拿 `useId` 去当列表的 `key`。

这不对。

`key` 应该来自数据本身的稳定身份，而不是组件渲染时生成的结构性 ID。

 和其它笔记的关系

- 在 [[../Knowledges/React Hooks|React Hooks]] 里，它属于偏工具型的能力补充
- 和 [[../Knowledges/React-useRef|useRef]]、[[./React useLayoutEffect 的问题解决和核心用法|useLayoutEffect]] 不同，它不处理 DOM 引用或布局，而是处理结构标识与可访问性关联

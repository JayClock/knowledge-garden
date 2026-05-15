---
date: 2025-10-09 10:03:29
updated: 2026-05-15 10:03:23
share: true
noteId: 1778807092639
---
React forwardRef 用来解决什么问题，如何使用？

---

`forwardRef` 解决的是“父组件如何把 ref 继续传进一个被封装的子组件”这个问题。它通常出现在组件封装边界上，让外层仍然能够拿到内部 DOM 节点或进一步暴露出的命令式能力。

 它解决什么问题

默认情况下，`ref` 不能像普通 `props` 那样自然穿透一层组件封装。

这意味着：

- 你封装了一个输入框组件
- 父组件却拿不到真实的 `input` DOM
- 也没法对内部元素做 `focus`、滚动或测量

这时就需要 `forwardRef`，把外层传入的 ref 继续转交给内部节点或内部组件。

 一句话理解

`forwardRef` 让组件在封装之后，仍然可以把 ref 继续向内传递。

这里增强的是“ref 穿透组件边界”的能力。

 一个最小例子

```tsx
interface InputProps {
  value?: string
}

const Input = forwardRef<HTMLInputElement, InputProps>((props, ref) => {
  return <input ref={ref} />
})
```

这样父组件就能通过 `<Input ref={...} />` 拿到内部的 `input` 节点。

 什么时候该用

适合：

- 封装输入框、按钮、弹层触发器等基础组件
- 组件库或设计系统封装
- 父组件需要直接拿到内部 DOM
- 需要和 [[./React-useImperativeHandle|useImperativeHandle]] 一起暴露命令式 API

 什么时候不该用

不适合：

- 普通数据传递
- 只是想跨组件共享状态
- 没有任何 ref 透传需求的普通业务组件

如果只是传数据或事件，优先回到 [[./React 组件通信方式|React 组件通信方式]] 里的 `props` 和回调。

 和 `useImperativeHandle` 的关系

它们经常成对出现，但职责不同：

- `forwardRef`
 负责把 ref 送进去
- [[./React-useImperativeHandle|useImperativeHandle]]
 负责控制父组件最终能看到什么

也就是说：

- 没有 `forwardRef`，ref 很难穿透组件边界
- 没有 `useImperativeHandle`，父组件通常直接拿到 DOM 或内部实例引用

 React 19 的变化

在 React 19 的语境下，`ref` 的传递方式变得更自然，某些场景不再必须显式写 `forwardRef` 才能表达 ref 作为组件输入的一部分。

但从知识结构上看，`forwardRef` 仍然代表着同一个核心问题：

- **组件封装后，ref 如何穿透边界**

所以理解这个概念本身仍然重要。

 一个常见误区

很多人会把 `forwardRef` 理解成“父组件控制子组件”的默认手段。

这不准确。

更准确的理解是：

- 它只是让 ref 可以穿透
- 不代表你应该默认走命令式控制

只有当声明式数据流不自然、又确实需要访问内部节点或暴露能力时，才适合使用它。

 和其它笔记的关系

- 在 [[./React-useRef|useRef]] 里，它和 ref 的命令式能力直接相关
- 在 [[./React-useImperativeHandle|useImperativeHandle]] 里，可以继续看到“透传 ref 之后怎么裁剪暴露面”
- 在 [[./React 组件通信方式|React 组件通信方式]] 里，它对应“`ref` 暴露实例能力”那条路线

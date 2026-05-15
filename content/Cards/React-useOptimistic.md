---
date: 2026-03-09T16:20:01
updated: 2026-05-15 12:16:33
up:
  - "[[../Knowledges/React Hooks|React Hooks]]"
share: true
noteId: 1778807092990
---
React useOptimistic 用来解决什么问题，核心用法是什么？

---

`useOptimistic` 解决的不是“性能”问题，而是“反馈节奏”问题。它让用户操作发生后，界面先按成功路径乐观更新，再等待服务端真正确认。

 它解决什么问题

很多交互如果等服务端成功后再更新 UI，用户会感觉迟钝。

例如：

- 发送消息
- 点赞
- 添加评论
- 修改列表项状态

这些场景里，用户更希望立刻看到结果，而不是先看到转圈。

`useOptimistic` 的作用就是：

- 先给用户一个成功后的临时界面
- 再等真实结果回来

 一句话理解

`useOptimistic` 让 UI 先按“操作会成功”来更新，从而把反馈提前到服务端确认之前。

这里增强的是“交互反馈节奏”的能力。

 一个典型例子

```tsx
import { useOptimistic, useState } from 'react'

function CommentForm({ comments, submitComment }) {
  const [optimisticComments, addOptimisticComment] = useOptimistic(
    comments,
    (state, newComment) => [...state, newComment]
  )

  const [text, setText] = useState('')

  const handleSubmit = async () => {
    const tempComment = {
      id: Math.random(),
      text,
      pending: true,
    }

    addOptimisticComment(tempComment)
    setText('')

    await submitComment(text)
  }

  return (
    <div>
      <input value={text} onChange={(event) => setText(event.target.value)} />
      <button onClick={handleSubmit}>Send</button>
      <ul>
        {optimisticComments.map((comment) => {
          return <li key={comment.id}>{comment.text}</li>
        })}
      </ul>
    </div>
  )
}
```

这里用户会先看到评论出现在列表里，而不是等请求结束后才出现。

 什么时候该用

适合：

- 用户期望立即反馈的写操作
- 成功概率高、失败可恢复的场景
- 你愿意设计失败回滚或重试策略

 什么时候不该用

不适合：

- 失败代价很高的关键操作
- 乐观展示会造成严重误导的业务
- 你没有准备失败回滚逻辑

乐观更新不是“假装成功”，而是“先反馈，再校正”。

 一个常见误区

很多人会把 `useOptimistic` 理解成“让请求更快”。

这当然不对。

它不会缩短网络时间，只是把用户感知到的反馈提前。

所以它优化的是：

- 感知性能
- 交互节奏

而不是服务端响应速度。

 和并发能力的关系

`useOptimistic` 虽然不像 [[./React-useTransition|useTransition]] 那样直接表现为优先级调度，但它同样属于 React 在更现代交互体验下提供的增强能力。

如果说：

- `useTransition` 解决“哪些更新该先发生”
- `useDeferredValue` 解决“哪些值可以晚一点传播”

那么：

- `useOptimistic` 解决“用户该先看到什么反馈”

 和其它笔记的关系

- 在 [[../Knowledges/React Hooks|React Hooks]] 里，它属于“并发渲染时代的调度增强”
- 在 [[../Knowledges/React Fiber|React Fiber]] 的语境里，可以把它放进更广义的体验调度与渐进反馈体系中理解
- 和 [[./React-useTransition|useTransition]]、[[./React-useDeferredValue|useDeferredValue]] 一起看，更容易建立“优先级、节奏、反馈”这三个维度的区别

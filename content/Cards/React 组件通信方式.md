---
date: 2025-05-05T08:14:11
updated: 2026-03-09 16:48:21
share: true
---
React 组件通信方式也可以放进 [[../Knowledges/渐进增强|渐进增强]] 的视角里看：先用最直接、最局部的通信方式解决问题，再随着组件层级、共享范围和系统边界扩大，逐步升级到更强的方案。

## 一条渐进增强的主线

`props` -> 回调函数 -> `ref` 暴露实例能力 -> [[./React-useContext|Context]] -> 状态管理库 -> Event Bus / 跨边界通信

这条线不是“越往后越高级”，而是“什么时候前一种方式已经不够用”。

## 第一层：父子直连，先用最朴素的方式

### 通过 `props` 向子组件传递数据

适合：

- 父组件把数据传给子组件
- 数据流清晰且层级很浅
- 当前需求只是单向展示

```tsx
const Parent = () => {
  const message = 'Hello from Parent'
  return <Child message={message} />
}

const Child = ({ message }) => {
  return <div>{message}</div>
}
```

这是最基本的通信方式，也是 React 默认推荐的数据流方向。

### 通过回调函数让子组件通知父组件

适合：

- 子组件要把事件或结果反馈给父组件
- 需要保持“状态提升”后的单向数据流

```tsx
const Parent = () => {
  const handleData = (data) => {
    console.log('Data from Child:', data)
  }

  return <Child onSendData={handleData} />
}

const Child = ({ onSendData }) => {
  return <button onClick={() => onSendData('Hello from Child')}>Send Data</button>
}
```

这本质上不是“子传父”，而是父组件把一个可调用能力传给子组件。

## 第二层：不仅传数据，还要暴露能力

### 使用 `ref` 调用子组件暴露的方法

适合：

- 父组件需要直接触发子组件的某个动作
- 典型场景是 `focus`、滚动、清空输入框、触发动画

```tsx
import React, { forwardRef, useImperativeHandle, useRef } from 'react'

const Child = forwardRef((props, ref) => {
  useImperativeHandle(ref, () => ({
    sayHello() {
      alert('Hello from Child Component!')
    },
  }))

  return <div>Child Component</div>
})

function Parent() {
  const childRef = useRef(null)

  const handleClick = () => {
    childRef.current?.sayHello()
  }

  return (
    <div>
      <Child ref={childRef} />
      <button onClick={handleClick}>Call Child Method</button>
    </div>
  )
}
```

这是一种命令式通信，应该谨慎使用。只有在声明式数据流不自然时，再把它作为增强手段。

它和 [[../Knowledges/React Hooks|React Hooks]] 中的 [[./React-useRef|useRef]]、[[./React-useImperativeHandle|useImperativeHandle]]、[[./react-forwardRef|forwardRef]] 是同一条线。

## 第三层：跨层级传递，避免 props drilling

### 通过 [[./React-useContext|Context]] 进行跨组件通信

适合：

- 多层组件都要消费同一份数据
- 中间层组件只是机械地转发 `props`
- 共享主题、用户信息、语言、配置、轻量 UI 状态

```tsx
import React, { useState } from 'react'

const MyContext = React.createContext()

function Parent() {
  const [sharedData, setSharedData] = useState('Hello from Context')

  const updateData = () => {
    setSharedData('Updated Data from Context')
  }

  return (
    <MyContext.Provider value={{ sharedData, updateData }}>
      <ChildA />
    </MyContext.Provider>
  )
}

function ChildA() {
  return <ChildB />
}

function ChildB() {
  const { sharedData, updateData } = React.useContext(MyContext)

  return (
    <div>
      <div>ChildB: {sharedData}</div>
      <button onClick={updateData}>Update Data</button>
    </div>
  )
}
```

这里开始，通信问题已经逐步过渡到 [[../Knowledges/React 状态管理|React 状态管理]] 问题。

## 第四层：共享范围继续扩大，进入状态管理

### 使用状态管理库进行通信

适合：

- 多个互不相邻的组件需要消费同一份状态
- 通信问题已经上升为共享状态问题
- 需要更清晰的更新机制、拆分粒度和调试能力

典型方向：

- 轻量全局共享：[[./React-Zustand|zustand]]
- 细粒度原子化状态：[[./React-Jotai|jotai]]
- 强约束与工程治理：[[React-Redux|redux]]

这时组件之间已经不是单纯“通信”，而是在围绕同一个状态源协作。

## 第五层：跨组件之外，进入跨系统边界

### 使用事件总线（Event Bus）进行通信

适合：

- 通信双方没有稳定的父子关系
- 需要跨模块、跨子系统广播事件
- 某些场景下用事件比共享状态更自然

但要注意：

- Event Bus 更像“发布事件”，不是“共享状态”
- 一旦滥用，很容易让依赖关系变隐蔽，调试成本上升

所以它通常更适合局部的解耦场景，而不是默认的全局通信方案。

如果系统继续扩大到多应用协作，则可以继续延伸到 [[./微前端的渐进式集成|微前端的渐进式集成]]。

## 如何选择

可以按这个顺序判断：

1. 只是父传子？用 `props`
2. 只是子组件通知父组件？用回调函数
3. 父组件需要直接触发子组件动作？用 `ref`
4. 需要跨层级共享？用 [[./React-useContext|Context]]
5. 需要更大范围的共享状态协作？进入 [[../Knowledges/React 状态管理|React 状态管理]]
6. 需要跨模块广播事件或跨边界协作？再考虑 Event Bus 或更上层的集成方案

## 一个更准确的理解

React 组件通信方式的演进，本质上也是一个渐进增强过程：

- `props` 和回调函数解决局部、清晰、可追踪的通信
- `ref` 解决少量命令式能力暴露
- `Context` 解决跨层共享
- 状态管理库解决跨区域协作
- Event Bus 和系统集成方案解决跨边界通信

问题没有升级时，不要过早引入更重的通信机制；问题一旦越过边界，就应该顺着复杂度自然升级。

## 相关笔记

- [[../Knowledges/React 状态管理|React 状态管理]]
- [[../Knowledges/React Hooks|React Hooks]]
- [[./React-useContext|Context]]
- [[./React-useRef|useRef]]
- [[./微前端的渐进式集成|微前端的渐进式集成]]

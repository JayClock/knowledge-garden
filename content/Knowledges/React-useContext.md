---
date: 2025-04-17T16:36:54
updated: 2026-05-15 12:17:48
up:
  - "[[./React Hooks|React Hooks]]"
related:
  - "[[React-Redux|redux]]"
share: true
noteId: 1778807092839
---
React useContext 用来解决什么问题，核心用法是什么？

---

`useContext` 是 React 组件通信从局部传值走向跨层共享时的一次增强。当前面的 `props` 和回调函数开始变成机械转发时，就说明你可能该从 [[./React 组件通信方式|React 组件通信方式]] 进入 `Context` 了。

 它解决什么问题

`props` 只能沿着父子链路一层层传递。

当多个深层组件都需要同一份数据时，会出现：

- 中间组件并不真正关心这些数据
- 只是为了继续向下传递而写很多 `props`
- 共享需求开始从“通信”升级为“跨层共享”

这就是 `useContext` 的使用时机。

 一句话理解

`Context` 让一棵组件子树共享一份上层提供的值，`useContext` 负责在下游组件中读取这份值。

这里增强的是“传播方式”，不是“状态本身”。

 典型场景

适合：

- 主题
- 当前用户
- 语言
- 配置
- 权限
- 轻量级跨层 UI 状态

不适合直接拿来替代所有状态管理。

 基本机制

1. 用 `createContext` 创建一份上下文
2. 用 `Provider` 在上层提供值
3. 用 `useContext` 在下层读取值

```tsx
const themes = {
  light: {
    foreground: '#000000',
    background: '#eeeeee',
  },
  dark: {
    foreground: '#ffffff',
    background: '#222222',
  },
}

const ThemeContext = React.createContext(themes.light)

function App() {
  const [theme, setTheme] = useState('light')

  const toggleTheme = useCallback(() => {
    setTheme((theme) => (theme === 'light' ? 'dark' : 'light'))
  }, [])

  return (
    <ThemeContext.Provider value={themes[theme]}>
      <button onClick={toggleTheme}>Toggle Theme</button>
      <Toolbar />
    </ThemeContext.Provider>
  )
}

function Toolbar() {
  return <ThemedButton />
}

function ThemedButton() {
  const theme = useContext(ThemeContext)

  return (
    <button
      style={{
        background: theme.background,
        color: theme.foreground,
      }}
    >
      I am styled by theme context!
    </button>
  )
}
```

 什么时候该用

可以优先问自己这几个问题：

1. 这份数据是不是被多个深层组件共享
2. 中间层是不是只是在帮忙传 `props`
3. 这份共享是否局限在某一棵组件树里

如果答案大多是“是”，那 `useContext` 很可能合适。

 什么时候不该用

`useContext` 不天然适合下面这些场景：

- 高频更新的全局状态
- 很大的共享状态对象
- 对拆分粒度、选择性订阅、调试能力要求高的状态系统

因为 `Context` 更擅长“提供共享入口”，不擅长“承担复杂状态治理”。

这时通常应该继续进入 [[./React 状态管理|React 状态管理]]，再看 [[../Cards/React-Zustand|zustand]]、[[../Cards/React-Jotai|jotai]] 或 [[React-Redux|redux]]。

 一个常见误区

很多人会把 `Context` 误解成“全局状态管理”。

更准确的说法是：

- `Context` 解决的是“值如何跨层传播”
- 状态管理库解决的是“状态如何组织、更新、订阅和调试”

所以它们不是简单替代关系，而是复杂度不同阶段的不同解。

 和其它笔记的关系

- 在 [[./React 组件通信方式|React 组件通信方式]] 里，它是从 `props` 升级到跨层共享的关键一步
- 在 [[./React Hooks|React Hooks]] 里，它是函数组件接入共享能力的入口
- 在 [[./React 状态管理|React 状态管理]] 里，它是进入外部 store 之前的一层过渡

## 拆分卡片

- [[../Cards/useContext 解决跨层级共享数据的 props 透传问题|useContext 解决跨层级共享数据的 props 透传问题]]
- [[../Cards/useContext 增强的是数据传播方式而不是状态本身|useContext 增强的是数据传播方式而不是状态本身]]
- [[../Cards/useContext 适合主题用户语言权限等轻量共享数据|useContext 适合主题用户语言权限等轻量共享数据]]

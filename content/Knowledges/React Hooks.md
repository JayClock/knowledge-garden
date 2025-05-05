---
date: 2025-04-16T13:14:31
updated: 2025-05-05T09:50:34
share: true
in:
  - "[[Maps|Maps]]"
---
- 为什么需要 Hooks ?
	1.  React 组件之间不会互相继承，我们不推荐创建一个 Button 组件，然后再创建一个 Dropdown Button 来继承 Button
	2. 所有 ui 都是状态驱动，很少在外部去调用一个类实例（即组件）的方法。组件的所有方法都是在内部调用，或者作为生命周期方法被自动调用。
	3. 函数组件无法存在内部状态，必须是纯函数，而且也无法提供完整的生命周期机制，极大限制了函数组件的大规模使用。
	4. 函数和对象不同，没有一个实例的对象能够在多次执行之间保持状态，势必需要一个函数之外的空间保存这个状态，而且要检测其变化，从而能够触发函数组件的重新渲染。
	5. 为了更好的逻辑复用。
- 状态管理 Hooks
	1. [[../Cards/React-useState|useState]]：用于在函数组件中添加局部状态。
	2. useReducer：用于管理复杂的状态逻辑，类似于 Redux 的 reducer。
	3. [[../Cards/React-useCallback|useCallback]]
	4. [[../Cards/React-useMemo|useMemo]]
- 副作用 Hooks
	1. [[../Cards/React-useEffect|useEffect]]：用于在函数组件中执行副作用操作（如数据获取、订阅、手动 DOM 操作等）
	2. useLayoutEffect：与 useEffect 类似，但在 DOM 更新后同步执行，适用于需要直接操作 DOM 的场景
- 上下文 Hooks
	1. useContext：用于访问 React 的上下文
- 引用 Hooks
	1. [[../Cards/React-useRef|useRef]]：用于创建一个可变的引用对象，通常用于访问 DOM 元素或存储可变值
- 性能优化 Hooks
	1. [[../Cards/React-useMemo|useMemo]]：用于缓存计算结果，避免在每次渲染时重新计算
	2. [[ React-useCallback|useCallback]]：用于缓存回调函数，避免在每次渲染时都创建新的回调。
- 其它 Hooks
	1. useDeferredValue: 延迟更新 UI 的某些部分。
	2. useActionState: 根据某个表单动作的结果更新 state。
	3. useImperativeHandle: 用于自定义暴露给父组件的实例值，通常与 forwardRef 一起使用。主要用于[[../Cards/React 组件通信方式|父子组件传递]]
	4. useDebugValue: 用于在 React 开发者工具中显示自定义 Hook 的标签。
	5. useOptimistic 帮助你更乐观地更新用户界面
	6. useTransition: 用于标记某些状态更新为“过渡”状态，允许你在更新期间显示加载指示器。
	7. useId: 用于生成唯一的 ID，可以生成传递给无障碍属性的唯一 ID。
	8. useSyncExternalStore: 用于订阅外部存储（如 Redux 或 Zustand）的状态。
	9. useInsertionEffect: 为 CSS-in-JS 库的作者特意打造的，在布局副作用触发之前将元素插入到 DOM 中
- hooks 定义规则：
	1. 所有 hook 必须被执行到，也就是不能放在判断条件中
	2. 所有 hook 必须按照顺序执行。
- 四个典型的使用场景
	1. 抽取业务逻辑
	2. 封装通用逻辑
	3. 监听浏览器状态
	4. 拆分复杂组件


tanstack query

本身19已经支持 async function

常用的第三方库
1. lodash
2. ant design 
3. material ui
4. react-use
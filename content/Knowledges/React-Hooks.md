---
date: 2025-04-16T13:14:31
updated: 2025-04-17T22:02:31
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
- 内置的 hooks
	1. [[../Cards/React-useState|useState]]
	2. [[../Cards/React-useEffect|useEffect]]
	3. [[ React-useCallback|useCallback]]
	4. [[../Cards/React-useMemo|useMemo]]
	5. [[../Cards/React-useRef|useRef]]
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
---
date: 2025-09-30 20:00:35
updated: 2025-10-09 16:50:04
share: true
---
1. 如果是基础简单场景，考虑使用 [[../Cards/React-useState|useState]]
	- 适合管理简单状态
	- 适合管理组件内部的局部状态
2. 状态相对复杂，但是不需要全局存储，可以使用 [[React-useReducer|useReducer]]
	- 适合管理复杂的状态逻辑
	- 状态更新依赖于先前状态
3. 状态跨层级消费，可以选择 [[../Cards/React-useContext|useContext]]
	- 适合管理跨组件树的全局状态
	- 避免多层组件传递 props
4. 状态需要跨组件，且相对复杂，则可以选用集中状态管理方案 [[React-Redux|redux]] 、[[../Cards/React-Zustand|zustand]]、[[../Cards/React-Jotai|jotai]]
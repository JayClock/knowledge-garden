---
date: 2024-10-22T09:44:17
updated: 2025-05-05T08:09:23
share: true
source: https://projects.wojtekmaj.pl/react-lifecycle-methods-diagram/
tags:
  - review
---
- **挂载阶段**：组件首次创建并插入到 DOM 中的阶段
	```ts
	useEffect(() => {
	  console.log('代码只会在组件挂载后执行一次')
	}, [])
	```
- **更新阶段**：组件的 props 或 state 发生变化时，就会触发更新阶段
	```ts
	// 注意这里没有提供依赖数组
	useEffect(() => {
	  console.log('代码会在组件挂载后以及每次更新后执行')
	})
	// 特定依赖更新时执行
	useEffect(() => {
	  console.log('代码会在 count 更新后执行')
	}, [count])
	```
- **卸载阶段**：组件从 DOM 中移除时进入卸载阶段
	```ts
	useEffect(() => {
	  return () => {
	    console.log('代码会在组件卸载前执行')
	  }
	}, [])
	```

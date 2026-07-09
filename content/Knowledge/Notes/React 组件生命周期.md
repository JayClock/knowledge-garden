---
date: 2024-10-22T09:44:17
noteId: 1778930949115
source: https://projects.wojtekmaj.pl/react-lifecycle-methods-diagram/
updated: 2026-07-09 20:21:41
---
React 组件生命周期的核心作用和使用场景是什么？

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
![Pasted image 20250505165534](https://knowledge-garden.oss-cn-shanghai.aliyuncs.com/images/React%20%E7%B1%BB%E7%BB%84%E4%BB%B6%E7%94%9F%E5%91%BD%E5%91%A8%E6%9C%9F%E6%B5%81%E7%A8%8B%E5%9B%BE.png)![Pasted image 20250505165544](https://knowledge-garden.oss-cn-shanghai.aliyuncs.com/images/React%20%E5%87%BD%E6%95%B0%E7%BB%84%E4%BB%B6%20Hooks%20%E6%89%A7%E8%A1%8C%E6%B5%81%E7%A8%8B%E5%9B%BE.png)

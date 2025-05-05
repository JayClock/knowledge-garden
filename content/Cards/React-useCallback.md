---
date: 2025-04-17T10:21:36
updated: 2025-05-05T09:37:31
up:
  - "[[React Hooks|React Hooks]]"
share: true
---
- 背景：在 React 组件中，每一次 UI 的变化，都是通过重新执行整个函数来完成的，并没有一个直接的方式，在多次渲染之间维持一个状态。
	```tsx
	// 但是因为定义是在函数组件内部，因此在多次渲染之间，是无法重用 handleIncrement 这个函数的，而是每次都需要创建一个新的：
	function Counter() {
	  const [count, setCount] = useState(0);
	  const handleIncrement = () => setCount(count + 1);
	  // ...
	  return <button onClick={handleIncrement}>+</button>
	}
	```
- 造成的问题：
	即使 count 没有发生变化，但是函数组件其它状态发生变化而重新渲染时，都会重新创建一个 handleIncrement，不仅增加了系统开销，同时让 button 组件误以为 handleIncrement 而重新执行渲染
- 如何调整：
	```tsx
	import React, { useState, useCallback } from 'react';
	
	function Counter() {
	  const [count, setCount] = useState(0);
	  const handleIncrement = useCallback(
	    () => setCount(count + 1),
	    [count], // 只有当 count 发生变化时，才会重新创建回调函数
	  );
	  // ...
	  return <button onClick={handleIncrement}>+</button>
	}
```

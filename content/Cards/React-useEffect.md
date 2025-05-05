---
date: 2025-04-16T13:48:17
updated: 2025-05-05T09:37:31
up:
  - "[[React Hooks|React Hooks]]"
share: true
---
- 定义：执行一段不影响渲染出来的 ui 的代码
- 涵盖的 react 生命周期方法：ComponentDidMount、componentDidUpdate 和 componentWillUnmount
- 执行节点：
	1. 第一次以及依赖项发生变化后执行：提供依赖项数组。比如useEffect(() => {}, [deps])。
		```tsx
		import React, { useState, useEffect } from "react";
		
		function BlogView({ id }) {
		  // 设置一个本地 state 用于保存 blog 内容
		  const [blogContent, setBlogContent] = useState(null);
		
		  useEffect(() => {
		    // useEffect 的 callback 要避免直接的 async 函数，需要封装一下
		    const doAsync = async () => {
		      // 当 id 发生变化时，将当前内容清楚以保持一致性
		      setBlogContent(null);
		      // 发起请求获取数据
		      const res = await fetch(`/blog-content/${id}`);
		      // 将获取的数据放入 state
		      setBlogContent(await res.text());
		    };
		    doAsync();
		  }, [id]); // 使用 id 作为依赖项，变化时则执行副作用
		
		  // 如果没有 blogContent 则认为是在 loading 状态
		  const isLoading = !blogContent;
		  return <div>{isLoading ? "Loading..." : blogContent}</div>;
		}
		```
	2. 每次 render 后执行：不提供第二个依赖项参数。比如useEffect(() => {})。
		```tsx
		useEffect(() => {
		  // 每次 render 完一定执行
		  console.log('re-rendered');
		});
		```
	3. 仅第一次 render 后执行：提供一个空数组作为依赖项。比如useEffect(() => {}, [])只在组件首次 render 后执行，相当于 componentDidMount 生命周期
		```tsx
		useEffect(() => {
		  // 组件首次渲染时执行，等价于 class 组件中的 componentDidMount
		  console.log('did mount');
		}, [])
		```
	4. 组件 unmount 后执行：返回一个回调函数。比如useEffect() => { return () => {} }, [])。
		```tsx
		// 设置一个 size 的 state 用于保存当前窗口尺寸
		const [size, setSize] = useState({});
		useEffect(() => {
		  // 窗口大小变化事件处理函数
		  const handler = () => {
		    setSize(getSize());
		  };
		  // 监听 resize 事件
		  window.addEventListener('resize', handler);
		  
		  // 返回一个 callback 在组件销毁时调用
		  return () => {
		    // 移除 resize 事件
		    window.removeEventListener('resize', handler);
		  };
		}, []);
		```


---
date: 2025-04-17T16:31:32
updated: 2025-05-05T09:37:31
up:
  - "[[React Hooks|React Hooks]]"
share: true
---
- 背景：在 class 组件中，我们可以定义类的成员变量，来保存一些数据，但是在函数组件中，没有这样一个空间去保存数据。
	```tsx
	import React, { useState, useCallback, useRef } from "react";
	export default function Timer() {
	  // 定义 time state 用于保存计时的累积时间
	  const [time, setTime] = useState(0);
	
	  // 定义 timer 这样一个容器用于在跨组件渲染之间保存一个变量
	  const timer = useRef(null);
	
	  // 开始计时的事件处理函数
	  const handleStart = useCallback(() => {
	    // 使用 current 属性设置 ref 的值
	    timer.current = window.setInterval(() => {
	      setTime((time) => time + 1);
	    }, 100);
	  }, []);
	
	  // 暂停计时的事件处理函数
	  const handlePause = useCallback(() => {
	    // 使用 clearInterval 来停止计时
	    window.clearInterval(timer.current);
	    timer.current = null;
	  }, []);
	
	  return (
	    <div>
	      {time / 10} seconds.
	      <br />
	      <button onClick={handleStart}>Start</button>
	      <button onClick={handlePause}>Pause</button>
	    </div>
	  );
	}
	```
- 注意点：useRef 保存的数据一般是和 UI 的渲染无关的，即 useRef 不会触发组件的重新渲染。
- 另一个场景：获取 DOM 元素
	```tsx
	function TextInputWithFocusButton() {
	  const inputEl = useRef(null);
	  const onButtonClick = () => {
	    // current 属性指向了真实的 input 这个 DOM 节点，从而可以调用 focus 方法
	    inputEl.current.focus();
	  };
	  return (
	    <>
	      <input ref={inputEl} type="text" />
	      <button onClick={onButtonClick}>Focus the input</button>
	    </>
	  );
	}
	```

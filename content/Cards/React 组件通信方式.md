---
date: 2025-05-05T08:14:11
updated: 2025-05-05T08:19:39
share: true
---
- **通过 props 向子组件传递数据**
	```tsx
	//父组件
	const Parent = () => {
	  const message = 'Hello from Parent'
	  return <Child message={message} />
	}
	
	// 子组件
	const Child = ({ message }) => {
	  return <div>{message}</div>
	}
```
- **通过回调函数向父组件传递数据**
	```tsx
	//父组件
	const Parent = () => {
	  const handleData = (data) => {
	    console.log('Data from Child:', data)
	  }
	  return <Child onSendData={handleData} />
	}
	
	// 子组件
	const Child = ({ message }) => {
	  return <button onClick={() => onSendData('Hello from Child')}>Send Data</button>
	}
```
- **使用 useRef 调用子组件暴露的方法**
	```tsx
	import React, { useRef, forwardRef, useImperativeHandle } from 'react'
	
	// 子组件
	const Child = forwardRef((props, ref) => {
	  // 暴露方法给父组件
	  useImperativeHandle(ref, () => ({
	    sayHello() {
	      alert('Hello from Child Component!')
	    },
	  }))
	
	  return <div>Child Component</div>
	})
	
	// 父组件
	function Parent() {
	  const childRef = useRef(null)
	
	  const handleClick = () => {
	    if (childRef.current) {
	      childRef.current.sayHello()
	    }
	  }
	
	  return (
	    <div>
	      <Child ref={childRef} />
	      <button onClick={handleClick}>Call Child Method</button>
	    </div>
	  )
	}
	
	export default Parent
	```
- **通过 Context 进行跨组件通信**
	```tsx
	import React, { useState } from 'react'
	
	// 创建一个 Context
	const MyContext = React.createContext()
	
	// 父组件
	function Parent() {
	  const [sharedData, setSharedData] = useState('Hello from Context')
	
	  const updateData = () => {
	    setSharedData('Updated Data from Context')
	  }
	
	  return (
	    // 提供数据和更新函数
	    <MyContext.Provider value={{ sharedData, updateData }}>
	      <ChildA />
	    </MyContext.Provider>
	  )
	}
	
	// 子组件 A（引用子组件 B）
	function ChildA() {
	  return (
	    <div>
	      <ChildB />
	    </div>
	  )
	}
	
	// 子组件 B（使用 useContext）
	function ChildB() {
	  const { sharedData, updateData } = React.useContext(MyContext)
	  return (
	    <div>
	      <div>ChildB: {sharedData}</div>
	      <button onClick={updateData}>Update Data</button>
	    </div>
	  )
	}
	
	export default Parent
```
- **使用状态管理库进行通信**
- **使用事件总线（Event Bus）进行通信**